"""Carga el texto de un PDF en la base de conocimiento de Supabase."""

import argparse
import re
import time
from pathlib import Path

from google.genai.errors import APIError
from pypdf import PdfReader

from config import settings
from services.rag_supabase import conectar, embeddings


LOTE = 12
PALABRAS_POR_FRAGMENTO = 200
SOLAPAMIENTO = 30


def extraer_fragmentos(pdf: Path) -> list[tuple[int, str]]:
    fragmentos = []
    for pagina, hoja in enumerate(PdfReader(pdf).pages, start=1):
        texto = hoja.extract_text() or ""
        texto = re.sub(r"(?m)^Estudios Económicos CNBV\s*-\s*Vol\. 5, 2023\s*$", "", texto)
        palabras = texto.split()
        paso = PALABRAS_POR_FRAGMENTO - SOLAPAMIENTO
        for inicio in range(0, len(palabras), paso):
            bloque = palabras[inicio:inicio + PALABRAS_POR_FRAGMENTO]
            fragmentos.append((pagina, " ".join(bloque)))
            if inicio + PALABRAS_POR_FRAGMENTO >= len(palabras):
                break
    return fragmentos


def generar_lote(textos: list[str]) -> list[str]:
    for intento in range(3):
        try:
            return embeddings(textos, "RETRIEVAL_DOCUMENT")
        except APIError as exc:
            if exc.code != 429 or intento == 2:
                raise
            espera = 35 if intento == 0 else 60
            print(f"Límite temporal de Gemini. Reintento en {espera} s.", flush=True)
            time.sleep(espera)
    raise RuntimeError("Lote sin respuesta")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Ruta al documento PDF")
    args = parser.parse_args()
    fragmentos = extraer_fragmentos(args.pdf)
    if not fragmentos:
        parser.error("El PDF no contiene texto extraíble.")

    fuente = args.pdf.name
    modelo = settings.embedding_model
    esperados = [(posicion, pagina, texto, modelo)
                 for posicion, (pagina, texto) in enumerate(fragmentos)]
    with conectar() as db:
        anteriores = db.execute("""
            SELECT posicion, pagina, texto, modelo_embedding
            FROM cripto.fragmentos
            WHERE fuente = %s
            ORDER BY posicion
        """, (fuente,)).fetchall()
    if anteriores == esperados:
        print(f"Sin cambios. {len(fragmentos)} fragmentos en Supabase.")
        return

    registros = []
    for inicio in range(0, len(esperados), LOTE):
        lote = esperados[inicio:inicio + LOTE]
        vectores = generar_lote([texto for _, _, texto, _ in lote])
        registros.extend((fuente, *fila, vector) for fila, vector in zip(lote, vectores, strict=True))
        print(f"Embeddings generados: {len(registros)}/{len(esperados)}", flush=True)

    with conectar() as db, db.cursor() as cursor:
        cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (fuente,))
        cursor.execute("DELETE FROM cripto.fragmentos WHERE fuente = %s", (fuente,))
        cursor.executemany("""
            INSERT INTO cripto.fragmentos (fuente, posicion, pagina, texto, modelo_embedding, embedding)
            VALUES (%s, %s, %s, %s, %s, %s::extensions.vector)
        """, registros)
    print(f"Guardados {len(registros)} fragmentos de {len({pagina for pagina, _ in fragmentos})} páginas.")


if __name__ == "__main__":
    main()
