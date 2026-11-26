"""Registro de ejecuciones: una línea JSON por solicitud.

Cumple dos cosas a la vez:

1. **Criterio de despliegue (base).** La pauta pide "un registro simple que
   permita comprobar qué flujo se ejecutó y cómo terminó". El `logger.info` del
   servidor solo sirve si alguien está mirando la consola; este archivo queda en
   disco y sobrevive a reinicios del proceso, así que el docente puede cruzarlo
   con la respuesta recibida por HTTP usando el `solicitud_id`.

2. **Observabilidad (ampliación).** Al guardar duración, tokens y modelo por
   cada ejecución, `scripts/metricas.py` puede comparar antes/después con las
   mismas entradas.

Se escribe JSON Lines (un objeto por línea) y no un JSON único porque así se
puede agregar con `open(..., "a")` sin reescribir el archivo completo ni
corromperlo si el proceso muere a mitad de escritura.
"""

import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)

# Un lock por proceso: uvicorn atiende en un hilo del pool, y sin esto dos
# escrituras simultáneas podrían intercalar bytes en la misma línea.
_lock = threading.Lock()


def ruta() -> Path:
    """Archivo de registro, ya resuelto contra la carpeta del proyecto."""
    return settings.registro_path


def anotar(evento: dict) -> None:
    """Agrega una ejecución al registro. Nunca interrumpe la respuesta.

    Se registra el fallo de escritura pero no se propaga: perder una línea de
    auditoría no debe tumbar una consulta que ya se respondió bien.
    """
    registro = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        **evento,
    }
    try:
        destino = ruta()
        destino.parent.mkdir(parents=True, exist_ok=True)
        linea = json.dumps(registro, ensure_ascii=False, default=str)
        with _lock, destino.open("a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")
    except OSError as exc:
        logger.warning("No se pudo escribir el registro de ejecución: %s", exc)


def leer(limite: int | None = None) -> list[dict]:
    """Lee las ejecuciones registradas, de la más antigua a la más reciente.

    Las líneas corruptas se descartan: un archivo a medio escribir por un corte
    de energía no debe romper las métricas.
    """
    destino = ruta()
    if not destino.exists():
        return []
    filas: list[dict] = []
    with destino.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            try:
                filas.append(json.loads(linea))
            except json.JSONDecodeError:
                continue
    return filas[-limite:] if limite else filas


def buscar(solicitud_id: str) -> dict | None:
    """Busca una ejecución concreta por su ID (para cruzar con la respuesta)."""
    for fila in reversed(leer()):
        if fila.get("solicitud_id") == solicitud_id:
            return fila
    return None
