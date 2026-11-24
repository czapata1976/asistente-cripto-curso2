"""Herramientas del asistente de cripto (ReAct).

Estas son las tools LOCALES que el LLM puede llamar en el ciclo ReAct. Se
declaran con @tool y se agrupan en TOOLS para vincularlas con
llm.bind_tools(TOOLS).

- calcular_ganancia: cálculo determinista de ganancia/pérdida de una posición.
- convertir_a_pesos: conversión USD -> CLP con una tasa fija y declarada.
- registrar_compra_simulada: ACCIÓN (bono +0,5). Escribe en un portafolio de
  prueba (archivo JSON) y devuelve el estado anterior y posterior.

El precio en vivo NO está aquí: eso lo entrega el servidor MCP de CoinGecko
(ver nodes/mcp.py), porque la pauta exige que el dato externo venga de un MCP.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.tools import tool


# --- Configuración declarada (datos de prueba, reproducibles) ---------------

# Tasa de cambio fija y DECLARADA. No es un precio en vivo: es un supuesto del
# ejercicio para que el cálculo sea determinista y comprobable. El precio real
# de las criptos se obtiene por MCP.
TASA_USD_CLP = 950.0

# Portafolio de prueba: archivo local junto a este proyecto. No contiene datos
# reales ni dinero real; es un registro simulado para demostrar la acción.
PORTAFOLIO_PATH = Path(__file__).resolve().parent.parent / "datos" / "portafolio.json"


# --- Herramientas de cálculo (ReAct) ----------------------------------------


@tool
def calcular_ganancia(cantidad: float, precio_compra: float, precio_actual: float) -> str:
    """Calcula la ganancia o pérdida de una posición en cripto.

    Úsala cuando la persona diga cuánto compró, a qué precio y quiera saber su
    resultado. Los precios van en la misma moneda (por ejemplo USD).

    Args:
        cantidad: unidades de la cripto (ej. 0.5).
        precio_compra: precio al que compró cada unidad.
        precio_actual: precio actual de cada unidad.
    """
    invertido = cantidad * precio_compra
    valor_actual = cantidad * precio_actual
    ganancia = valor_actual - invertido
    pct = (ganancia / invertido * 100) if invertido else 0.0
    signo = "ganancia" if ganancia >= 0 else "pérdida"
    return (
        f"Invertido: {invertido:,.2f} | Valor actual: {valor_actual:,.2f} | "
        f"{signo.capitalize()}: {ganancia:,.2f} ({pct:+.2f}%)."
    )


@tool
def convertir_a_pesos(monto_usd: float) -> str:
    """Convierte un monto en dólares (USD) a pesos chilenos (CLP).

    Usa una tasa fija y declarada (950 CLP por USD). Úsala cuando la persona
    pida pasar un valor en dólares a pesos.
    """
    clp = monto_usd * TASA_USD_CLP
    return f"{monto_usd:,.2f} USD equivalen a {clp:,.0f} CLP (tasa fija: {TASA_USD_CLP:,.0f} CLP/USD)."


# --- Herramienta de acción (bono +0,5) --------------------------------------


def _leer_portafolio() -> list[dict]:
    """Lee el portafolio simulado; si no existe, devuelve una lista vacía."""
    if not PORTAFOLIO_PATH.exists():
        return []
    try:
        return json.loads(PORTAFOLIO_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


@tool
def registrar_compra_simulada(cripto: str, cantidad: float, precio_usd: float) -> str:
    """Registra una compra SIMULADA en un portafolio de práctica (no es real).

    Es una acción: modifica un archivo local y devuelve el estado anterior y el
    posterior. Úsala solo cuando la persona pida anotar o registrar una compra
    de práctica. No implica dinero real ni ninguna recomendación.

    Args:
        cripto: nombre de la cripto (ej. "bitcoin").
        cantidad: unidades compradas.
        precio_usd: precio pagado por unidad, en USD.
    """
    antes = _leer_portafolio()
    movimiento = {
        "cripto": cripto.strip().lower(),
        "cantidad": cantidad,
        "precio_usd": precio_usd,
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    despues = antes + [movimiento]

    PORTAFOLIO_PATH.parent.mkdir(parents=True, exist_ok=True)
    PORTAFOLIO_PATH.write_text(
        json.dumps(despues, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return (
        f"Compra simulada registrada.\n"
        f"ANTES: {len(antes)} movimiento(s).\n"
        f"DESPUÉS: {len(despues)} movimiento(s). "
        f"Último: {movimiento['cantidad']} {movimiento['cripto']} a {movimiento['precio_usd']:,.2f} USD."
    )


# --- Registro de herramientas -----------------------------------------------

# Lista que se vincula al modelo en el nodo ReAct.
TOOLS = [calcular_ganancia, convertir_a_pesos, registrar_compra_simulada]

# Índice por nombre, para ejecutar la tool que pidió el modelo.
TOOLS_POR_NOMBRE = {t.name: t for t in TOOLS}
