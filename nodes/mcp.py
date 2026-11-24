"""Nodo MCP: precios de cripto en vivo desde CoinGecko (bono de la pauta).

Flujo del nodo:
1. El LLM, con salida estructurada, decide QUÉ criptos consultar a partir del
   mensaje del usuario (descubre la intención y mapea a ids de CoinGecko).
2. Se llama al servidor MCP (herramienta `execute`) para traer el precio real.
3. El LLM redacta la respuesta final usando ESE dato (no inventa precios).

Si el MCP no está configurado o falla, el nodo responde de forma controlada sin
romper el grafo. La pauta pide mostrar la decisión, la llamada real y el uso del
dato en la respuesta: todo eso queda en la traza (pasos_mcp).
"""

import asyncio

from pydantic import BaseModel, Field

from llm import get_llm
from prompts.mcp_prompt import MCP_SYSTEM_PROMPT, MCP_REDACCION_PROMPT
from services.mcp_cliente import precio_en_vivo
from services.mensajes import construir_mensajes, normalizar
from state import AgentState


class CriptosPedidas(BaseModel):
    """Qué criptos consultar, decididas por el LLM a partir del mensaje."""

    ids: list[str] = Field(
        default_factory=list,
        description="ids de CoinGecko mencionadas, ej. ['bitcoin', 'ethereum']. Vacío si no hay ninguna.",
    )


def _decidir_criptos(user_input: str) -> list[str]:
    """El LLM extrae qué criptos quiere el usuario (mapeadas a ids de CoinGecko)."""
    try:
        extractor = get_llm().with_structured_output(CriptosPedidas)
        decision = extractor.invoke(construir_mensajes(MCP_SYSTEM_PROMPT, user_input))
        return [i.strip().lower() for i in decision.ids if i.strip()]
    except Exception:
        return []


def mcp(state: AgentState) -> dict:
    """Consulta precios reales por MCP y redacta la respuesta con ese dato."""
    pregunta = state.get("user_input", "")
    pasos: list[str] = []

    # 1. El LLM decide qué criptos consultar.
    ids = _decidir_criptos(pregunta)
    pasos.append(f"criptos detectadas = {ids or 'ninguna'}")

    if not ids:
        return {
            "borrador": (
                "¿De qué criptomoneda quieres el precio? Por ejemplo Bitcoin o Ethereum."
            ),
            "pasos_mcp": pasos,
            "trace": ["mcp"],
        }

    # 2. Llamada real al servidor MCP.
    try:
        precios = asyncio.run(precio_en_vivo(ids, ["usd", "clp"]))
    except Exception:
        return {
            "borrador": (
                "No pude consultar el precio en vivo ahora mismo."
            ),
            "pasos_mcp": pasos + ["error MCP: consulta no disponible"],
            "trace": ["mcp"],
        }

    pasos.append(f"respuesta MCP = {precios}")

    if not precios:
        return {
            "borrador": "El servidor no devolvió precios para esas criptomonedas.",
            "pasos_mcp": pasos,
            "trace": ["mcp"],
        }

    # 3. El LLM redacta usando SOLO el dato del MCP.
    contexto = f"Datos de CoinGecko (en vivo): {precios}"
    respuesta = get_llm().invoke(
        construir_mensajes(MCP_REDACCION_PROMPT, pregunta, contexto=contexto)
    )
    return {
        "borrador": normalizar(respuesta),
        "pasos_mcp": pasos,
        "trace": ["mcp"],
    }
