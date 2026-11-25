from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from nodes.rag import rag
from services.contrato_a2a import RespuestaEspecialista


def responder(state: MessagesState) -> dict:
    pregunta = next(
        (mensaje.text for mensaje in reversed(state["messages"])
         if isinstance(mensaje, HumanMessage)),
        "",
    )
    try:
        resultado = rag({"user_input": pregunta})
        fuentes = resultado.get("fuentes_rag", [])
        estado = "respondido" if fuentes and not resultado.get("rag_sin_evidencia") else "sin_evidencia"
        if resultado.get("rag_no_disponible"):
            estado = "no_disponible"
        respuesta = RespuestaEspecialista(
            respuesta=resultado["borrador"], fuentes=fuentes, estado=estado,
            fragmentos=resultado.get("fragmentos_rag", []),
        )
    except Exception:
        respuesta = RespuestaEspecialista(
            respuesta="La guía cripto no está disponible ahora mismo.",
            estado="no_disponible",
        )
    return {"messages": [AIMessage(content=respuesta.model_dump_json())]}


builder = StateGraph(MessagesState)
builder.add_node("consultar_guia", responder)
builder.add_edge(START, "consultar_guia")
builder.add_edge("consultar_guia", END)
graph = builder.compile()
