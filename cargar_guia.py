"""Carga el corpus del RAG en el backend configurado.

Reemplaza a `cargar_guia_supabase.py` y añade dos capacidades que hacían falta
para que el proyecto sea reproducible:

1. **Markdown además de PDF.** El corpus real de este proyecto es
   `criptomonedas-desde-cero.md`, que está versionado en el repositorio. Antes
   había que conseguir un PDF externo para poder reconstruir el índice.
2. **Backend seleccionable.** `RAG_BACKEND=sqlite` indexa en un archivo local;
   `RAG_BACKEND=postgres` indexa en pgvector. El chunking y los embeddings son
   idénticos, así que el índice es equivalente.

Uso:
    python cargar_guia.py                      # usa RAG_CORPUS del .env
    python cargar_guia.py ruta/al/manual.md
    python cargar_guia.py manual.pdf
    python cargar_guia.py --revisar            # solo cuenta, no indexa
"""

import argparse
import re
import sys
import time
from pathlib import Path

from google.genai.errors import APIError

from config import settings
from services.embeddings import embeddings

# Parámetros de chunking. 200 palabras con 30 de solape mantiene continuidad
# entre trozos sin inflar el índice.
PALABRAS_POR_FRAGMENTO = 200
SOLAPAMIENTO = 30
# Secciones del Markdown más cortas que esto se descartan: suelen ser títulos
# sueltos o notas de una línea que ensucian la recuperación.
MINIMO_PALABRAS = 25
# Gemini limita las peticiones por minuto; lotes pequeños evitan el 429.
LOTE = 12


def _trozos(palabras: list[str]) -> list[str]:
    """Parte una lista de palabras en fragmentos con solapamiento."""
    if not palabras:
        return []
    paso = PALABRAS_POR_FRAGMENTO - SOLAPAMIENTO
    trozos = []
    for inicio in range(0, len(palabras), paso):
        bloque = palabras[inicio:inicio + PALABRAS_POR_FRAGMENTO]
        if bloque:
            trozos.append(" ".join(bloque))
        if inicio + PALABRAS_POR_FRAGMENTO >= len(palabras):
            break
    return trozos


def fragmentos_pdf(ruta: Path) -> list[tuple[str, str]]:
    """Extrae fragmentos por página de un PDF: [(ubicacion, texto)]."""
    from pypdf import PdfReader

    resultado = []
    for pagina, hoja in enumerate(PdfReader(ruta).pages, start=1):
        texto = re.sub(
            r"(?m)^Estudios Económicos CNBV\s*-\s*Vol\. 5, 2023\s*$", "",
            hoja.extract_text() or "",
        )
        for trozo in _trozos(texto.split()):
            resultado.append((f"{ruta.name}, p. {pagina}", trozo))
    return resultado


def fragmentos_markdown(ruta: Path) -> list[tuple[str, str]]:
    """Extrae fragmentos por sección de un Markdown: [(ubicacion, texto)].

    Cada sección de nivel 2 (`## `) se convierte en la unidad de cita. Así la
    respuesta puede decir "criptomonedas-desde-cero.md, §8 — Stablecoins" en
    lugar de una página que el Markdown no tiene.
    """
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    secciones: list[tuple[str, list[str]]] = []
    titulo_actual, buffer = "Introducción", []

    for linea in lineas:
        encabezado = re.match(r"^(#{1,3})\s+(.*)$", linea)
        # Solo los niveles 2 y 3 abren sección: el título del documento (#) y
        # los apartados menores no son buenas unidades de cita.
        if encabezado and len(encabezado.group(1)) in (2, 3):
            secciones.append((titulo_actual, buffer))
            titulo_actual, buffer = encabezado.group(2).strip(), []
        else:
            buffer.append(linea)
    secciones.append((titulo_actual, buffer))

    resultado = []
    for numero, (titulo, cuerpo) in enumerate(secciones, start=1):
        palabras = " ".join(cuerpo).split()
        if len(palabras) < MINIMO_PALABRAS:
            continue
        ubicacion = f"{ruta.name}, §{numero} — {titulo}"
        for trozo in _trozos(palabras):
            resultado.append((ubicacion, trozo))
    return resultado


def extraer_fragmentos(ruta: Path) -> list[tuple[str, str]]:
    """Elige el extractor según la extensión del archivo."""
    if ruta.suffix.lower() in {".md", ".markdown", ".txt"}:
        return fragmentos_markdown(ruta)
    if ruta.suffix.lower() == ".pdf":
        return fragmentos_pdf(ruta)
    raise ValueError(f"Formato no soportado: {ruta.suffix}")


def generar_lote(textos: list[str]) -> list[list[float]]:
    """Genera embeddings de un lote reintentando ante el límite de cuota."""
    for intento in range(3):
        try:
            return embeddings(textos, "RETRIEVAL_DOCUMENT")
        except APIError as exc:
            if getattr(exc, "code", None) != 429 or intento == 2:
                raise
            espera = 35 if intento == 0 else 60
            print(f"  Límite temporal de Gemini. Reintento en {espera} s.", flush=True)
            time.sleep(espera)
    raise RuntimeError("Lote sin respuesta")


def _backend():
    """Importa el backend activo y su serializador de vectores."""
    if settings.rag_backend == "postgres":
        from services import rag_supabase as backend
        from services.embeddings import a_json
        return backend, lambda vector: a_json(vector)
    from services import rag_local as backend
    from array import array
    return backend, lambda vector: array("f", vector).tobytes()


def indexar(corpus: Path, verboso: bool = True) -> int:
    """Genera los embeddings del corpus y reemplaza el índice. Devuelve el total.

    Args:
        corpus: documento a indexar.
        verboso: imprime el progreso. Se apaga cuando la indexación es
                 automática al arrancar el servicio.
    """
    def avisar(mensaje: str) -> None:
        if verboso:
            print(mensaje, flush=True)

    fragmentos = extraer_fragmentos(corpus)
    if not fragmentos:
        raise ValueError("El documento no contiene texto aprovechable.")
    if not settings.google_api_key:
        raise RuntimeError("Falta GOOGLE_API_KEY: sin ella no se generan vectores.")

    avisar(f"Corpus: {corpus.name}")
    avisar(f"Fragmentos: {len(fragmentos)} en "
           f"{len({ubicacion for ubicacion, _ in fragmentos})} secciones")

    backend, serializar = _backend()
    modelo = settings.embedding_model
    registros = []
    for inicio in range(0, len(fragmentos), LOTE):
        lote = fragmentos[inicio:inicio + LOTE]
        vectores = generar_lote([texto for _, texto in lote])
        registros.extend(
            (ubicacion, inicio + i, texto, modelo, serializar(vector))
            for i, ((ubicacion, texto), vector) in enumerate(zip(lote, vectores, strict=True))
        )
        avisar(f"  Embeddings generados: {len(registros)}/{len(fragmentos)}")

    return backend.guardar(corpus.name, registros)


def asegurar_indice() -> int | None:
    """Indexa el corpus si el backend local está vacío.

    Pensado para el despliegue: el índice SQLite no se versiona, así que un
    contenedor recién creado arrancaría sin base de conocimiento. Con
    `RAG_AUTOCARGA=1` el servicio se indexa solo la primera vez y queda
    operativo sin intervención manual.

    Devuelve cuántos fragmentos se indexaron, o None si no hacía falta.
    """
    if settings.rag_backend != "sqlite" or not settings.rag_autocarga:
        return None

    from services import rag_local

    if rag_local.contar() > 0:
        return None
    if not settings.rag_corpus.exists() or not settings.google_api_key:
        return None

    import logging

    log = logging.getLogger("uvicorn.error")
    log.info("Índice vacío: indexando %s automáticamente", settings.rag_corpus.name)
    total = indexar(settings.rag_corpus, verboso=False)
    log.info("Índice listo: %s fragmentos", total)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", nargs="?", type=Path, default=settings.rag_corpus,
                        help=f"Archivo a indexar (por defecto: {settings.rag_corpus})")
    parser.add_argument("--revisar", action="store_true",
                        help="Solo muestra cuántos fragmentos se generarían, sin llamar a Gemini")
    args = parser.parse_args()

    if not args.corpus.exists():
        print(f"No existe el corpus: {args.corpus}", file=sys.stderr)
        return 1

    fragmentos = extraer_fragmentos(args.corpus)
    if args.revisar:
        if not fragmentos:
            print("El documento no contiene texto aprovechable.", file=sys.stderr)
            return 1
        secciones = len({ubicacion for ubicacion, _ in fragmentos})
        palabras = sum(len(texto.split()) for _, texto in fragmentos)
        print(f"Corpus: {args.corpus.name}")
        print(f"Fragmentos: {len(fragmentos)} en {secciones} secciones ({palabras:,} palabras)")
        print("Modo revisión: no se llamó a Gemini ni se escribió nada.")
        return 0

    if not settings.google_api_key:
        print("Falta GOOGLE_API_KEY en el .env: sin ella no se pueden generar vectores.",
              file=sys.stderr)
        return 1

    guardados = indexar(args.corpus)
    print(f"Indexados {guardados} fragmentos en el backend '{settings.rag_backend}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
