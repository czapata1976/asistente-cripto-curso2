"""Nodo juez: guardrail final (bono) + red de seguridad determinista.

Todas las ramas pasan por aquí antes de END. Hace dos cosas:
1. Un filtro determinista en código: si el borrador se parece a una clave o
   expone configuración, lo bloquea sin depender del LLM.
2. Un juez LLM que revisa el contenido y puede corregir o reemplazar la
   respuesta.

Se puede desactivar el juez LLM (INCLUIR_JUEZ_LLM=False) para comparar el
"antes y después", como sugiere el material del curso.
"""

import re

from llm import get_llm
from prompts.juez_prompt import JUEZ_PROMPT
from services.mensajes import construir_mensajes, normalizar
from state import AgentState


# Patrones deterministas que nunca deberían salir en una respuesta.
_PATRONES_PROHIBIDOS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),          # claves de Google
    re.compile(r"sk-[0-9A-Za-z]{20,}"),               # claves estilo OpenAI
    re.compile(r"GOOGLE_API_KEY", re.IGNORECASE),
    re.compile(r"SUPABASE_DB_URL", re.IGNORECASE),
]

MENSAJE_SEGURO = (
    "No puedo compartir esa información. ¿Puedo ayudarte con algo dentro de mi alcance?"
)


def _tiene_contenido_prohibido(texto: str) -> bool:
    return any(p.search(texto) for p in _PATRONES_PROHIBIDOS)


def crear_juez(incluir_juez_llm: bool = True):
    """Devuelve el nodo juez. Si incluir_juez_llm=False, solo aplica el filtro
    determinista (útil para comparar con/sin juez)."""

    def juez(state: AgentState) -> dict:
        borrador = state.get("borrador", "")

        # 1. Filtro determinista: bloquea secretos aunque el LLM fallara.
        if _tiene_contenido_prohibido(borrador):
            return {"final_answer": MENSAJE_SEGURO, "trace": ["juez"]}

        delegacion = state.get("delegacion", {})
        if (
            not incluir_juez_llm
            or delegacion.get("estado") in {"fallo_a2a", "no_disponible", "sin_evidencia"}
            or "accion_bloqueada" in state.get("trace", [])
        ):
            return {"final_answer": borrador, "trace": ["juez"]}

        # 2. Juez LLM: revisa contenido y puede corregir/reemplazar.
        try:
            revisado = get_llm().invoke(
                construir_mensajes(JUEZ_PROMPT, state.get("user_input", ""), contexto=borrador)
            )
            final = normalizar(revisado) or borrador
        except Exception:
            final = borrador

        # Segunda pasada determinista por si el juez dejó pasar algo.
        if _tiene_contenido_prohibido(final):
            final = MENSAJE_SEGURO
        elif delegacion.get("estado") == "respondido":
            fuentes = state.get("fuentes_rag", [])
            if fuentes and not any(fuente in final for fuente in fuentes):
                final += "\n\nFuentes consultadas: " + "; ".join(fuentes)
        return {"final_answer": final, "trace": ["juez"]}

    return juez
