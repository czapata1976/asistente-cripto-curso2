"""Recuperación semántica de la guía cripto en Postgres + pgvector.

Backend usado en el despliegue. Para desarrollo local existe `rag_local`, que
guarda los mismos vectores en SQLite y no necesita servidor de base de datos.
El módulo `services.rag` elige uno u otro según `RAG_BACKEND`.
"""
import psycopg
from psycopg.rows import dict_row

from config import settings
from services.embeddings import embeddings, a_json


__all__ = ["buscar", "formatear", "conectar", "embeddings", "guardar"]


def conectar():
    if not settings.supabase_db_url:
        raise RuntimeError("Configura SUPABASE_DB_URL")
    return psycopg.connect(
        settings.supabase_db_url, connect_timeout=6, prepare_threshold=None,
    )


def buscar(pregunta: str, k: int = 3) -> list[dict]:
    (consulta,) = embeddings([pregunta], "RETRIEVAL_QUERY")
    vector = a_json(consulta)
    with conectar() as db, db.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SET LOCAL statement_timeout = '6s'")
        cursor.execute("""
            SELECT COALESCE(
                       ubicacion,
                       CASE WHEN pagina IS NOT NULL
                            THEN CONCAT(fuente, ', p. ', pagina)
                            ELSE CONCAT(fuente, ' (fragmento ', posicion + 1, ')')
                       END
                   ) AS fuente, texto,
                   1 - (embedding OPERATOR(extensions.<=>) %s::extensions.vector) AS parecido
            FROM cripto.fragmentos
            WHERE modelo_embedding = %s
            ORDER BY parecido DESC, fuente, posicion
            LIMIT %s
        """, (vector, settings.embedding_model, k))
        return cursor.fetchall()


def guardar(fuente: str, registros: list[tuple[str, int, str, str | None, str]]) -> int:
    """Reemplaza los fragmentos de una fuente de forma atómica.

    `registros` viene como (ubicacion, posicion, texto, modelo, vector_json),
    la misma forma que usa el backend SQLite. El bloqueo consultivo evita que
    dos cargas simultáneas se pisen a mitad de camino.
    """
    if not registros:
        return 0
    filas = [(fuente, *registro) for registro in registros]
    with conectar() as db, db.cursor() as cursor:
        cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (fuente,))
        cursor.execute("DELETE FROM cripto.fragmentos WHERE fuente = %s", (fuente,))
        cursor.executemany("""
            INSERT INTO cripto.fragmentos
                (fuente, ubicacion, posicion, texto, modelo_embedding, embedding)
            VALUES (%s, %s, %s, %s, %s, %s::extensions.vector)
        """, filas)
        return len(registros)


def formatear(fragmentos: list[dict]) -> str:
    return "\n".join(f"- {f['texto']} [{f['fuente']}]" for f in fragmentos)
