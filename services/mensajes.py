"""Construcción de mensajes para el LLM.

Regla de oro de seguridad (del PDF "Evaluar y proteger"): las reglas van en el
mensaje `system` y la entrada del usuario va en su propio mensaje `human`.
Nunca se pega el texto del usuario dentro del system, porque entonces el modelo
lo leería con la misma autoridad que las reglas.
"""

from langchain_core.messages import AIMessage, BaseMessage


def construir_mensajes(
    system_prompt: str,
    user_text: str,
    contexto: str = "",
    historial: list[dict[str, str]] | None = None,
) -> list[tuple[str, str]]:
    """Devuelve la lista de mensajes para el LLM.

    - El `system_prompt` lleva las reglas.
    - El `historial`, si viene, se agrega como TURNOS REALES (human/assistant),
      no como texto dentro del human. Así el modelo lo trata como la
      conversación previa y puede usar un dato del primer turno en el segundo
      (criterio de historial de la pauta).
    - El `contexto` extra (fragmentos RAG, dato de una tool o del MCP) va dentro
      del mensaje human final, entre etiquetas, nunca en el system.
    """
    mensajes: list[tuple[str, str]] = [("system", system_prompt)]

    for h in (historial or []):
        rol = "assistant" if h.get("rol") == "assistant" else "human"
        mensajes.append((rol, h.get("texto", "")))

    if contexto:
        human = f"<contexto>\n{contexto}\n</contexto>\n\n<mensaje>\n{user_text}\n</mensaje>"
    else:
        human = user_text
    mensajes.append(("human", human))
    return mensajes


def normalizar(value) -> str:
    """Extrae texto plano de la respuesta del LLM de forma defensiva.

    Los AIMessage pueden traer content como lista de bloques con metadatos
    (firmas, etc.). Aquí nos quedamos solo con el texto y descartamos el resto,
    para que la respuesta final nunca exponga la representación interna.
    """
    try:
        if value is None:
            return ""
        if isinstance(value, AIMessage):
            texto = getattr(value, "text", None)
            if isinstance(texto, str) and texto:
                return texto
            return normalizar(value.content)
        if isinstance(value, BaseMessage):
            return normalizar(value.content)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            if isinstance(value.get("text"), str):
                return value["text"]
            if "content" in value:
                return normalizar(value["content"])
            return ""
        if isinstance(value, list):
            partes = []
            for item in value:
                if isinstance(item, str):
                    partes.append(item)
                elif (
                    isinstance(item, dict)
                    and item.get("type") == "text"
                    and isinstance(item.get("text"), str)
                ):
                    partes.append(item["text"])
            return "\n\n".join(partes)
    except Exception:
        return ""
    return ""
