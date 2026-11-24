"""Cliente MCP para CoinGecko (bono de la pauta).

Conecta al servidor MCP oficial y gratuito de CoinGecko por HTTP (streamable)
y expone dos ayudas:

- get_mcp_tools(): descubre las herramientas del servidor (para demostrar el
  "descubrimiento" que pide la pauta).
- precio_en_vivo(ids, monedas): obtiene precios reales llamando a la herramienta
  `execute` del servidor con un código fijo y seguro.

El servidor CoinGecko expone 2 herramientas:
  - execute: corre código TypeScript contra un SDK ya inicializado (`client`).
  - search_docs: busca en la documentación del SDK.
No hay una tool directa "dame el precio", por eso envolvemos `execute` con un
código fijo. Así el dato viene del MCP (como exige la pauta) y la llamada es
estable y reproducible, sin depender de que el LLM escriba TypeScript correcto.

Requiere langchain-mcp-adapters y MCP_URL en el .env.
"""

import json

from config import settings


def _crear_cliente():
    """Crea el cliente MCP apuntando al servidor configurado en MCP_URL."""
    from langchain_mcp_adapters.client import MultiServerMCPClient

    if not settings.mcp_url:
        raise RuntimeError("MCP_URL no está configurada en el .env")

    return MultiServerMCPClient(
        {
            "coingecko": {
                "transport": "streamable_http",
                "url": settings.mcp_url,
            }
        }
    )


async def get_mcp_tools():
    """Descubre y devuelve la lista de herramientas del servidor MCP."""
    client = _crear_cliente()
    return await client.get_tools()


# Código TypeScript FIJO que corre dentro del servidor CoinGecko. Pide el precio
# simple de una o varias criptos en una o varias monedas. No recibe entrada del
# usuario sin validar: los ids y monedas se arman en Python más abajo.
_PLANTILLA_CODIGO = """async function run(client) {{
  return await client.simple.price.get({{ vs_currencies: '{monedas}', ids: '{ids}' }});
}}"""


def _sanear(valores: list[str]) -> str:
    """Deja solo ids/monedas simples (letras, números y guiones), separados por coma."""
    limpios = []
    for v in valores:
        v = "".join(c for c in v.strip().lower() if c.isalnum() or c in "-")
        if v:
            limpios.append(v)
    return ",".join(limpios)


async def precio_en_vivo(ids: list[str], monedas: list[str] | None = None) -> dict:
    """Devuelve el precio real de las criptos indicadas usando el MCP.

    Args:
        ids: ids de CoinGecko (ej. ["bitcoin", "ethereum"]).
        monedas: monedas de referencia (por defecto ["usd", "clp"]).

    Returns:
        dict con la respuesta de CoinGecko, por ejemplo:
        {"bitcoin": {"usd": 84790, "clp": 84020459}}
    """
    monedas = monedas or ["usd", "clp"]
    ids_str = _sanear(ids)
    monedas_str = _sanear(monedas)
    if not ids_str:
        return {}

    codigo = _PLANTILLA_CODIGO.format(ids=ids_str, monedas=monedas_str)

    client = _crear_cliente()
    tools = {t.name: t for t in await client.get_tools()}
    if "execute" not in tools:
        raise RuntimeError("El servidor MCP no expone la herramienta 'execute'.")

    salida = await tools["execute"].ainvoke(
        {"code": codigo, "intent": "consultar precio simple de criptomonedas"}
    )
    return _extraer_json(salida)


def _extraer_json(salida) -> dict:
    """Extrae el JSON de precios de la respuesta del MCP (lista de bloques)."""
    texto = ""
    if isinstance(salida, list):
        for bloque in salida:
            if isinstance(bloque, dict) and bloque.get("type") == "text":
                texto += bloque.get("text", "")
    elif isinstance(salida, str):
        texto = salida
    else:
        texto = str(salida)

    try:
        data = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    # CoinGecko devuelve {"result": {...}} dentro del execute.
    return data.get("result", data) if isinstance(data, dict) else {}
