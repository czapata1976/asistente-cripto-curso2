"""Nodo router: clasifica la intención y elige la rama (workflow, bono)."""

from typing import Literal

from pydantic import BaseModel, Field

from llm import get_llm
from prompts.router_prompt import ROUTER_PROMPT
from services.mensajes import construir_mensajes
from state import AgentState


class Decision(BaseModel):
    """Salida estructurada y cerrada del router."""

    # TODO (adaptar): estas etiquetas deben coincidir con state.Rama y el grafo.
    branch: Literal["conversacion", "herramienta", "rag", "mcp", "plan"] = Field(
        description="Rama que debe atender el mensaje del usuario."
    )


def router(state: AgentState) -> dict:
    """Decide la rama con salida estructurada; si falla, cae a conversacion."""
    user_input = state.get("user_input", "")
    try:
        clasificador = get_llm().with_structured_output(Decision)
        decision = clasificador.invoke(
            construir_mensajes(ROUTER_PROMPT, user_input)
        )
        branch = decision.branch
    except Exception:
        branch = "conversacion"
    return {"branch": branch, "trace": ["router"]}


def ruta_desde_estado(state: AgentState) -> str:
    """Devuelve la etiqueta para la arista condicional del grafo."""
    return state.get("branch", "conversacion")
