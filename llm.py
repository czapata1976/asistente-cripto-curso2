"""Creación diferida del modelo Gemini.

Se crea el LLM solo cuando un nodo lo necesita (no al importar), para poder
compilar e importar el grafo sin tener credenciales cargadas. Patrón tomado
de seguridad2.0.
"""

from langchain_google_genai import ChatGoogleGenerativeAI

from config import require_llm


def get_llm(temperature: float = 0) -> ChatGoogleGenerativeAI:
    """Devuelve un modelo Gemini listo para invocar.

    temperature=0 por defecto para respuestas deterministas y trazables.
    """
    cfg = require_llm()
    return ChatGoogleGenerativeAI(
        model=cfg.google_model,
        google_api_key=cfg.google_api_key,
        temperature=temperature,
        timeout=20,
        max_retries=0,
    )
