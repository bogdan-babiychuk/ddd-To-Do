import os
import aiosqlite
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from pathlib import Path

DEFAULT_DB_PATH = "src/db/url_shortener.db"


def get_db_path() -> Path:
    return Path(os.getenv("DB_PATH", DEFAULT_DB_PATH))


async def init_db() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(db_path) as conn:
        await conn.execute("PRAGMA foreign_keys=ON")

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shortened_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT NOT NULL UNIQUE,
                original_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks_count INTEGER NOT NULL DEFAULT 0,
                last_click_at TEXT NULL
            )
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS link_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                clicked_at TEXT NOT NULL,
                FOREIGN KEY(short_id) REFERENCES shortened_links(short_id) ON DELETE CASCADE
            )
            """
        )




async def get_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    db_path = get_db_path()
    async with aiosqlite.connect(db_path) as conn:
        await conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = aiosqlite.Row
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
