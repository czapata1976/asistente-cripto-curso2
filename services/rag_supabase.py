"""Recuperación semántica de la guía cripto en Supabase."""
import json
from functools import lru_cache

import psycopg
from google import genai
from google.genai import types
from psycopg.rows import dict_row

from config import settings


@lru_cache(maxsize=1)
def cliente_embeddings():
    return genai.Client(api_key=settings.google_api_key, http_options={"timeout": 20000})


def embeddings(textos: list[str], tarea: str) -> list[str]:
    respuesta = cliente_embeddings().models.embed_content(
        model=settings.embedding_model,
        contents=textos,
        config=types.EmbedContentConfig(task_type=tarea, output_dimensionality=3072),
    )
    vectores = [vector.values for vector in respuesta.embeddings or []]
    if len(vectores) != len(textos) or any(len(v or []) != 3072 for v in vectores):
        raise ValueError("Gemini devolvió embeddings incompletos")
    return [json.dumps(vector, allow_nan=False, separators=(",", ":")) for vector in vectores]


def conectar():
    if not settings.supabase_db_url:
        raise RuntimeError("Configura SUPABASE_DB_URL")
    return psycopg.connect(
        settings.supabase_db_url, connect_timeout=6, prepare_threshold=None,
    )


def buscar(pregunta: str, k: int = 3) -> list[dict]:
    (vector,) = embeddings([pregunta], "RETRIEVAL_QUERY")
    with conectar() as db, db.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SET LOCAL statement_timeout = '6s'")
        cursor.execute("""
            SELECT CASE WHEN pagina IS NOT NULL
                       THEN CONCAT(fuente, ', p. ', pagina)
                       ELSE CONCAT(fuente, ' (fragmento ', posicion + 1, ')')
                   END AS fuente, texto,
                   1 - (embedding OPERATOR(extensions.<=>) %s::extensions.vector) AS parecido
            FROM cripto.fragmentos
            WHERE modelo_embedding = %s
            ORDER BY parecido DESC, fuente, posicion
            LIMIT %s
        """, (vector, settings.embedding_model, k))
        return cursor.fetchall()


def formatear(fragmentos: list[dict]) -> str:
    return "\n".join(f"- {f['texto']} [{f['fuente']}]" for f in fragmentos)
