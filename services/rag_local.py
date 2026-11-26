"""Índice vectorial local en SQLite: RAG sin servidor de base de datos.

Motivación: el despliegue usa Postgres + pgvector, pero obligar a instalar
Docker o a crear una cuenta de Supabase solo para *probar* el recuperador haría
el proyecto menos reproducible, no más. Este backend guarda los mismos vectores
de 3.072 dimensiones en un archivo SQLite y calcula el parecido coseno en
Python.

Es adecuado para el tamaño del corpus de este proyecto (cientos o pocos miles
de fragmentos): con ~200 fragmentos una consulta tarda milisegundos. Para
millones de vectores habría que usar pgvector o un índice ANN.

El vector se guarda como BLOB de `float32` (3.072 × 4 = 12.288 bytes), no como
texto JSON: `array.frombytes` es mucho más rápido que parsear 3.072 números por
fila en cada consulta.
"""

import sqlite3
from array import array
from contextlib import contextmanager
from math import sqrt

from config import settings
from services.embeddings import DIMENSIONES, embeddings


@contextmanager
def conectar():
    """Abre el índice y garantiza que el esquema exista.

    El `yield` va DENTRO del bloque `with db:`. Si se hace al revés (crear el
    esquema en el bloque y devolver la conexión fuera), sqlite3 cierra sin
    confirmar y las escrituras del llamador se pierden en silencio.
    """
    ruta = settings.rag_sqlite_path
    ruta.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(ruta)
    try:
        db.row_factory = sqlite3.Row
        with db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS fragmentos (
                    fuente          TEXT    NOT NULL,
                    ubicacion       TEXT    NOT NULL,
                    posicion        INTEGER NOT NULL,
                    texto           TEXT    NOT NULL CHECK (length(trim(texto)) > 0),
                    modelo_embedding TEXT,
                    embedding       BLOB    NOT NULL,
                    PRIMARY KEY (fuente, posicion)
                )
            """)
            db.execute("CREATE INDEX IF NOT EXISTS fragmentos_modelo_idx ON fragmentos (modelo_embedding)")
            yield db
    finally:
        db.close()


def _a_blob(vector: list[float]) -> bytes:
    return array("f", vector).tobytes()


def _desde_blob(blob: bytes) -> array:
    vector = array("f")
    vector.frombytes(blob)
    if len(vector) != DIMENSIONES:
        raise ValueError(f"Vector de dimensión {len(vector)}, se esperaba {DIMENSIONES}")
    return vector


def _coseno(a, b) -> float:
    """Parecido coseno. Los embeddings de Gemini no vienen normalizados."""
    producto = norma_a = norma_b = 0.0
    for x, y in zip(a, b):
        producto += x * y
        norma_a += x * x
        norma_b += y * y
    if norma_a <= 0.0 or norma_b <= 0.0:
        return 0.0
    return producto / (sqrt(norma_a) * sqrt(norma_b))


def buscar(pregunta: str, k: int = 3) -> list[dict]:
    """Devuelve los k fragmentos más parecidos a la pregunta.

    Misma forma de salida que el backend de Postgres: lista de dicts con
    `fuente`, `texto` y `parecido`.
    """
    (consulta,) = embeddings([pregunta], "RETRIEVAL_QUERY")
    consulta = array("f", consulta)

    with conectar() as db:
        filas = db.execute(
            "SELECT ubicacion, texto, embedding FROM fragmentos WHERE modelo_embedding = ?",
            (settings.embedding_model,),
        ).fetchall()

    puntuados = [
        {"fuente": fila["ubicacion"], "texto": fila["texto"],
         "parecido": _coseno(consulta, _desde_blob(fila["embedding"]))}
        for fila in filas
    ]
    puntuados.sort(key=lambda f: (-f["parecido"], f["fuente"]))
    return puntuados[:k]


def formatear(fragmentos: list[dict]) -> str:
    """Texto del contexto que se inyecta al LLM, con la fuente de cada trozo."""
    return "\n".join(f"- {f['texto']} [{f['fuente']}]" for f in fragmentos)


def guardar(fuente: str, registros: list[tuple[str, int, str, str | None, bytes]]) -> int:
    """Reemplaza todos los fragmentos de una fuente de forma atómica.

    `registros` viene como (ubicacion, posicion, texto, modelo, blob).
    """
    if not registros:
        return 0
    with conectar() as db:
        db.execute("DELETE FROM fragmentos WHERE fuente = ?", (fuente,))
        db.executemany(
            "INSERT INTO fragmentos (fuente, ubicacion, posicion, texto, modelo_embedding, embedding)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            [(fuente, *registro) for registro in registros],
        )
        return len(registros)


def contar() -> int:
    """Cuántos fragmentos hay indexados (para diagnósticos y pruebas)."""
    with conectar() as db:
        return db.execute("SELECT COUNT(*) FROM fragmentos").fetchone()[0]
