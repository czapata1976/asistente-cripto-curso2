"""Nodo RAG: responde conceptos usando la guía cargada en el Redis del curso.

Aplica un umbral de parecido: si el mejor fragmento no lo supera, no llama al
LLM y responde que no tiene la información. Así se cumple la regla de la pauta:
usar RAG solo cuando de verdad hay evidencia en el corpus.
"""

from llm import get_llm
from prompts.rag_prompt import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT
from services.mensajes import normalizar
from services import rag_redis
from state import AgentState


# Umbral mínimo de parecido (coseno) para considerar que hay evidencia.
UMBRAL = 0.65
SIN_INFO = "No tengo esa información en el material disponible."


def rag(state: AgentState) -> dict:
    """Recupera fragmentos, aplica umbral y responde citando fuentes."""
    pregunta = state.get("user_input", "")
    try:
        fragmentos = rag_redis.buscar(pregunta, k=3)
    except Exception:
        return {
            "borrador": (
                "La guía cripto no está disponible ahora mismo."
            ),
            "pasos_react": ["material no disponible"],
            "trace": ["rag"],
            "rag_no_disponible": True,
        }

    if not fragmentos or fragmentos[0]["parecido"] < UMBRAL:
        # Sin evidencia suficiente: no se llama al LLM.
        mejor = fragmentos[0]["parecido"] if fragmentos else None
        return {
            "borrador": SIN_INFO,
            "fuentes_rag": [],
            "pasos_react": [f"sin evidencia (mejor parecido = {mejor})"],
            "trace": ["rag"],
        }

    contexto = rag_redis.formatear(fragmentos)
    fuentes = [f["fuente"] for f in fragmentos]
    mensajes = [
        ("system", RAG_SYSTEM_PROMPT),
        ("human", RAG_USER_PROMPT.format(contexto=contexto, pregunta=pregunta)),
    ]
    respuesta = get_llm().invoke(mensajes)
    return {
        "borrador": normalizar(respuesta),
        "fuentes_rag": fuentes,
        "pasos_react": [f"fragmentos usados: {fuentes}"],
        "trace": ["rag"],
    }
