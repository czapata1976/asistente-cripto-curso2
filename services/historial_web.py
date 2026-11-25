"""Historial web en PostgreSQL o SQLite local."""
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from config import settings
from services.rag_supabase import conectar as conectar_postgres


@contextmanager
def conectar():
    if settings.web_history_postgres:
        with conectar_postgres() as db:
            yield db
        return
    path = settings.web_db
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    try:
        with db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    owner TEXT NOT NULL,
                    messages TEXT NOT NULL,
                    updated TEXT NOT NULL
                )
            """)
            yield db
    finally:
        db.close()


def historial(owner: str, admin: bool) -> list[dict]:
    with conectar() as db:
        rows = db.execute(
            ("SELECT id::text, mensajes::text FROM cripto.conversaciones WHERE propietario = %s OR %s ORDER BY actualizada_en DESC"
             if settings.web_history_postgres else "SELECT id, messages FROM chats WHERE owner = ? OR ? ORDER BY updated DESC"),
            (owner, admin),
        )
        return [{"sessionId": sid, "messages": json.loads(messages)} for sid, messages in rows]


def leer(chat_id: str, owner: str, admin: bool) -> str | None:
    with conectar() as db:
        row = db.execute(
            ("SELECT mensajes::text FROM cripto.conversaciones WHERE id = %s AND (propietario = %s OR %s)"
             if settings.web_history_postgres else "SELECT messages FROM chats WHERE id = ? AND (owner = ? OR ?)"),
            (chat_id, owner, admin),
        ).fetchone()
        return row[0] if row else None


def guardar(chat_id: str, owner: str, anterior: str | None, mensajes: list[dict]) -> bool:
    contenido = json.dumps(mensajes, ensure_ascii=False)
    ahora = datetime.now(timezone.utc).isoformat()
    with conectar() as db:
        if anterior is None:
            sql = ("INSERT INTO cripto.conversaciones (id, propietario, mensajes, actualizada_en) VALUES (%s, %s, %s::jsonb, %s)"
                   if settings.web_history_postgres else "INSERT INTO chats VALUES (?, ?, ?, ?)")
            db.execute(sql, (chat_id, owner, contenido, ahora))
            return True
        result = db.execute(
            ("UPDATE cripto.conversaciones SET mensajes = %s::jsonb, actualizada_en = %s WHERE id = %s AND mensajes = %s::jsonb"
             if settings.web_history_postgres else "UPDATE chats SET messages = ?, updated = ? WHERE id = ? AND messages = ?"),
            (contenido, ahora, chat_id, anterior),
        )
        return result.rowcount == 1


def eliminar(chat_id: str) -> bool:
    with conectar() as db:
        sql = ("DELETE FROM cripto.conversaciones WHERE id = %s"
               if settings.web_history_postgres else "DELETE FROM chats WHERE id = ?")
        return db.execute(sql, (chat_id,)).rowcount == 1
