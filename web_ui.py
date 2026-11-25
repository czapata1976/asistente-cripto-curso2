"""Sesiones de navegador y rutas del chat del Asistente cripto."""
import hashlib
import hmac
import json
import re
import time
from base64 import b64encode
from datetime import datetime, timezone
from pathlib import Path
from secrets import compare_digest, token_bytes
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from config import settings
from services import historial_web


PAGES = Path(__file__).resolve().parent / "web"
SESSION = "cripto_session"
BROWSER = "cripto_browser"
SESSION_SECONDS = 8 * 3600
TEMP_SECRET = token_bytes(32)


class Login(BaseModel):
    username: Literal["usuario", "admin"]
    password: str = Field(min_length=1, max_length=256)


class Chat(BaseModel):
    message: str = Field(min_length=1, max_length=4000, pattern=r"\S")
    session_id: UUID4 | None = None


class Delete(BaseModel):
    session_id: UUID4


def password_for(role: str) -> str:
    return {"usuario": settings.web_user_password, "admin": settings.web_admin_password}.get(role, "")


def firmar(texto: str) -> str:
    secret = settings.web_session_secret.encode() or TEMP_SECRET
    return hmac.digest(secret, f"cripto:{texto}".encode(), "sha256").hex()


def identidad(request: Request) -> tuple[str, str] | None:
    campos = request.cookies.get(SESSION, "").split(".")
    if len(campos) != 4:
        return None
    role, browser, expires, digest = campos
    password = password_for(role)
    if not password or not re.fullmatch(r"[0-9]{1,12}", expires) or int(expires) <= time.time():
        return None
    if not compare_digest(digest.encode(), firmar(f"session:{role}.{browser}.{expires}.{password}").encode()):
        return None
    return role, f"{role}:{browser}"


def error(texto: str, status: int) -> JSONResponse:
    return JSONResponse({"error": texto}, status_code=status, headers={"Cache-Control": "no-store"})


async def leer_json(request: Request, modelo: type[BaseModel]):
    if request.headers.get("content-type", "").partition(";")[0].strip().lower() != "application/json":
        raise ValueError("Se esperaba JSON")
    return modelo.model_validate(await request.json())


async def root(request: Request) -> RedirectResponse:
    return RedirectResponse("/app")


async def pagina(request: Request) -> HTMLResponse:
    nombre = "chat.html" if identidad(request) else "login.html"
    html = (PAGES / nombre).read_text(encoding="utf-8")
    directivas = ["default-src 'none'", "connect-src 'self'", "img-src 'self'", "base-uri 'none'",
                  "form-action 'self'", "frame-ancestors 'none'"]
    for tag in ("style", "script"):
        hashes = ["'sha256-" + b64encode(hashlib.sha256(block.encode()).digest()).decode() + "'"
                  for block in re.findall(f"<{tag}>(.*?)</{tag}>", html, re.DOTALL)]
        directivas.append(f"{tag}-src " + (" ".join(hashes) or "'none'"))
    return HTMLResponse(html, headers={
        "Cache-Control": "no-store",
        "Content-Security-Policy": "; ".join(directivas),
        "X-Content-Type-Options": "nosniff",
    })


async def login(request: Request) -> JSONResponse:
    if not (settings.web_user_password or settings.web_admin_password):
        return error("Acceso web sin configurar", 503)
    if settings.web_user_password and settings.web_user_password == settings.web_admin_password:
        return error("Configura contraseñas distintas para los dos roles", 503)
    try:
        body = await leer_json(request, Login)
    except ValueError:
        return error("Usuario o contraseña incorrectos", 401)
    password = password_for(body.username)
    if not password or not compare_digest(password.encode(), body.password.encode()):
        return error("Usuario o contraseña incorrectos", 401)

    browser, _, firma = request.cookies.get(BROWSER, "").partition(".")
    if not re.fullmatch(r"[0-9a-f]{32}", browser) or not compare_digest(
        firma.encode(), firmar(f"browser:{browser}").encode()
    ):
        browser = uuid4().hex
    payload = f"{body.username}.{browser}.{int(time.time()) + SESSION_SECONDS}"
    cookie = {"path": "/app", "httponly": True, "samesite": "strict",
              "secure": settings.web_secure_cookie or request.url.scheme == "https"}
    response = JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})
    response.set_cookie(
        SESSION, f"{payload}.{firmar(f'session:{payload}.{password}')}", max_age=SESSION_SECONDS, **cookie
    )
    response.set_cookie(BROWSER, f"{browser}.{firmar(f'browser:{browser}')}", max_age=365 * 24 * 3600, **cookie)
    return response


async def logout(request: Request) -> JSONResponse:
    response = JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})
    response.delete_cookie(
        SESSION, path="/app", httponly=True, samesite="strict",
        secure=settings.web_secure_cookie or request.url.scheme == "https",
    )
    return response


async def history(request: Request) -> JSONResponse:
    identity = identidad(request)
    if identity is None:
        return error("Inicia sesión para continuar", 401)
    role, owner = identity
    admin = role == "admin"
    chats = await run_in_threadpool(historial_web.historial, owner, admin)
    return JSONResponse({"canDelete": admin, "chats": chats}, headers={"Cache-Control": "no-store"})


async def chat(request: Request) -> JSONResponse:
    identity = identidad(request)
    if identity is None:
        return error("Inicia sesión para continuar", 401)
    role, owner = identity
    try:
        body = await leer_json(request, Chat)
    except ValueError:
        return error("Mensaje o ID de conversación inválido", 422)

    chat_id = str(body.session_id or uuid4())
    anterior = None
    if body.session_id:
        anterior = await run_in_threadpool(historial_web.leer, chat_id, owner, role == "admin")
        if anterior is None:
            return error("Conversación no encontrada", 404)

    mensajes = json.loads(anterior) if anterior else []
    historial = [{"rol": mensaje["role"], "texto": mensaje["text"]} for mensaje in mensajes]
    resultado, status = await request.app.state.ejecutar_consulta(body.message.strip(), historial)
    if status != 200:
        return JSONResponse(resultado, status_code=status, headers={"Cache-Control": "no-store"})

    reply = resultado.pop("respuesta")
    timestamp = datetime.now(timezone.utc).isoformat()
    mensajes.extend([
        {"role": "user", "text": body.message.strip()},
        {"role": "assistant", "text": reply, "answeredAt": timestamp, "execution": resultado},
    ])
    if not await run_in_threadpool(historial_web.guardar, chat_id, owner, anterior, mensajes):
        return error("La conversación cambió. Recarga la página e intenta nuevamente.", 409)
    return JSONResponse(
        {"session_id": chat_id, "reply": reply, "answeredAt": timestamp, "execution": resultado},
        headers={"Cache-Control": "no-store"},
    )


async def delete(request: Request) -> Response:
    identity = identidad(request)
    if identity is None:
        return error("Inicia sesión para continuar", 401)
    if identity[0] != "admin":
        return error("Solo el administrador puede eliminar conversaciones", 403)
    try:
        body = await leer_json(request, Delete)
    except ValueError:
        return error("ID de conversación inválido", 422)
    if not await run_in_threadpool(historial_web.eliminar, str(body.session_id)):
        return error("Conversación no encontrada", 404)
    return Response(status_code=204)


async def logo(request: Request) -> FileResponse:
    return FileResponse(PAGES / "logo-cripto.png", media_type="image/png")


routes = [
    Route("/app/logo-cripto.png", logo),
    Route("/", root),
    Route("/app", pagina),
    Route("/app/login", login, methods=["POST"]),
    Route("/app/logout", logout, methods=["POST"]),
    Route("/app/history", history),
    Route("/app/chat", chat, methods=["POST"]),
    Route("/app/chat", delete, methods=["DELETE"]),
]
