import logging
from secrets import compare_digest
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from config import settings
from main import graph
from nodes.juez import MENSAJE_SEGURO
from web_ui import routes as web_routes


logger = logging.getLogger("uvicorn.error")


class Consulta(BaseModel):
    mensaje: str = Field(min_length=1, max_length=4000, pattern=r"\S")


async def consultar(request: Request) -> JSONResponse:
    if not settings.api_token:
        return JSONResponse({"error": "Servicio sin configurar"}, status_code=503)
    esperado = f"Bearer {settings.api_token}".encode()
    recibido = request.headers.get("Authorization", "").encode()
    if not compare_digest(recibido, esperado):
        return JSONResponse(
            {"error": "Acceso no autorizado"}, status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        consulta = Consulta.model_validate(await request.json())
    except (ValidationError, ValueError):
        return JSONResponse({"error": "Envía un mensaje válido"}, status_code=422)

    payload, status = await ejecutar_consulta(consulta.mensaje, [])
    return JSONResponse(payload, status_code=status)


async def ejecutar_consulta(mensaje: str, historial: list[dict]) -> tuple[dict, int]:
    solicitud_id = str(uuid4())
    try:
        resultado = await run_in_threadpool(graph.invoke, {
            "user_input": mensaje,
            "historial": historial,
            "trace": [],
            "permitir_escritura": False,
        })
    except Exception as exc:
        logger.warning("solicitud=%s estado=error tipo=%s", solicitud_id, type(exc).__name__)
        return {
            "solicitud_id": solicitud_id,
            "error": "No fue posible completar la consulta.",
        }, 503

    respuesta = resultado.get("final_answer", "")
    mostrar_evidencia = respuesta != MENSAJE_SEGURO
    delegacion = resultado.get("delegacion")
    estado = delegacion["estado"] if delegacion else "procesado"
    logger.info("solicitud=%s ruta=%s estado=%s traza=%s",
                solicitud_id, resultado.get("branch"), estado, resultado.get("trace"))
    return {
        "solicitud_id": solicitud_id,
        "respuesta": respuesta,
        "ruta": resultado.get("branch"),
        "traza": resultado.get("trace", []),
        "herramientas": resultado.get("pasos_react", []) if mostrar_evidencia else [],
        "mcp": resultado.get("pasos_mcp", []) if mostrar_evidencia else [],
        "fuentes": resultado.get("fuentes_rag", []) if mostrar_evidencia else [],
        "delegacion": delegacion if mostrar_evidencia else None,
    }, 200


app = Starlette(routes=[Route("/consulta", consultar, methods=["POST"]), *web_routes])
app.state.ejecutar_consulta = ejecutar_consulta
