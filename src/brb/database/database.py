import sqlite3
import os

class Database:
    def __init__(self, db_path: str = os.path.expanduser("~/.brb/brb.db")):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self) -> None:
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    folder TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now', 'localtime')),
                    message TEXT NOT NULL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    command TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """)

    def insert_session(self, folder: str, message: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO sessions (folder, message) VALUES(?, ?)
            """, (folder, message))
            return cursor.lastrowid

    def insert_command(self, sess_id: int, command: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO commands (session_id, command) VALUES(?, ?)
            """, (sess_id, command))
            return cursor.lastrowid

    def insert_saving (self, path: str, message: str, lastcommands: list[str]):
        s_id = self.insert_session(path, message)
        for c in lastcommands:
            self.insert_command(s_id, c)

    def fetch_all_commands(self, indexsession: int) -> list[str]:
        with self.get_connection() as conn:
            commands = conn.execute("""
                SELECT command
                FROM commands
                WHERE session_id = ?
            """, (indexsession,)).fetchall()
            return [command[0] for command in commands]

    def fetch_last_session(self) -> dict|None:
        with self.get_connection() as conn:
            last_sess = conn.execute("""
                SELECT id, folder, created_at, message 
                FROM sessions
                ORDER BY id DESC
                LIMIT 1
            """).fetchone()

            if last_sess is None:
                return None

            commands = self.fetch_all_commands(last_sess[0])

            return {
                "id": last_sess[0],
                "folder": last_sess[1],
                "created_at": last_sess[2],
                "message": last_sess[3],
                "commands": commands
            }

    def fetch_all_sessions(self) -> list[dict] | None:
        with self.get_connection() as conn:
            all_sess = conn.execute("""
                SELECT id, folder, created_at, message 
                FROM sessions
                ORDER BY id DESC
            """).fetchall()

            if all_sess is None:
                return None

            return [{
                "id": i[0],
                "folder": i[1],
                "created_at": i[2],
                "message": i[3],
                "commands": self.fetch_all_commands(i[0])
            } for i in all_sess]