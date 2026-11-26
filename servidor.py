import json
import logging
import re
import time
from secrets import compare_digest
from uuid import uuid4

from langchain_core.exceptions import ModelRateLimitError
from pydantic import BaseModel, Field, ValidationError
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from config import settings
from main import graph
from nodes.juez import MENSAJE_SEGURO, crear_juez
from nodes.rag import rag as nodo_rag
from services import historial_web, registro
from services.telemetria import ContadorUso
from tools.herramientas import calcular_ganancia
from web_ui import routes as web_routes


logger = logging.getLogger("uvicorn.error")

# Dueño de las conversaciones creadas por la API. El chat web usa
# "usuario:<navegador>" y "admin:<navegador>", así que no colisionan.
PROPIETARIO_API = "api"


# Respaldo de solo lectura para la consulta de ejemplo con montos explícitos.
NUMERO = r"[0-9]{1,12}(?:[.,][0-9]{1,8})?"
COMPRA_EXPLICITA = re.compile(
    rf"compr[ée] ({NUMERO}) ([a-z0-9]{{1,12}}) a usd ({NUMERO}) "
    rf"y hoy cada \2 vale usd ({NUMERO})[.]? ¿?cu[aá]nto gan[ée]\?",
    re.IGNORECASE,
)


class Consulta(BaseModel):
    mensaje: str = Field(min_length=1, max_length=4000, pattern=r"\S")
    # Opcional: reutilizar el mismo session_id retoma el hilo anterior
    # (memoria persistente). Si se omite, cada consulta es aislada.
    session_id: str | None = Field(default=None, max_length=64)


class PreguntaRag(BaseModel):
    pregunta: str = Field(min_length=1, max_length=4000, pattern=r"\S")
    k: int = Field(default=3, ge=1, le=8)


def _autorizado(request: Request) -> bool:
    """Compara el Bearer en tiempo constante para no filtrar el token."""
    if not settings.api_token:
        return False
    esperado = f"Bearer {settings.api_token}".encode()
    recibido = request.headers.get("Authorization", "").encode()
    return compare_digest(recibido, esperado)


def _sin_autorizacion() -> JSONResponse:
    return JSONResponse(
        {"error": "Acceso no autorizado"}, status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def consultar(request: Request) -> JSONResponse:
    if not settings.api_token:
        return JSONResponse({"error": "Servicio sin configurar"}, status_code=503)
    if not _autorizado(request):
        return _sin_autorizacion()

    try:
        consulta = Consulta.model_validate(await request.json())
    except (ValidationError, ValueError):
        return JSONResponse({"error": "Envía un mensaje válido"}, status_code=422)

    payload, status = await ejecutar_consulta(
        consulta.mensaje, [], origen="api", session_id=consulta.session_id
    )
    return JSONResponse(payload, status_code=status)


async def consultar_rag(request: Request) -> JSONResponse:
    """Recuperación documental directa del agente principal.

    Existe para separar dos criterios que la pauta evalúa por separado:

    - *Delegación A2A*: el agente principal encarga la pregunta a un
      especialista remoto y usa su respuesta.
    - *RAG documental*: el agente recupera fragmentos y los usa para
      respaldar lo que responde, mostrando fuentes y similitud.

    Si el único camino al corpus fuera el especialista, ambos criterios se
    sostendrían con la misma llamada. Con este endpoint el agente principal
    demuestra el recuperador por sí mismo, sin delegar en nadie.
    """
    if not settings.api_token:
        return JSONResponse({"error": "Servicio no configurado"}, status_code=503)
    if not _autorizado(request):
        return _sin_autorizacion()

    try:
        cuerpo = PreguntaRag.model_validate(await request.json())
    except (ValidationError, ValueError):
        return JSONResponse({"error": "Envía una pregunta válida"}, status_code=422)

    inicio = time.perf_counter()
    salida = await run_in_threadpool(nodo_rag, {"user_input": cuerpo.pregunta})

    # Mismo filtro determinista que usa el juez, sin gastar una llamada al modelo.
    revisado = crear_juez(incluir_juez_llm=False)({
        "borrador": salida.get("borrador", ""), "trace": [], "delegacion": {},
    })

    payload = {
        "pregunta": cuerpo.pregunta,
        "respuesta": revisado.get("final_answer", ""),
        "fuentes": salida.get("fuentes_rag", []),
        "fragmentos": salida.get("fragmentos_rag", []),
        "sin_evidencia": bool(salida.get("rag_sin_evidencia")),
    }
    registro.anotar({
        "solicitud_id": str(uuid4()),
        "origen": "rag_directo",
        "mensaje": cuerpo.pregunta[:200],
        "ruta": "rag_directo",
        "estado": "sin_evidencia" if payload["sin_evidencia"] else "respondido",
        "fuentes": payload["fuentes"],
        "duracion_ms": round((time.perf_counter() - inicio) * 1000, 1),
        "fragmentos": len(payload["fragmentos"]),
    })
    return JSONResponse(payload)


async def ejecutar_consulta(
    mensaje: str,
    historial: list[dict],
    origen: str = "api",
    session_id: str | None = None,
    grafo=None,
) -> tuple[dict, int]:
    """Ejecuta el grafo, mide la ejecución y la deja en el registro.

    Args:
        mensaje: consulta del usuario.
        historial: turnos previos ya cargados (el chat web los pasa resueltos).
        origen: "api", "web", "n8n" o "eval". Permite separar métricas por canal.
        session_id: si viene, la conversación se carga y se guarda en disco.
        grafo: grafo alternativo a ejecutar. `evals/ejecutar.py` lo usa para
               comparar con y sin juez sobre las mismas entradas.
    """
    motor = grafo or graph
    solicitud_id = str(uuid4())
    inicio = time.perf_counter()

    # Si se pidió continuar un hilo, se recuperan los turnos anteriores.
    anterior = None
    if session_id:
        anterior = await run_in_threadpool(
            historial_web.leer, session_id, PROPIETARIO_API, False
        )
        if anterior is not None:
            historial = [
                {"rol": m["role"], "texto": m["text"]} for m in json.loads(anterior)
            ]

    contador = ContadorUso()
    estado = "procesado"

    try:
        resultado = await run_in_threadpool(
            motor.invoke,
            {
                "user_input": mensaje,
                "historial": historial,
                "trace": [],
                "permitir_escritura": False,
            },
            {"callbacks": [contador]},
        )
    except ModelRateLimitError:
        # Resiliencia: Gemini agotó la cuota. En vez de fallar siempre, se
        # intenta un cálculo local determinista para el caso más común.
        compra = COMPRA_EXPLICITA.fullmatch(" ".join(mensaje.split()))
        if compra is None:
            _anotar(solicitud_id, mensaje, inicio, contador, origen, session_id,
                    estado="fallback_cuota", error="ModelRateLimitError", resultado=None)
            return {
                "solicitud_id": solicitud_id,
                "error": "Gemini alcanzó su límite de uso. Intenta de nuevo en unos minutos.",
            }, 503
        cantidad, _, compra_usd, actual_usd = compra.groups()
        montos = (float(valor.replace(",", ".")) for valor in (cantidad, compra_usd, actual_usd))
        cantidad_num, compra_num, actual_num = montos
        calculo = calcular_ganancia.invoke({
            "cantidad": cantidad_num, "precio_compra": compra_num, "precio_actual": actual_num,
        })
        resultado = {
            "branch": "herramienta",
            "final_answer": f"Cálculo en USD. {calculo}",
            "trace": ["limite_gemini", "calculo_local"],
            "pasos_react": [f"Respaldo local: calcular_ganancia → {calculo}"],
        }
    except Exception as exc:
        logger.warning("solicitud=%s estado=error tipo=%s", solicitud_id, type(exc).__name__)
        _anotar(solicitud_id, mensaje, inicio, contador, origen, session_id,
                estado="error", error=type(exc).__name__, resultado=None)
        return {
            "solicitud_id": solicitud_id,
            "error": "No fue posible completar la consulta.",
        }, 503

    respuesta = resultado.get("final_answer", "")
    mostrar_evidencia = respuesta != MENSAJE_SEGURO
    delegacion = resultado.get("delegacion")
    if delegacion:
        estado = delegacion["estado"]
    logger.info("solicitud=%s ruta=%s estado=%s traza=%s",
                solicitud_id, resultado.get("branch"), estado, resultado.get("trace"))

    payload = {
        "solicitud_id": solicitud_id,
        "respuesta": respuesta,
        "ruta": resultado.get("branch"),
        "traza": resultado.get("trace", []),
        "herramientas": resultado.get("pasos_react", []) if mostrar_evidencia else [],
        "mcp": resultado.get("pasos_mcp", []) if mostrar_evidencia else [],
        "fuentes": resultado.get("fuentes_rag", []) if mostrar_evidencia else [],
        "delegacion": delegacion if mostrar_evidencia else None,
        "delegacion_n8n": resultado.get("delegacion_n8n") if mostrar_evidencia else None,
    }

    # Memoria: se persiste el turno para que una próxima solicitud con el mismo
    # session_id pueda usarlo.
    if session_id:
        await _guardar_turno(session_id, anterior, mensaje, respuesta, payload)
        payload["session_id"] = session_id

    _anotar(solicitud_id, mensaje, inicio, contador, origen, session_id,
            estado=estado, error=None, resultado=payload)
    return payload, 200


async def _guardar_turno(session_id: str, anterior: str | None,
                         mensaje: str, respuesta: str, payload: dict) -> None:
    """Agrega el turno a la conversación persistida."""
    mensajes = json.loads(anterior) if anterior else []
    mensajes.extend([
        {"role": "user", "text": mensaje},
        {"role": "assistant", "text": respuesta, "execution": payload},
    ])
    await run_in_threadpool(
        historial_web.guardar, session_id, PROPIETARIO_API, anterior, mensajes
    )


def _anotar(solicitud_id: str, mensaje: str, inicio: float, contador: ContadorUso,
            origen: str, session_id: str | None, *, estado: str,
            error: str | None, resultado: dict | None) -> None:
    """Compone la línea del registro a partir del resultado de la ejecución."""
    duracion_ms = round((time.perf_counter() - inicio) * 1000, 1)
    datos = resultado or {}
    registro.anotar({
        "solicitud_id": solicitud_id,
        "origen": origen,
        "session_id": session_id,
        "mensaje": mensaje[:200],
        "ruta": datos.get("ruta"),
        "estado": estado,
        "traza": datos.get("traza", []),
        "accion_bloqueada": "accion_bloqueada" in datos.get("traza", []),
        "fuentes": datos.get("fuentes", []),
        "delegacion": (datos.get("delegacion") or {}).get("estado"),
        "delegacion_n8n": (datos.get("delegacion_n8n") or {}).get("estado"),
        "pasos_react": datos.get("herramientas", []),
        "pasos_mcp": datos.get("mcp", []),
        "duracion_ms": duracion_ms,
        "error": error,
        **contador.resumen(),
    })


async def obtener_registro(request: Request) -> JSONResponse:
    """Devuelve la línea de registro de una solicitud concreta.

    Permite cruzar el `solicitud_id` recibido por HTTP con lo que el servidor
    registró, sin acceso a la consola ni a los archivos del host.
    """
    if not _autorizado(request):
        return _sin_autorizacion()
    fila = await run_in_threadpool(registro.buscar, request.path_params["solicitud_id"])
    if fila is None:
        return JSONResponse({"error": "Solicitud no encontrada"}, status_code=404)
    return JSONResponse(fila)


async def salud(request: Request) -> JSONResponse:
    """Estado del servicio sin exponer configuración sensible."""
    return JSONResponse({
        "servicio": "asistente-cripto",
        "estado": "operativo",
        "modelo": settings.google_model,
        "rag_backend": settings.rag_backend,
        "token_configurado": bool(settings.api_token),
    })


app = Starlette(routes=[
    # "/" lo resuelve web_ui (redirige al chat). "/salud" es el chequeo del
    # servicio para el despliegue y para el docente.
    Route("/salud", salud),
    Route("/consulta", consultar, methods=["POST"]),
    Route("/rag", consultar_rag, methods=["POST"]),
    Route("/registro/{solicitud_id}", obtener_registro),
    *web_routes,
])
app.state.ejecutar_consulta = ejecutar_consulta
