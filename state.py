"""Estado compartido que circula entre los nodos del grafo.

Es un TypedDict: cada nodo lee y escribe campos de aquí. El campo `trace` usa
un reducer aditivo (operator.add) para acumular la secuencia de nodos sin que
un nodo pise lo que escribió el anterior — esto es lo que pide la pauta para
la trazabilidad y para demostrar el historial.
"""

import operator
from typing import Annotated, Literal, TypedDict


# Ramas que conoce el router del asistente de cripto. Deben coincidir con las
# del router (nodes/router.py) y con el grafo (main.py).
Rama = Literal[
    "conversacion",   # saludos y charla general (no usa herramientas)
    "herramienta",    # ReAct: calcular ganancia, convertir, registrar compra
    "rag",            # conceptos de la guía (qué es una wallet, volatilidad...)
    "mcp",            # precio en vivo desde CoinGecko
    "plan",           # plan de compra periódica resuelto por el especialista n8n
]


class AgentState(TypedDict, total=False):
    """Datos que se pasan entre el router, las ramas y el juez."""

    # --- Entrada e historial ---
    user_input: str
    # Historial: lista de {"rol": "user"|"assistant", "texto": ...}
    historial: list[dict[str, str]]

    # --- Decisión del router ---
    branch: Rama

    permitir_escritura: bool
    delegacion: dict
    delegacion_n8n: dict

    # --- Resultados parciales de cada rama ---
    pasos_react: list[str]   # traza del ciclo ReAct (tool -> observación)
    pasos_mcp: list[str]     # traza de la decisión y llamada al MCP
    fuentes_rag: list[str]   # fuentes citadas por el RAG

    # --- Respuesta ---
    borrador: str            # respuesta antes del juez
    final_answer: str        # respuesta final, ya revisada

    # --- Trazabilidad (reducer aditivo) ---
    trace: Annotated[list[str], operator.add]
