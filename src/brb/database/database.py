import sqlite3
import os
from brb.saving.models import Session

class Database:
    def __init__(self, db_path: str = os.path.expanduser("~/.brb/brb.db")):
        self.db_path = db_path
        self._memory_conn = None

    def get_connection(self) -> sqlite3.Connection:
        if self.db_path == ":memory:":
            if self._memory_conn is None:
                self._memory_conn = sqlite3.connect(self.db_path)
                self._memory_conn.execute("PRAGMA foreign_keys = ON")
            return self._memory_conn

        dirname = os.path.dirname(self.db_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
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
                    message TEXT NOT NULL,
                    git_branch TEXT,
                    git_status TEXT
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

    def insert_session(self, sess: Session) -> Session|None:
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO sessions (folder, message, git_branch, git_status) VALUES(?, ?, ?, ?)
            """, (sess.folder, sess.message, sess.git_branch, sess.git_status))
            sess.id = cursor.lastrowid
            conn.executemany("""
                INSERT INTO commands (session_id, command) VALUES(?, ?)
            """, [(sess.id, c) for c in sess.commands])
        return self.fetch_session_by_id(sess.id)


    def fetch_all_commands(self, indexsession: int) -> list[str]:
        with self.get_connection() as conn:
            commands = conn.execute("""
                SELECT command
                FROM commands
                WHERE session_id = ?
            """, (indexsession,)).fetchall()
            return [command[0] for command in commands]

    def fetch_session_by_id(self, indexsession: int) -> Session|None:
        with self.get_connection() as conn:
            row = conn.execute("""
                SELECT id, folder, created_at, message, git_branch, git_status
                FROM sessions
                WHERE id = ?
            """, (indexsession,)).fetchone()

            if not row:
                return None

            return Session(
                id = row[0],
                folder = row[1],
                created_at = row[2],
                message = row[3],
                commands = self.fetch_all_commands(row[0]),
                git_branch = row[4],
                git_status = row[5]
            )

    def fetch_last_session(self) -> Session|None:
        with self.get_connection() as conn:
            last_sess = conn.execute("""
                SELECT id, folder, created_at, message, git_branch, git_status
                FROM sessions
                ORDER BY id DESC
                LIMIT 1
            """).fetchone()

            if last_sess is None:
                return None

            commands = self.fetch_all_commands(last_sess[0])

            return Session(
                id= last_sess[0],
                folder= last_sess[1],
                created_at= last_sess[2],
                message= last_sess[3],
                commands= commands,
                git_branch = last_sess[4],
                git_status = last_sess[5]
            )

    def fetch_last_session_by_folder(self, folder: str) -> Session|None:
        with self.get_connection() as conn:
            last_sess = conn.execute("""
                SELECT id, folder, created_at, message, git_branch, git_status
                FROM sessions
                WHERE folder = ?
                ORDER BY id DESC
                LIMIT 1
            """, (folder,)).fetchone()

            if last_sess is None:
                return None

            commands = self.fetch_all_commands(last_sess[0])

            return Session(
                id= last_sess[0],
                folder= last_sess[1],
                created_at= last_sess[2],
                message= last_sess[3],
                commands= commands,
                git_branch = last_sess[4],
                git_status = last_sess[5]
            )

    def fetch_all_sessions(self) -> list[Session] | None:
        with self.get_connection() as conn:
            all_sess = conn.execute("""
                SELECT id, folder, created_at, message, git_branch, git_status
                FROM sessions
                ORDER BY id DESC
            """).fetchall()

            if all_sess is None:
                return None

            return [Session(
                id= i[0],
                folder= i[1],
                created_at= i[2],
                message= i[3],
                commands= self.fetch_all_commands(i[0]),
                git_branch = i[4],
                git_status = i[5]
            ) for i in all_sess]