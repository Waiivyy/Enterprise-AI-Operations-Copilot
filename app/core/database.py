import json
import sqlite3
from pathlib import Path

from app.core.config import get_settings

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def seed_demo_database(path: Path | None = None) -> Path:
    db_path = path or get_settings().sqlite_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    users = json.loads((DATA_DIR / "sample_users.json").read_text())
    tickets = json.loads((DATA_DIR / "sample_tickets.json").read_text())
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                department TEXT NOT NULL,
                region TEXT NOT NULL,
                employment_type TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                requester TEXT NOT NULL,
                requester_email TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT OR REPLACE INTO users
            (email, display_name, department, region, employment_type)
            VALUES (:email, :display_name, :department, :region, :employment_type)
            """,
            users,
        )
        connection.executemany(
            """
            INSERT OR REPLACE INTO tickets
            (ticket_id, requester, requester_email, title, description)
            VALUES (:ticket_id, :requester, :requester_email, :title, :description)
            """,
            tickets,
        )
    return db_path
