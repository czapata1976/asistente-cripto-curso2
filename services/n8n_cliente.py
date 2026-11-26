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
from uuid import uuid4

import httpx

from config import settings


NOMBRE_ESPECIALISTA_N8N = "n8n_plan_dca"


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
    """
    url = settings.n8n_webhook_url.strip()
    if not url:
        raise RuntimeError("Configura N8N_WEBHOOK_URL para usar el especialista n8n")

    message_id = str(uuid4())
    texto = f"{encargo}\nParámetros: {json.dumps(parametros, ensure_ascii=False)}"

    with httpx.Client(timeout=httpx.Timeout(30, connect=5)) as cliente:
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
