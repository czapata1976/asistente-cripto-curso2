"""Cliente A2A para el agente especialista alojado en n8n.

Habla el mismo protocolo que el especialista LangGraph (`services/a2a_cliente.py`):
descubre/usa un endpoint y envía un mensaje JSON-RPC `message/send`, esperando
un artefacto con un `part.text`. La diferencia es el transporte: aquí no hay
descubrimiento, porque un workflow de n8n se expone como webhook con una URL fija.

Este es el flujo A2A **adicional** de la pauta: no reemplaza al obligatorio
(conceptos de la guía), sino que resuelve otro caso — armar un plan de compra
periódica de práctica — con un especialista distinto, ejecutado en n8n.
"""

import json
from urllib.parse import urlparse
from uuid import uuid4

import httpx
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from config import settings


NOMBRE_ESPECIALISTA_N8N = "n8n_plan_dca"


class N8NNoConfigurado(RuntimeError):
    """El despliegue no tiene N8N_WEBHOOK_URL.

    Se separa de un fallo de red porque el diagnóstico y el mensaje al usuario
    son distintos: aquí no hay nada que reintentar, falta configuración.
    En Cloud Run esto ocurre si el servicio no recibió la variable: el
    contenedor no lleva `.env` (está en `.dockerignore`).
    """


class N8NInalcanzable(RuntimeError):
    """La URL está configurada pero n8n no respondió.

    El caso típico es apuntar a `127.0.0.1`: dentro de Cloud Run ese host es el
    propio contenedor del agente, no la máquina del desarrollador. n8n debe
    estar en una URL que el servicio alcance, normalmente otro servicio de
    Cloud Run.
    """


def _extraer_texto(tarea: dict) -> str:
    """Saca el primer texto de los artefactos de la tarea A2A."""
    for artefacto in tarea.get("artifacts") or []:
        for parte in artefacto.get("parts") or []:
            if "text" in parte:
                return parte["text"]
    raise ValueError("La tarea A2A no devolvió una respuesta")


def pedir_plan(encargo: str, parametros: dict) -> tuple[str, dict]:
    """Envía el encargo al workflow de n8n y devuelve (tarea_id, artefacto).

    Args:
        encargo: lo que pidió la persona, en lenguaje natural.
        parametros: parámetros ya resueltos por el LLM del agente principal
                    (monto, frecuencia, semanas, cripto). n8n no necesita un
                    modelo propio: solo calcula y da formato.

    Raises:
        N8NNoConfigurado: falta `N8N_WEBHOOK_URL` en este despliegue.
        N8NInalcanzable: hay URL pero la conexión falló o n8n devolvió error.
        ValueError: n8n respondió algo que no cumple el contrato A2A.
    """
    url = settings.n8n_webhook_url.strip()
    if not url:
        raise N8NNoConfigurado(
            "N8N_WEBHOOK_URL no está definida: el flujo de plan está deshabilitado."
        )

    message_id = str(uuid4())
    texto = f"{encargo}\nParámetros: {json.dumps(parametros, ensure_ascii=False)}"

    cabeceras: dict[str, str] = {}
    if settings.n8n_cloud_run_iam:
        # n8n desplegado como servicio privado de Cloud Run: se pide un ID
        # token para la audiencia del servicio. Es el mismo mecanismo que usa
        # `services/a2a_cliente.py` con el especialista LangGraph.
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        cabeceras["Authorization"] = f"Bearer {id_token.fetch_id_token(Request(), base)}"

    try:
        with httpx.Client(timeout=httpx.Timeout(30, connect=5), headers=cabeceras) as cliente:
            respuesta = cliente.post(url, json={
                "jsonrpc": "2.0",
                "id": message_id,
                "method": "message/send",
                "params": {"message": {
                    "role": "user",
                    "messageId": message_id,
                    "parts": [{"kind": "text", "text": texto}],
                }},
            })
            respuesta.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise N8NInalcanzable(
            f"n8n respondió HTTP {exc.response.status_code} en {url}"
        ) from exc
    except httpx.HTTPError as exc:
        raise N8NInalcanzable(f"no se pudo conectar a {url}: {type(exc).__name__}") from exc

    cuerpo = respuesta.json()
    if cuerpo.get("id") != message_id:
        raise ValueError("Respuesta A2A inválida: el id no coincide")
    if "error" in cuerpo:
        raise ValueError(str((cuerpo["error"] or {}).get("message", "error de n8n")))

    tarea = cuerpo["result"]
    estado = (tarea.get("status") or {}).get("state")
    if estado not in {"completed", "TASK_STATE_COMPLETED"}:
        raise ValueError(f"n8n no completó la tarea (estado={estado})")

    return tarea["id"], json.loads(_extraer_texto(tarea))
