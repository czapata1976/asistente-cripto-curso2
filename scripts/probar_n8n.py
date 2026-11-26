"""Prueba directa del webhook A2A del workflow de n8n."""

import json
import sys
import uuid

import httpx

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = "http://127.0.0.1:5678/webhook/a2a-plan"

parametros = {"monto_usd": 50, "frecuencia": "semanal", "semanas": 12, "cripto": "bitcoin"}
texto = "Armar un plan de compra periódica.\nParámetros: " + json.dumps(parametros, ensure_ascii=False)
message_id = str(uuid.uuid4())

solicitud = {
    "jsonrpc": "2.0",
    "id": message_id,
    "method": "message/send",
    "params": {"message": {
        "role": "user",
        "messageId": message_id,
        "parts": [{"kind": "text", "text": texto}],
    }},
}

print("POST", URL)
try:
    respuesta = httpx.post(URL, json=solicitud, timeout=30)
except httpx.HTTPError as exc:
    print(f"ERROR de conexion: {type(exc).__name__}: {exc}")
    raise SystemExit(1)

print("HTTP", respuesta.status_code)
cuerpo = respuesta.json()
print(json.dumps(cuerpo, ensure_ascii=False, indent=2)[:1500])

# Comprobaciones
assert cuerpo.get("id") == message_id, "el id de la respuesta no coincide"
tarea = cuerpo["result"]
assert tarea["status"]["state"] == "completed", "la tarea no se completo"
artefacto = json.loads(tarea["artifacts"][0]["parts"][0]["text"])
print("\nARTEFACTO:")
print(f"  compras: {artefacto['compras']}")
print(f"  total_usd: {artefacto['total_usd']}")
print(f"  primeras: {artefacto['plan'][:2]}")
assert artefacto["compras"] == 12 and abs(artefacto["total_usd"] - 600.0) < 0.01
print("\nOK: el workflow de n8n responde A2A correctamente.")
