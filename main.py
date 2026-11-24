"""Construcción y ejecución del grafo del asistente de cripto.

main.py SOLO arma el grafo (sin lógica de negocio, que vive en nodes/, tools/,
services/). Expone `graph` como símbolo importable y deja el bucle de consola
dentro de if __name__ == "__main__".

Flujo:
    START -> router -> [conversacion | herramienta | delegacion_a2a | mcp] -> juez -> END

- conversacion: charla general con historial.
- herramienta: ReAct (calcular ganancia, convertir, registrar compra simulada).
- delegacion_a2a: conceptos recuperados por el especialista remoto.
- mcp: precio en vivo desde CoinGecko.

Las cuatro ramas convergen en el juez; ninguna va directo a END.
"""

import argparse

from langgraph.graph import END, START, StateGraph

from nodes.conversacion import conversacion
from nodes.herramienta import herramienta
from nodes.juez import crear_juez
from nodes.mcp import mcp
from nodes.delegacion import delegar_concepto
from nodes.router import router, ruta_desde_estado
from state import AgentState


def build_graph(incluir_juez: bool = True):
    """Construye y compila el grafo completo.

    incluir_juez=False deja el juez como filtro determinista mínimo, útil para
    comparar el comportamiento con y sin el guardrail LLM.
    """
    builder = StateGraph(AgentState)

    builder.add_node("router", router)
    builder.add_node("conversacion", conversacion)
    builder.add_node("herramienta", herramienta)
    builder.add_node("delegacion_a2a", delegar_concepto)
    builder.add_node("mcp", mcp)
    builder.add_node("juez", crear_juez(incluir_juez_llm=incluir_juez))

    builder.add_edge(START, "router")

    # Arista condicional: el router decide la rama.
    builder.add_conditional_edges(
        "router",
        ruta_desde_estado,
        {
            "conversacion": "conversacion",
            "herramienta": "herramienta",
            "rag": "delegacion_a2a",
            "mcp": "mcp",
        },
    )

    # Todas las ramas convergen en el juez.
    builder.add_edge("conversacion", "juez")
    builder.add_edge("herramienta", "juez")
    builder.add_edge("delegacion_a2a", "juez")
    builder.add_edge("mcp", "juez")
    builder.add_edge("juez", END)

    return builder.compile()


# Grafo importable por defecto (con juez), para notebooks y el servidor.
graph = build_graph(incluir_juez=True)


def _run_consola(incluir_juez: bool) -> None:
    """Bucle de consola con historial acumulado entre turnos."""
    historial: list[dict[str, str]] = []
    app = build_graph(incluir_juez=incluir_juez)
    print("Escribe tu mensaje. 'salir' para terminar.")
    while True:
        try:
            user_input = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"salir", "exit", "quit"}:
            break
        if not user_input:
            continue

        estado = {"user_input": user_input, "historial": historial, "trace": [], "permitir_escritura": True}
        resultado = app.invoke(estado)
        respuesta = resultado.get("final_answer", "")
        print(f"Agente: {respuesta}")

        # Se acumula el turno en el historial para el criterio de memoria.
        historial.append({"rol": "user", "texto": user_input})
        historial.append({"rol": "assistant", "texto": respuesta})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chasis agéntico")
    parser.add_argument(
        "--sin-juez",
        action="store_true",
        help="ejecuta sin el juez LLM (solo filtro determinista)",
    )
    args = parser.parse_args()
    _run_consola(incluir_juez=not args.sin_juez)
