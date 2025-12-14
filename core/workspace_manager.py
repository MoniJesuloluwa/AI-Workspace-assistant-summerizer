import os
import sqlite3
from datetime import datetime
from core.file_analyzer import FileAnalyzer


class WorkspaceManager:
    """
    Handles database operations:
    - Creating tables
    - Indexing directories
    - Storing file metadata
    - Querying
    """

    DB_PATH = "data/workspace.db"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(self.DB_PATH)
        self._create_tables()
        self.analyzer = FileAnalyzer()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT UNIQUE,
                extension TEXT,
                size INTEGER,
                modified TEXT,
                content TEXT,
                summary TEXT,
                category TEXT
            );
        """)
        self.conn.commit()

    # ----------------------------
    # Indexing
    # ----------------------------
    def index_directory(self, directory: str) -> int:
        """
        Walks a directory and indexes all supported files.
        Returns: number of files successfully scanned.
        """
        indexed_count = 0

        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)

                content = self.analyzer.extract_text(full_path)
                if not content.strip():
                    continue

                stats = os.stat(full_path)

                self._upsert_file(
                    name=file,
                    path=full_path,
                    extension=os.path.splitext(file)[1],
                    size=stats.st_size,
                    modified=datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    content=content
                )
                indexed_count += 1

        return indexed_count

    def _upsert_file(self, name, path, extension, size, modified, content):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO files (name, path, extension, size, modified, content)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                name = excluded.name,
                extension = excluded.extension,
                size = excluded.size,
                modified = excluded.modified,
                content = excluded.content;
        """, (name, path, extension, size, modified, content))
        self.conn.commit()

    # ----------------------------
    # Querying
    # ----------------------------
    def list_files(self, limit=50):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, size, category, path FROM files
            ORDER BY id DESC
            LIMIT ?;
        """, (limit,))
        return cursor.fetchall()

    def search_files(self, query: str):
        cursor = self.conn.cursor()
        like = f"%{query}%"
        cursor.execute("""
            SELECT id, name, summary, path FROM files
            WHERE name LIKE ? OR summary LIKE ? OR content LIKE ?
            ORDER BY id DESC;
        """, (like, like, like))
        return cursor.fetchall()

    # ----------------------------
    # For AI Summaries
    # ----------------------------
    def get_files_missing_summaries(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, content FROM files
            WHERE (summary IS NULL OR summary = '')
            ORDER BY id DESC
            LIMIT ?;
        """, (limit,))
        return cursor.fetchall()

    def update_summary(self, file_id: int, summary: str, category: str | None = None):
        cursor = self.conn.cursor()
        if category is None:
            cursor.execute("""
                UPDATE files
                SET summary = ?
                WHERE id = ?;
            """, (summary, file_id))
        else:
            cursor.execute("""
                UPDATE files
                SET summary = ?, category = ?
                WHERE id = ?;
            """, (summary, category, file_id))
        self.conn.commit()
