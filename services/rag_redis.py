"""Servicio RAG sobre el Redis del curso (bono).

El corpus (el ebook "criptomonedas-desde-cero.md") ya está cargado en Redis en la
base "<REDIS_PREFIJO>:ebook_cripto", con el esquema del Taller 2: cada fragmento
es un hash con los campos "texto", "fuente" y "vector" (lista JSON). Aquí SOLO se
consulta (retrieval): no se sube ni se modifica nada en Redis.

Para que sea rápido, los vectores se cargan UNA vez en una matriz NumPy (cacheada)
y la búsqueda es un producto matriz-vector (todos los cosenos de golpe), en vez de
recorrer fragmento por fragmento en Python puro.

Configuración declarada (para la pauta):
- Embeddings: Google "gemini-embedding-001" (3072 dimensiones).
- Campos del fragmento: "texto", "fuente", "vector" (JSON).
- Métrica: similitud coseno.
- Base: "<REDIS_PREFIJO>:ebook_cripto".

Requiere: redis, numpy y langchain-google-genai. La carga/ingesta del corpus se
hace por separado (ver el notebook de ingesta del Taller 3).
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from config import settings


# --- Parámetros declarados ---------------------------------------------------

MODELO_EMBEDDINGS = "models/gemini-embedding-001"
DIMENSIONES = 3072
METRICA = "coseno"


def _base() -> str:
    """Base (subcarpeta) de Redis donde está el ebook."""
    return f"{settings.redis_prefijo}:ebook_cripto"


# --- Conexiones perezosas ----------------------------------------------------


@lru_cache(maxsize=1)
def _get_redis():
    """Conexión perezosa a Redis (una sola vez)."""
    if not settings.redis_url:
        raise RuntimeError("REDIS_URL no está configurada en el .env")
    import redis

    return redis.Redis.from_url(
        settings.redis_url, decode_responses=True, socket_connect_timeout=8, socket_timeout=8
    )


@lru_cache(maxsize=1)
def _get_embedder():
    """Modelo de embeddings de Gemini (una sola vez)."""
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    return GoogleGenerativeAIEmbeddings(model=MODELO_EMBEDDINGS)


@lru_cache(maxsize=1)
def _cargar_matriz():
    """Lee TODOS los fragmentos de Redis UNA vez y arma la matriz de vectores
    (NumPy, normalizada). Se cachea: las siguientes búsquedas no vuelven a Redis.
    """
    r = _get_redis()
    base = _base()
    ids = sorted(r.smembers(f"{base}:fragmentos"), key=lambda x: int(x))

    pipe = r.pipeline()
    for i in ids:
        pipe.hgetall(f"{base}:fragmento:{i}")

    textos: list[str] = []
    fuentes: list[str] = []
    vectores: list[list[float]] = []
    for h in pipe.execute():
        if not h:
            continue
        textos.append(h.get("texto", ""))
        fuentes.append(h.get("fuente", ""))
        vectores.append(json.loads(h["vector"]))

    if not textos:
        return textos, fuentes, None

    import numpy as np

    M = np.asarray(vectores, dtype=np.float32)
    normas = np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    M = M / normas  # cada fila normalizada: el coseno es un producto punto
    return textos, fuentes, M


# --- Búsqueda (retrieval) ----------------------------------------------------


def buscar(pregunta: str, k: int = 3) -> list[dict[str, Any]]:
    """Devuelve los k fragmentos más parecidos del ebook (coseno vectorizado).

    Cada fragmento es {texto, fuente, parecido}, ordenados de mayor a menor
    parecido. Lanza excepción si Redis o los embeddings no están disponibles;
    el nodo que llama debe capturarla.
    """
    textos, fuentes, M = _cargar_matriz()
    if not textos:
        return []

    import numpy as np

    q = np.asarray(_get_embedder().embed_query(pregunta), dtype=np.float32)
    q = q / (np.linalg.norm(q) + 1e-9)
    sims = M @ q                       # un producto matriz-vector = todos los cosenos
    idx = np.argsort(-sims)[:k]        # los k más altos
    return [
        {"texto": textos[j], "fuente": fuentes[j], "parecido": round(float(sims[j]), 3)}
        for j in idx
    ]


def formatear(fragmentos: list[dict[str, Any]]) -> str:
    """Convierte los fragmentos en texto con sus fuentes, para el prompt."""
    return "\n".join(f"- {f['texto']} [{f['fuente']}]" for f in fragmentos)
