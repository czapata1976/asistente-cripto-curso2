"""Fachada del recuperador: elige el backend según `RAG_BACKEND`.

- `RAG_BACKEND=sqlite`   → `services.rag_local` (archivo local, sin servidor).
- `RAG_BACKEND=postgres` → `services.rag_supabase` (pgvector en Postgres/Supabase).

Ambos exponen `buscar()` y `formatear()` con la misma forma de salida, así que
`nodes/rag.py` y el especialista no necesitan saber cuál está activo.
"""

import logging

from config import settings

logger = logging.getLogger(__name__)

if settings.rag_backend == "postgres":
    from services import rag_supabase as backend
else:
    from services import rag_local as backend

NOMBRE_BACKEND = settings.rag_backend

buscar = backend.buscar
formatear = backend.formatear

logger.debug("Backend de RAG activo: %s", NOMBRE_BACKEND)

__all__ = ["buscar", "formatear", "backend", "NOMBRE_BACKEND"]
