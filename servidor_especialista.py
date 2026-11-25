"""Servidor HTTP del especialista para el intercambio A2A usado por el chat."""
from uuid import uuid4

from langchain_core.messages import HumanMessage
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from especialista import graph

AGENTE = "especialista_cripto"


async def buscar(request: Request) -> JSONResponse:
    data = await request.json()
    return JSONResponse([{"assistant_id": AGENTE}] if data.get("graph_id") == AGENTE else [])


async def enviar(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
    if not isinstance(body, dict) or body.get("jsonrpc") != "2.0":
        return JSONResponse({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid request"}})
    respuesta = {"jsonrpc": "2.0", "id": body.get("id")}
    if body.get("method") != "message/send":
        return JSONResponse({**respuesta, "error": {"code": -32601, "message": "Method not found"}})
    try:
        message = body["params"]["message"]
        texto = "\n".join(p["text"] for p in message["parts"] if p.get("kind") == "text").strip()
    except (AttributeError, KeyError, TypeError):
        texto = ""
    if not texto or len(texto) > 4000:
        return JSONResponse({**respuesta, "error": {"code": -32602, "message": "Invalid params"}})
    estado = await graph.ainvoke({"messages": [HumanMessage(content=texto)]})
    return JSONResponse({**respuesta, "result": {
        "kind": "task",
        "id": str(uuid4()),
        "contextId": str(uuid4()),
        "status": {"state": "completed"},
        "artifacts": [{"artifactId": str(uuid4()), "parts": [
            {"kind": "text", "text": estado["messages"][-1].text}
        ]}],
    }})


app = Starlette(routes=[
    Route("/assistants/search", buscar, methods=["POST"]),
    Route(f"/a2a/{AGENTE}", enviar, methods=["POST"]),
])
