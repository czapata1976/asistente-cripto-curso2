"""Configuración centralizada del chasis.

Este es el ÚNICO módulo que lee variables de entorno (patrón de los talleres).
Todo lo demás importa `settings` desde aquí. Así nunca hay credenciales
escritas en el código ni lecturas de os.environ dispersas.

El .env se busca en la raíz del proyecto (junto a este chasis).
"""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


# Carpeta de este archivo (chasis-agente/) y la raíz del proyecto (Taller Final/).
PROJECT_DIR = Path(__file__).resolve().parent
ROOT_DIR = PROJECT_DIR.parent

# Se carga primero el .env de la raíz y, si existe, el local del chasis.
load_dotenv(ROOT_DIR / ".env")
load_dotenv(PROJECT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    """Valores de configuración usados por todo el chasis."""

    # --- LLM (obligatorio) ---
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    google_model: str = os.getenv("GOOGLE_MODEL", "gemini-3.6-flash")

    supabase_db_url: str = os.getenv("SUPABASE_DB_URL", "")
    embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

    # --- RAG con Redis (bono, opcional) ---
    redis_url: str = os.getenv("REDIS_URL", "")
    redis_prefijo: str = os.getenv("REDIS_PREFIJO", "")

    # --- MCP (bono, opcional) ---
    mcp_url: str = os.getenv("MCP_URL", "")

    especialista_url: str = os.getenv("ESPECIALISTA_A2A_URL", "http://127.0.0.1:2024")
    especialista_token: str = os.getenv("ESPECIALISTA_API_TOKEN", "")
    api_token: str = os.getenv("CRIPTO_API_TOKEN", "")

    web_user_password: str = os.getenv("WEB_USER_PASSWORD", "")
    web_admin_password: str = os.getenv("WEB_ADMIN_PASSWORD", "")
    web_session_secret: str = os.getenv("WEB_SESSION_SECRET", "")
    web_secure_cookie: bool = os.getenv("WEB_SECURE_COOKIE", "") == "1"
    web_db: Path = Path(os.getenv("WEB_HISTORY_DB", str(PROJECT_DIR / "datos" / "historial_web.sqlite3")))

    # --- Trazas / debug ---
    debug: bool = os.getenv("DEBUG", "") == "1"


settings = Settings()


def require_llm() -> Settings:
    """Valida que existan las credenciales mínimas del LLM.

    Se llama de forma diferida (al crear el modelo), no al importar, para que
    el grafo se pueda importar y compilar sin credenciales.
    """
    faltan = [
        nombre
        for nombre, valor in (
            ("GOOGLE_API_KEY", settings.google_api_key),
            ("GOOGLE_MODEL", settings.google_model),
        )
        if not valor
    ]
    if faltan:
        raise RuntimeError(
            "Falta configurar " + ", ".join(faltan) + " en el .env de la raíz."
        )
    return settings
