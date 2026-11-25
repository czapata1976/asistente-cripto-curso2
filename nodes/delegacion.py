import httpx
from google.auth.exceptions import GoogleAuthError

from services.a2a_cliente import NOMBRE_ESPECIALISTA, consultar_especialista
from state import AgentState


def delegar_concepto(state: AgentState) -> dict:
    pregunta = state["user_input"]
    evidencia = {"agente": NOMBRE_ESPECIALISTA, "encargo": pregunta}
    try:
        tarea_id, resultado = consultar_especialista(pregunta)
    except (GoogleAuthError, httpx.HTTPError, ValueError, KeyError, IndexError, TypeError):
        evidencia["estado"] = "fallo_a2a"
        return {
            "borrador": "No pude consultar al especialista cripto. Intenta nuevamente más tarde.",
            "delegacion": evidencia,
            "trace": ["delegacion_a2a", "fallo_a2a"],
        }

    evidencia.update(resultado.model_dump(), tarea_id=tarea_id)
    return {
        "borrador": resultado.respuesta,
        "fuentes_rag": resultado.fuentes,
        "delegacion": evidencia,
        "trace": ["delegacion_a2a", resultado.estado],
    }
