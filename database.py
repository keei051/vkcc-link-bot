import sqlite3
from typing import List, Tuple, Optional

class Database:
    def __init__(self, path="database.db"):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                original_url TEXT,
                short_url TEXT,
                title TEXT
            )
        """)
        self.conn.commit()

    def add_link(self, user_id: int, original_url: str, short_url: str, title: Optional[str] = None):
        self.cursor.execute(
            "INSERT INTO links (user_id, original_url, short_url, title) VALUES (?, ?, ?, ?)",
            (user_id, original_url, short_url, title)
        )
        self.conn.commit()

    def get_links(self, user_id: int) -> List[Tuple[int, str, str, Optional[str]]]:
        self.cursor.execute(
            "SELECT id, original_url, short_url, title FROM links WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        return self.cursor.fetchall()

    def delete_link(self, link_id: int, user_id: int) -> bool:
        self.cursor.execute(
            "DELETE FROM links WHERE id = ? AND user_id = ?",
            (link_id, user_id)
        )
        deleted = self.cursor.rowcount > 0
        self.conn.commit()
        return deleted

    def rename_link(self, link_id: int, user_id: int, new_title: str) -> bool:
        self.cursor.execute(
            "UPDATE links SET title = ? WHERE id = ? AND user_id = ?",
            (new_title, link_id, user_id)
        )
        updated = self.cursor.rowcount > 0
        self.conn.commit()
        return updated

    def get_link(self, link_id: int, user_id: int) -> Optional[Tuple[str, str, Optional[str]]]:
        self.cursor.execute(
            "SELECT original_url, short_url, title FROM links WHERE id = ? AND user_id = ?",
            (link_id, user_id)
        )
        return self.cursor.fetchone()
