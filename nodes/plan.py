"""Nodo del flujo A2A adicional: plan de compra periódica resuelto en n8n.

Reparto de responsabilidades:

1. El LLM del agente principal **interpreta** la petición y extrae parámetros
   (monto, frecuencia, semanas, cripto) con salida estructurada.
2. El especialista en **n8n** recibe el encargo por A2A y **calcula** el plan.
3. El agente principal **usa** el artefacto devuelto para redactar la respuesta.

La redacción final es determinista a partir del artefacto: no se pide al modelo
que "cuente" el plan, para que no pueda alterar las cifras que calculó n8n.
"""

from typing import Literal

from pydantic import BaseModel, Field

from llm import get_llm
from prompts.plan_prompt import PLAN_PROMPT
from services.mensajes import construir_mensajes
from services.n8n_cliente import NOMBRE_ESPECIALISTA_N8N, N8NNoConfigurado, pedir_plan
from state import AgentState


class PlanParams(BaseModel):
    """Parámetros que el plan necesita, ya normalizados."""

    monto_usd: float = Field(gt=0, le=1_000_000, description="Monto por compra, en USD.")
    frecuencia: Literal["semanal", "quincenal", "mensual"] = Field(
        default="semanal", description="Cada cuánto se repite la compra."
    )
    semanas: int = Field(ge=1, le=104, description="Cuántas compras en total.")
    cripto: str = Field(default="bitcoin", max_length=32, description="Criptomoneda objetivo.")


def _redactar(artefacto: dict) -> str:
    """Arma la respuesta con las cifras que devolvió n8n, sin reinterpretarlas."""
    plan = artefacto.get("plan") or []
    primeras = plan[:3]
    lineas = [
        f"Plan de compra periódica para {artefacto.get('cripto')}: "
        f"{artefacto.get('compras')} compras {artefacto.get('frecuencia')}es "
        f"de USD {artefacto.get('monto_usd'):,.2f}.",
        f"Inversión total al final del plan: USD {artefacto.get('total_usd'):,.2f}.",
        "",
        "Primeras compras:",
    ]
    lineas += [
        f"  {fila['numero']}. USD {fila['monto_usd']:,.2f} "
        f"(acumulado USD {fila['acumulado_usd']:,.2f})"
        for fila in primeras
    ]
    if len(plan) > len(primeras):
        lineas.append(f"  … y {len(plan) - len(primeras)} compras más.")
    if artefacto.get("nota"):
        lineas += ["", artefacto["nota"]]
    return "\n".join(lineas)


def plan_dca(state: AgentState) -> dict:
    """Delega el cálculo del plan al especialista n8n y usa su resultado."""
    encargo = state.get("user_input", "")

    try:
        extractor = get_llm().with_structured_output(PlanParams)
        parametros = extractor.invoke(construir_mensajes(PLAN_PROMPT, encargo))
    except Exception:
        return {
            "borrador": (
                "Para armar el plan necesito el monto por compra y durante cuántas "
                "semanas. Por ejemplo: «50 USD semanales durante 12 semanas en bitcoin»."
            ),
            "trace": ["n8n", "parametros_invalidos"],
            "delegacion_n8n": {"agente": NOMBRE_ESPECIALISTA_N8N, "encargo": encargo,
                               "estado": "parametros_invalidos"},
        }

    datos = parametros.model_dump()
    evidencia = {"agente": NOMBRE_ESPECIALISTA_N8N, "encargo": encargo, "parametros": datos}

    try:
        tarea_id, artefacto = pedir_plan(encargo, datos)
    except N8NNoConfigurado as exc:
        # No es un fallo transitorio: el despliegue no tiene planificador. El
        # mensaje lo dice sin prometer un reintento que nunca funcionaría.
        evidencia.update(estado="no_configurado", error=str(exc))
        return {
            "borrador": (
                "El planificador de aportes no está habilitado en este despliegue. "
                "Puedo calcular ganancias, explicar conceptos y consultar precios."
            ),
            "trace": ["n8n", "n8n_no_configurado"],
            "delegacion_n8n": evidencia,
        }
    except Exception as exc:
        evidencia.update(estado="fallo_n8n", error=type(exc).__name__)
        return {
            "borrador": (
                "No pude contactar al planificador. Intenta de nuevo en unos minutos."
            ),
            "trace": ["n8n", "fallo_n8n"],
            "delegacion_n8n": evidencia,
        }

    evidencia.update(estado="completado", tarea_id=tarea_id, artefacto=artefacto)
    return {
        "borrador": _redactar(artefacto),
        "trace": ["n8n", "completado"],
        "delegacion_n8n": evidencia,
    }
