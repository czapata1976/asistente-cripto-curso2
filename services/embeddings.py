"""Generación de embeddings con Gemini (compartido por todos los backends).

Los dos backends de recuperación (`rag_local` con SQLite y `rag_supabase` con
pgvector) usan exactamente el mismo modelo y la misma dimensión. Si no fuera
así, los vectores del índice y los de la consulta no serían comparables.

Devuelve listas de `float` en Python puro. Cada backend decide cómo
serializarlas (BLOB en SQLite, literal `vector` en Postgres).
"""

import json
from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


# Dimensión fijada por el esquema (vector(3072) en Postgres y BLOB de 12.288
# bytes en SQLite). Cambiarla exige reconstruir el índice y la migración.
DIMENSIONES = 3072


@lru_cache(maxsize=1)
def cliente_embeddings() -> "genai.Client":
    """Cliente de Gemini reutilizado entre llamadas (evita reconectar)."""
    return genai.Client(api_key=settings.google_api_key, http_options={"timeout": 20000})


def embeddings(textos: list[str], tarea: str) -> list[list[float]]:
    """Genera embeddings para una lista de textos.

    Args:
        textos: fragmentos a vectorizar.
        tarea: "RETRIEVAL_DOCUMENT" al indexar o "RETRIEVAL_QUERY" al consultar.
               Gemini aplica una transformación distinta a cada uno; mezclarlas
               degrada el parecido.
    """
    if not textos:
        return []
    respuesta = cliente_embeddings().models.embed_content(
        model=settings.embedding_model,
        contents=textos,
        config=types.EmbedContentConfig(task_type=tarea, output_dimensionality=DIMENSIONES),
    )
    vectores = [list(vector.values or []) for vector in respuesta.embeddings or []]
    if len(vectores) != len(textos) or any(len(v) != DIMENSIONES for v in vectores):
        raise ValueError("Gemini devolvió embeddings incompletos")
    return vectores


def a_json(vector: list[float]) -> str:
    """Serializa un vector al literal que espera pgvector."""
    return json.dumps(vector, allow_nan=False, separators=(",", ":"))
