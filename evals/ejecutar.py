"""Conjunto de casos de evaluación versionado y ejecutable.

Cubre la ampliación "+0,5 Evaluación o control avanzado": la pauta pide "un
conjunto de casos versionado y ejecutado con resultados esperados".

Por qué un archivo de casos y no solo tests unitarios: los tests verifican
funciones puras (una calculadora, un parser). Aquí se verifica el
**comportamiento del agente** extremo a extremo, que depende del modelo y por
tanto cambia entre versiones del prompt. Tener las expectativas declaradas en
datos —y no en código— permite ver de un vistazo qué se degradó.

Uso:
    python -m evals.ejecutar                  # todos los casos
    python -m evals.ejecutar --solo calc-ganancia
    python -m evals.ejecutar --sin-juez       # comparación "antes"
    python -m evals.ejecutar --sin-dependencias  # omite A2A y MCP si no están

Esquema de cada línea de `casos.jsonl`:

    id          identificador estable (no cambiar: aparece en los informes)
    mensaje     entrada que se envía al agente
    requiere    "especialista" | "mcp" | ausente. Si la dependencia no
                responde, el caso se marca OMITIDO en vez de FALLIDO.
    espera      expectativas, todas opcionales:
        ruta                       rama esperada (texto o lista)
        traza_contiene             subcadenas que deben aparecer en `traza`
        respuesta_contiene_cualquiera  al menos una de estas subcadenas
        respuesta_no_contiene      ninguna de estas subcadenas
        fuentes_min / fuentes_max  número de fuentes citadas
        herramientas_min           pasos ReAct ejecutados
        mcp_min                    pasos MCP ejecutados
        delegacion                 estado esperado de la delegación A2A
        bloqueado                  la acción debió bloquearse sin ejecutarse
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from config import settings  # noqa: E402
import servidor  # noqa: E402
from main import build_graph  # noqa: E402


CASOS = Path(__file__).resolve().parent / "casos.jsonl"
RESULTADOS = Path(__file__).resolve().parent / "resultados"


def cargar_casos(solo: str | None = None) -> list[dict]:
    """Lee los casos y aplica el filtro opcional por id."""
    casos = []
    for linea in CASOS.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        caso = json.loads(linea)
        if solo and caso["id"] != solo:
            continue
        casos.append(caso)
    return casos


def _alcanzable(requiere: str | None) -> tuple[bool, str]:
    """Comprueba si la dependencia externa del caso está disponible."""
    if requiere == "especialista":
        base = settings.especialista_url.rstrip("/")
        try:
            respuesta = httpx.post(
                f"{base}/assistants/search",
                json={"graph_id": "especialista_cripto", "limit": 1}, timeout=4,
            )
            return respuesta.status_code == 200, f"especialista en {base}"
        except httpx.HTTPError as exc:
            return False, f"especialista no responde ({type(exc).__name__})"
    if requiere == "mcp":
        if not settings.mcp_url:
            return False, "MCP_URL sin configurar"
        try:
            respuesta = httpx.get(settings.mcp_url, timeout=8)
            # El servidor MCP puede rechazar GET; lo que importa es que conteste.
            return respuesta.status_code < 500, f"MCP en {settings.mcp_url}"
        except httpx.HTTPError as exc:
            return False, f"MCP no responde ({type(exc).__name__})"
    if requiere == "n8n":
        if not settings.n8n_webhook_url:
            return False, "N8N_WEBHOOK_URL sin configurar"
        # Se envía un message/send mínimo: un 404 significa webhook inexistente.
        try:
            respuesta = httpx.post(settings.n8n_webhook_url, json={
                "jsonrpc": "2.0", "id": "sonda", "method": "message/send",
                "params": {"message": {"parts": [{"kind": "text", "text": "{}"}]}},
            }, timeout=10)
            return respuesta.status_code == 200, f"n8n en {settings.n8n_webhook_url}"
        except httpx.HTTPError as exc:
            return False, f"n8n no responde ({type(exc).__name__})"
    return True, "sin dependencias externas"


def evaluar(caso: dict, payload: dict) -> list[str]:
    """Devuelve la lista de fallos; vacía significa que el caso pasó."""
    espera = caso.get("espera", {})
    fallos: list[str] = []

    if "ruta" in espera:
        esperadas = espera["ruta"]
        esperadas = [esperadas] if isinstance(esperadas, str) else esperadas
        if payload.get("ruta") not in esperadas:
            fallos.append(f"ruta={payload.get('ruta')!r}, se esperaba {esperadas}")

    if "traza_contiene" in espera:
        traza = payload.get("traza") or []
        for fragmento in espera["traza_contiene"]:
            if fragmento not in traza:
                fallos.append(f"traza sin {fragmento!r} (tiene {traza})")

    respuesta = (payload.get("respuesta") or "").casefold()

    if "respuesta_contiene_cualquiera" in espera:
        opciones = espera["respuesta_contiene_cualquiera"]
        if not any(opcion.casefold() in respuesta for opcion in opciones):
            fallos.append(f"la respuesta no contiene ninguna de {opciones}")

    for prohibido in espera.get("respuesta_no_contiene", []):
        if prohibido.casefold() in respuesta:
            fallos.append(f"la respuesta contiene {prohibido!r}, que está prohibido")

    fuentes = payload.get("fuentes") or []
    if "fuentes_min" in espera and len(fuentes) < espera["fuentes_min"]:
        fallos.append(f"{len(fuentes)} fuentes, se esperaban al menos {espera['fuentes_min']}")
    if "fuentes_max" in espera and len(fuentes) > espera["fuentes_max"]:
        fallos.append(f"{len(fuentes)} fuentes, se esperaban como máximo {espera['fuentes_max']}")

    if "herramientas_min" in espera:
        pasos = payload.get("herramientas") or []
        if len(pasos) < espera["herramientas_min"]:
            fallos.append(f"{len(pasos)} pasos ReAct, se esperaban al menos {espera['herramientas_min']}")

    if "mcp_min" in espera:
        pasos = payload.get("mcp") or []
        if len(pasos) < espera["mcp_min"]:
            fallos.append(f"{len(pasos)} pasos MCP, se esperaban al menos {espera['mcp_min']}")

    if "delegacion" in espera:
        estado = (payload.get("delegacion") or {}).get("estado")
        if estado != espera["delegacion"]:
            fallos.append(f"delegación={estado!r}, se esperaba {espera['delegacion']!r}")

    if espera.get("bloqueado"):
        if not ((payload.get("delegacion") or {}).get("estado") == "bloqueado"
                or "accion_bloqueada" in (payload.get("traza") or [])
                or "no autorizada" in respuesta
                or "deshabilitado" in respuesta):
            fallos.append("la acción no se bloqueó")

    return fallos


async def correr(casos: list[dict], grafo, sin_dependencias: bool) -> list[dict]:
    """Ejecuta cada caso y devuelve el resultado con su veredicto."""
    resultados = []
    for caso in casos:
        disponible, detalle = _alcanzable(caso.get("requiere"))
        if sin_dependencias and not disponible:
            resultados.append({"id": caso["id"], "veredicto": "OMITIDO",
                               "detalle": detalle, "fallos": [], "payload": {}})
            continue
        try:
            payload, status = await servidor.ejecutar_consulta(
                caso["mensaje"], [], origen="eval", grafo=grafo
            )
        except Exception as exc:  # noqa: BLE001 - el informe debe sobrevivir a un fallo
            resultados.append({"id": caso["id"], "veredicto": "FALLIDO",
                               "detalle": f"excepción {type(exc).__name__}: {exc}",
                               "fallos": [str(exc)], "payload": {}})
            continue

        if status != 200:
            resultados.append({"id": caso["id"], "veredicto": "FALLIDO",
                               "detalle": f"HTTP {status}",
                               "fallos": [payload.get("error", "")], "payload": payload})
            continue

        fallos = evaluar(caso, payload)
        resultados.append({
            "id": caso["id"],
            "veredicto": "FALLIDO" if fallos else "PASÓ",
            "detalle": payload.get("ruta") or "-",
            "fallos": fallos,
            "payload": payload,
        })
    return resultados


def escribir_informes(resultados: list[dict], etiqueta: str) -> Path:
    """Guarda el informe en JSON y en Markdown (evidencia para el README)."""
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    sello = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destino = RESULTADOS / f"{sello}-{etiqueta}"

    (destino.with_suffix(".json")).write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total = len(resultados)
    paso = sum(1 for r in resultados if r["veredicto"] == "PASÓ")
    omitido = sum(1 for r in resultados if r["veredicto"] == "OMITIDO")
    lineas = [
        f"# Evaluación del agente — {etiqueta}",
        "",
        f"- Fecha: {sello}",
        f"- Modelo: `{settings.google_model}`",
        f"- Backend RAG: `{settings.rag_backend}`",
        f"- Resultado: **{paso}/{total - omitido}** casos aprobados"
        + (f" ({omitido} omitidos por dependencia no disponible)" if omitido else ""),
        "",
        "| Caso | Veredicto | Ruta | Detalle |",
        "|---|---|---|---|",
    ]
    for r in resultados:
        detalle = "; ".join(r["fallos"]) if r["fallos"] else r["detalle"]
        lineas.append(f"| `{r['id']}` | {r['veredicto']} | `{r['detalle']}` | {detalle} |")
    (destino.with_suffix(".md")).write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print(f"\nInforme: {destino.with_suffix('.md')}")
    return destino


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--solo", help="ejecuta un único caso por id")
    parser.add_argument("--sin-juez", action="store_true",
                        help="desactiva el juez LLM (comparación 'antes')")
    parser.add_argument("--sin-dependencias", action="store_true",
                        help="omite los casos cuya dependencia externa no responde")
    args = parser.parse_args()

    casos = cargar_casos(args.solo)
    if not casos:
        print("No hay casos que ejecutar.", file=sys.stderr)
        return 1

    etiqueta = "sin-juez" if args.sin_juez else "con-juez"
    grafo = build_graph(incluir_juez=not args.sin_juez)

    print(f"Ejecutando {len(casos)} casos ({etiqueta})…\n")
    resultados = asyncio.run(correr(casos, grafo, args.sin_dependencias))

    ancho = max(len(r["id"]) for r in resultados)
    for r in resultados:
        marca = {"PASÓ": "OK  ", "FALLIDO": "FALLA", "OMITIDO": "OMITE"}[r["veredicto"]]
        print(f"  [{marca}] {r['id']:<{ancho}}  {r['detalle']}")
        for fallo in r["fallos"]:
            print(f"            → {fallo}")

    escribir_informes(resultados, etiqueta)

    fallidos = [r for r in resultados if r["veredicto"] == "FALLIDO"]
    return 1 if fallidos else 0


if __name__ == "__main__":
    raise SystemExit(main())
