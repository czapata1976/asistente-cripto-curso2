"""Métricas y comparación antes/después sobre el registro de ejecuciones.

Cubre la ampliación "+0,5 Rendimiento, costo u observabilidad avanzada", cuya
prueba exigida es: "comparación antes y después con las mismas entradas y sin
perder calidad, o diagnóstico de un problema concreto mediante trazas y
métricas".

Escenario de comparación incluido en el proyecto —el juez LLM:

    python -m evals.ejecutar --sin-juez   # escribe en el registro como "eval"
    mv datos/registros/ejecuciones.jsonl datos/registros/antes.jsonl
    python -m evals.ejecutar              # vuelve a correr los mismos casos
    mv datos/registros/ejecuciones.jsonl datos/registros/despues.jsonl
    python scripts/metricas.py --comparar datos/registros/antes.jsonl datos/registros/despues.jsonl

El juez añade una llamada al modelo por consulta: esa es la hipótesis. Las
métricas dicen cuánto cuesta y si a cambio se gana algo.

Uso:
    python scripts/metricas.py                       # resumen del registro actual
    python scripts/metricas.py --archivo ruta.jsonl
    python scripts/metricas.py --comparar a.jsonl b.jsonl
    python scripts/metricas.py --json                # salida legible por máquina
"""

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from config import settings  # noqa: E402
from services import registro  # noqa: E402


def percentil(valores: list[float], p: float) -> float:
    """Percentil por interpolación lineal (suficiente para pocas muestras)."""
    if not valores:
        return 0.0
    ordenados = sorted(valores)
    if len(ordenados) == 1:
        return ordenados[0]
    posicion = (len(ordenados) - 1) * p
    inferior = int(posicion)
    superior = min(inferior + 1, len(ordenados) - 1)
    peso = posicion - inferior
    return ordenados[inferior] * (1 - peso) + ordenados[superior] * peso


def resumir(filas: list[dict]) -> dict:
    """Agrega el registro en totales y por ruta."""
    por_ruta: dict[str, list[dict]] = defaultdict(list)
    for fila in filas:
        por_ruta[fila.get("ruta") or "sin_ruta"].append(fila)

    def bloque(subconjunto: list[dict]) -> dict:
        latencias = [f.get("duracion_ms") or 0 for f in subconjunto]
        entradas = [f.get("tokens_entrada") or 0 for f in subconjunto]
        salidas = [f.get("tokens_salida") or 0 for f in subconjunto]
        llamadas = [f.get("llm_llamadas") or 0 for f in subconjunto]
        errores = sum(1 for f in subconjunto if f.get("error") or f.get("estado") == "error")
        return {
            "n": len(subconjunto),
            "error_pct": round(100 * errores / len(subconjunto), 1) if subconjunto else 0.0,
            "p50_ms": round(percentil(latencias, 0.50), 1),
            "p95_ms": round(percentil(latencias, 0.95), 1),
            "tokens_entrada": sum(entradas),
            "tokens_salida": sum(salidas),
            "tokens_medio": round(statistics.fmean(entradas[i] + salidas[i]
                                                  for i in range(len(subconjunto))), 1)
            if subconjunto else 0.0,
            "llm_llamadas_medio": round(statistics.fmean(llamadas), 2) if llamadas else 0.0,
        }

    return {
        "total": bloque(filas),
        "por_ruta": {ruta: bloque(sub) for ruta, sub in sorted(por_ruta.items())},
        "estados": dict(Counter(f.get("estado") or "-" for f in filas)),
        "acciones_bloqueadas": sum(1 for f in filas if f.get("accion_bloqueada")),
    }


def _tabla(resumen: dict, titulo: str) -> list[str]:
    lineas = [
        f"### {titulo}",
        "",
        "| Ruta | n | Error % | p50 ms | p95 ms | Tokens ent. | Tokens sal. | Tokens medio | Llamadas LLM |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    filas = [("TOTAL", resumen["total"])] + list(resumen["por_ruta"].items())
    for nombre, b in filas:
        lineas.append(
            f"| `{nombre}` | {b['n']} | {b['error_pct']}% | {b['p50_ms']:.0f} | "
            f"{b['p95_ms']:.0f} | {b['tokens_entrada']:,} | {b['tokens_salida']:,} | "
            f"{b['tokens_medio']:.0f} | {b['llm_llamadas_medio']} |"
        )
    lineas.append("")
    estados = ", ".join(f"{k}: {v}" for k, v in resumen["estados"].items())
    lineas.append(f"Estados: {estados or '-'} · Acciones bloqueadas: {resumen['acciones_bloqueadas']}")
    lineas.append("")
    return lineas


def comparar(antes: dict, despues: dict) -> list[str]:
    """Tabla de diferencia entre dos resúmenes sobre las mismas entradas."""
    lineas = [
        "### Comparación antes / después",
        "",
        "Las mismas entradas ejecutadas dos veces. Δ es `después - antes`.",
        "",
        "| Métrica | Antes | Después | Δ |",
        "|---|---|---|---|",
    ]

    def fila(nombre: str, clave: str, formato: str = "{:.1f}") -> None:
        a = antes["total"][clave]
        d = despues["total"][clave]
        delta = d - a
        signo = "+" if delta > 0 else ""
        lineas.append(f"| {nombre} | {formato.format(a)} | {formato.format(d)} | "
                      f"{signo}{formato.format(delta)} |")

    fila("Ejecuciones", "n", "{:.0f}")
    fila("p50 latencia (ms)", "p50_ms")
    fila("p95 latencia (ms)", "p95_ms")
    fila("Tokens de entrada", "tokens_entrada", "{:,.0f}")
    fila("Tokens de salida", "tokens_salida", "{:,.0f}")
    fila("Llamadas al modelo por consulta", "llm_llamadas_medio", "{:.2f}")
    fila("Tasa de error (%)", "error_pct", "{:.1f}")
    lineas.append("")
    return lineas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--archivo", type=Path, help="registro a resumir (por defecto, el del .env)")
    parser.add_argument("--comparar", nargs=2, type=Path, metavar=("ANTES", "DESPUES"),
                        help="dos registros a comparar")
    parser.add_argument("--json", action="store_true", help="imprime JSON en vez de tablas")
    args = parser.parse_args()

    if args.comparar:
        antes, despues = args.comparar
        for ruta in (antes, despues):
            if not ruta.exists():
                print(f"No existe: {ruta}", file=sys.stderr)
                return 1
        fa = [json.loads(l) for l in antes.read_text(encoding="utf-8").splitlines() if l.strip()]
        fd = [json.loads(l) for l in despues.read_text(encoding="utf-8").splitlines() if l.strip()]
        ra, rd = resumir(fa), resumir(fd)
        if args.json:
            print(json.dumps({"antes": ra, "despues": rd}, ensure_ascii=False, indent=2))
            return 0
        print("\n".join(
            ["# Métricas del asistente cripto", ""]
            + _tabla(ra, "Antes") + _tabla(rd, "Después") + comparar(ra, rd)
        ))
        return 0

    ruta = args.archivo or registro.ruta()
    if not ruta.exists():
        print(f"No hay registro en {ruta}. Ejecuta alguna consulta primero.", file=sys.stderr)
        return 1
    filas = [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l.strip()]
    resumen = resumir(filas)
    if args.json:
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
        return 0
    print(f"Modelo: {settings.google_model} · Registro: {ruta}\n")
    print("\n".join(_tabla(resumen, "Resumen")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
