"""Nodo ReAct: el LLM razona, pide herramientas y decide cuándo parar.

Este nodo implementa el criterio obligatorio de MAYOR peso (1,0) de la pauta:
- El LLM solicita una herramienta (tool_call).
- La observación (resultado de la tool) vuelve al LLM.
- El LLM decide si repite (otra tool) o si responde.
- Hay una condición de parada explícita: MAX_ITERACIONES.

Se implementa "a mano" con bind_tools + un bucle, para que el ciclo ReAct sea
visible y trazable (la pauta pide ver la traza del ciclo).
"""

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from llm import get_llm
from prompts.herramienta_prompt import HERRAMIENTA_PROMPT
from services.mensajes import normalizar
from state import AgentState
from tools.herramientas import TOOLS, TOOLS_POR_NOMBRE


# Condición de parada: nunca más de estas iteraciones de razonamiento.
MAX_ITERACIONES = 5


def herramienta(state: AgentState) -> dict:
    """Ejecuta el ciclo ReAct y devuelve el borrador de respuesta."""
    user_input = state.get("user_input", "")

    # Modelo con las herramientas vinculadas: así puede emitir tool_calls.
    permitir_escritura = state.get("permitir_escritura", False)
    herramientas = [tool for tool in TOOLS
                    if permitir_escritura or tool.name != "registrar_compra_simulada"]
    modelo = get_llm().bind_tools(herramientas)

    prompt = HERRAMIENTA_PROMPT
    if not permitir_escritura:
        prompt += "\nEste servicio es de solo lectura. Indica que el registro de compras está deshabilitado."

    mensajes = [
        SystemMessage(content=prompt),
        HumanMessage(content=user_input),
    ]
    pasos: list[str] = []

    for _ in range(MAX_ITERACIONES):
        respuesta = modelo.invoke(mensajes)
        mensajes.append(respuesta)

        tool_calls = getattr(respuesta, "tool_calls", None) or []
        if not tool_calls:
            # El modelo decidió responder: fin del ciclo.
            pasos.append("respuesta final del LLM (sin más herramientas)")
            return {
                "borrador": normalizar(respuesta),
                "pasos_react": pasos,
                "trace": ["herramienta"],
            }

        # El modelo pidió una o más herramientas: las ejecutamos y devolvemos
        # la observación como ToolMessage para que el LLM razone sobre ella.
        for call in tool_calls:
            nombre = call.get("name", "")
            args = call.get("args", {}) or {}
            tool = TOOLS_POR_NOMBRE.get(nombre)
            if nombre == "registrar_compra_simulada" and not permitir_escritura:
                mensaje = "Acción no autorizada: registro de compras deshabilitado."
                pasos.append(f"tool={nombre} bloqueada antes de ejecutarse")
                return {"borrador": mensaje, "pasos_react": pasos, "trace": ["herramienta", "accion_bloqueada"]}
            if tool is None:
                observacion = f"La herramienta '{nombre}' no existe."
            else:
                try:
                    observacion = str(tool.invoke(args))
                except Exception:
                    observacion = f"Error al ejecutar '{nombre}'."
            pasos.append(f"tool={nombre} args={args} -> {observacion}")
            mensajes.append(
                ToolMessage(content=observacion, tool_call_id=call.get("id", nombre))
            )

    # Se alcanzó la condición de parada sin respuesta final.
    pasos.append("parada por MAX_ITERACIONES")
    return {
        "borrador": (
            "No pude completar la consulta con las herramientas disponibles. "
            "¿Puedes reformular tu pregunta?"
        ),
        "pasos_react": pasos,
        "trace": ["herramienta"],
    }
