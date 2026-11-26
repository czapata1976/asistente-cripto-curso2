"""Nodo RAG: responde conceptos usando la guía cargada en Supabase.

Aplica un umbral de parecido: si el mejor fragmento no lo supera, no llama al
LLM y responde que no tiene la información. Así se cumple la regla de la pauta:
usar RAG solo cuando de verdad hay evidencia en el corpus.
"""

from llm import get_llm
from prompts.rag_prompt import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT
from services.mensajes import normalizar
from services import rag as recuperador
from state import AgentState


# Umbral mínimo de parecido (coseno) para considerar que hay evidencia.
UMBRAL = 0.65
SIN_INFO = "No tengo esa información en el material disponible."


def rag(state: AgentState) -> dict:
    """Recupera fragmentos, aplica umbral y responde citando fuentes."""
    pregunta = state.get("user_input", "")
    try:
        fragmentos = recuperador.buscar(pregunta, k=3)
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
        # La bandera `rag_sin_evidencia` debe quedar marcada aquí también, no
        # solo cuando el LLM responde "no tengo esa información". Si falta,
        # quien consuma el nodo (el especialista o /rag) solo puede deducir el
        # estado por `fuentes` vacías, que es un indicio y no un hecho.
        mejor = fragmentos[0]["parecido"] if fragmentos else None
        return {
            "borrador": SIN_INFO,
            "fuentes_rag": [],
            "rag_sin_evidencia": True,
            "pasos_react": [f"sin evidencia (mejor parecido = {mejor})"],
            "trace": ["rag"],
        }

    contexto = recuperador.formatear(fragmentos)
    fuentes = list(dict.fromkeys(f["fuente"] for f in fragmentos))
    mensajes = [
        ("system", RAG_SYSTEM_PROMPT),
        ("human", RAG_USER_PROMPT.format(contexto=contexto, pregunta=pregunta)),
    ]
    respuesta = normalizar(get_llm().invoke(mensajes))
    sin_evidencia = respuesta.strip().casefold().rstrip(".") == SIN_INFO.casefold().rstrip(".")
    if not sin_evidencia and not any(fuente in respuesta for fuente in fuentes):
        respuesta += "\n\nFuentes consultadas: " + "; ".join(fuentes)
    return {
        "borrador": respuesta,
        "rag_sin_evidencia": sin_evidencia,
        "fragmentos_rag": [
            {
                "fuente": f["fuente"],
                "extracto": f["texto"][:320] + ("…" if len(f["texto"]) > 320 else ""),
                "similitud": round(f["parecido"], 3),
            }
            for f in fragmentos
        ],
        "fuentes_rag": fuentes,
        "pasos_react": [f"fragmentos usados: {fuentes}"],
        "trace": ["rag"],
    }
