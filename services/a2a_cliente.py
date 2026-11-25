from uuid import uuid4

import httpx
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from config import settings
from services.contrato_a2a import RespuestaEspecialista


NOMBRE_ESPECIALISTA = "especialista_cripto"


def consultar_especialista(pregunta: str) -> tuple[str, RespuestaEspecialista]:
    """Descubre al especialista y envía un encargo A2A por JSON-RPC."""
    base = settings.especialista_url.rstrip("/")
    headers = {}
    if settings.especialista_token:
        headers["X-Api-Key"] = settings.especialista_token

    if settings.especialista_cloud_run_iam:
        token = id_token.fetch_id_token(Request(), base)
        headers["Authorization"] = f"Bearer {token}"

    with httpx.Client(headers=headers, timeout=httpx.Timeout(30, connect=4)) as cliente:
        discovery = cliente.post(
            f"{base}/assistants/search",
            json={"graph_id": NOMBRE_ESPECIALISTA, "limit": 1},
        )
        discovery.raise_for_status()
        assistant_id = discovery.json()[0]["assistant_id"]
        message_id = str(uuid4())
        respuesta = cliente.post(f"{base}/a2a/{assistant_id}", json={
            "jsonrpc": "2.0",
            "id": message_id,
            "method": "message/send",
            "params": {"message": {
                "role": "user",
                "messageId": message_id,
                "parts": [{"kind": "text", "text": pregunta}],
            }},
        })
        respuesta.raise_for_status()

    cuerpo = respuesta.json()
    if cuerpo.get("id") != message_id or "error" in cuerpo:
        raise ValueError("Respuesta A2A inválida")
    resultado = cuerpo["result"]
    tarea = resultado.get("task", resultado)
    if tarea["status"]["state"] not in {"completed", "TASK_STATE_COMPLETED"}:
        raise ValueError("El especialista no completó la tarea")
    for artefacto in tarea["artifacts"]:
        for parte in artefacto.get("parts", []):
            if "text" in parte:
                return tarea["id"], RespuestaEspecialista.model_validate_json(parte["text"])
    raise ValueError("La tarea A2A no devolvió una respuesta")
