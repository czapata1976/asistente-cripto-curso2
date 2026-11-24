"""Nodo conversacional: responde charla general usando el historial.

Aquí se demuestra el HISTORIAL (criterio obligatorio): el historial se envía
como TURNOS REALES (human/assistant) al LLM, así que en un segundo turno el
agente puede usar un dato del primero (por ejemplo el nombre) sin tenerlo
escrito en el código.
"""

from llm import get_llm
from prompts.conversacion_prompt import CONVERSACION_PROMPT
from services.mensajes import construir_mensajes, normalizar
from state import AgentState


def conversacion(state: AgentState) -> dict:
    """Responde de forma conversacional con memoria del historial."""
    user_input = state.get("user_input", "")
    historial = state.get("historial", [])

    respuesta = get_llm().invoke(
        construir_mensajes(CONVERSACION_PROMPT, user_input, historial=historial)
    )
    return {"borrador": normalizar(respuesta), "trace": ["conversacion"]}
