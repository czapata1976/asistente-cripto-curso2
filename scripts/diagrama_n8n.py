"""Genera un diagrama Mermaid del workflow de n8n a partir del JSON exportado.

Motivo: la imagen más fiel de lo que hace n8n es su propio lienzo, pero una
captura no sirve como documentación de un repositorio: no se puede revisar en un
diff ni se mantiene al día. Este script lee `n8n/a2a-plan-dca.json` —el artefacto
que se importa de verdad— y dibuja exactamente los nodos y conexiones que
existen, sin transcripción manual que se desactualice.

Uso:
    python scripts/diagrama_n8n.py                 # diagrama + secuencia
    python scripts/diagrama_n8n.py --solo-flujo    # solo el grafo de nodos
"""

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WORKFLOW = RAIZ / "n8n" / "a2a-plan-dca.json"

# Icono por familia de nodo, para que el diagrama se lea sin abrir el JSON.
FORMA = {
    "n8n-nodes-base.webhook": ("[[", "]]", "webhook"),
    "n8n-nodes-base.code": ("{{", "}}", "código"),
    "n8n-nodes-base.respondToWebhook": ("([", "])", "respuesta"),
}


def _id(nombre: str) -> str:
    """Identificador válido para Mermaid a partir del nombre del nodo."""
    limpio = re.sub(r"[^0-9A-Za-z]+", "_", nombre).strip("_")
    return f"n_{limpio}" if limpio else "n_nodo"


def _etiqueta(nodo: dict) -> str:
    """Texto del nodo: nombre, tipo corto y su rol en una línea."""
    tipo = nodo["type"].split(".")[-1]
    rol = FORMA.get(nodo["type"], ("", "", tipo))[2]
    return f"<b>{nodo['name']}</b><br/><small>{rol}</small>"


def diagrama_flujo(datos: dict) -> str:
    """Flowchart de nodos y conexiones tal como están en el workflow."""
    lineas = ["```mermaid", "flowchart LR"]

    for nodo in datos["nodes"]:
        abre, cierra, _ = FORMA.get(nodo["type"], ("[", "]", ""))
        lineas.append(f'    {_id(nodo["name"])}{abre}"{_etiqueta(nodo)}"{cierra}')

    for origen, salidas in datos.get("connections", {}).items():
        for grupo in salidas.get("main", []):
            for destino in grupo or []:
                lineas.append(f'    {_id(origen)} --> {_id(destino["node"])}')

    lineas.append("```")
    return "\n".join(lineas)


def diagrama_secuencia() -> str:
    """Recorrido A2A extremo a extremo, incluyendo al agente principal."""
    return """```mermaid
sequenceDiagram
    autonumber
    participant U as Usuario
    participant A as Agente principal
    participant R as Router (LLM)
    participant N as Workflow n8n
    participant J as Juez

    U->>A: POST /consulta<br/>«50 USD de bitcoin cada semana, 12 semanas»
    A->>R: clasifica la intención
    R-->>A: rama = plan
    A->>A: el LLM extrae parámetros<br/>{monto_usd, frecuencia, semanas, cripto}
    A->>N: message/send (JSON-RPC)<br/>encargo + parámetros
    activate N
    N->>N: Webhook A2A recibe el mensaje
    N->>N: Calcular plan<br/>12 × 50 USD = 600 USD
    N-->>A: artefacto con el plan completo
    deactivate N
    A->>A: redacta usando las cifras<br/>que devolvió n8n
    A->>J: revisa la respuesta
    J-->>U: respuesta final + solicitud_id
```"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--solo-flujo", action="store_true",
                        help="omite el diagrama de secuencia")
    parser.add_argument("--archivo", type=Path, default=WORKFLOW)
    args = parser.parse_args()

    if not args.archivo.exists():
        print(f"No existe el workflow: {args.archivo}", file=sys.stderr)
        return 1

    datos = json.loads(args.archivo.read_text(encoding="utf-8"))

    print(f"## Workflow: {datos['name']}\n")
    print(f"- Nodos: {len(datos['nodes'])}")
    print(f"- Publicado: {'sí' if datos.get('active') else 'no'}")
    print()
    print(diagrama_flujo(datos))
    if not args.solo_flujo:
        print()
        print("## Recorrido completo del encargo\n")
        print(diagrama_secuencia())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
