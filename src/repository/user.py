import sqlite3
import os

DB_PATH = "src/database/roboflow.db"

class User:
    def __init__(self, username):
        self.username = username
        self.note = None
        self._load_user()

    def _connect(self):
        """Tạo kết nối đến DB"""
        return sqlite3.connect(DB_PATH)

    def _load_user(self):
        """Tải thông tin người dùng từ DB"""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT note FROM users WHERE username = ?", (self.username,))
        row = cur.fetchone()
        conn.close()

        if row:
            self.note = row[0] or ""
        else:
            raise ValueError(f"User '{self.username}' không tồn tại trong database.")

    def update_note(self, new_note):
        """Cập nhật ghi chú trong DB"""
        self.note = new_note
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("UPDATE users SET note = ? WHERE username = ?", (new_note, self.username))
        conn.commit()
        conn.close()
        print(f"✅ Note của {self.username} đã được cập nhật.")
