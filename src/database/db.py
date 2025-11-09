import sqlite3
import os
import json
from src.config import DATABASE_PATH

def init_db():
    """
    Tạo database và bảng users + face_vectors.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS face_vectors (
            id_vector INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            embedding TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id_user)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        users = [
            ("Thong Senpai", "123456", "Hello world"),
            ("TamCter", "baque", "Tribeti"),
            ("Thong", "123123", "Notepad siêu cấp"),
            ("Huy", "363636", "Notepad content")
        ]
        cursor.executemany("INSERT INTO users (username, password, note) VALUES (?, ?, ?)", users)
        print("✅ Database initialized with sample users.")
    else:
        print("ℹ️ Database already initialized.")

    conn.commit()
    conn.close()


def check_login(username: str, password: str) -> bool:
    """Kiểm tra thông tin đăng nhập."""
    if not os.path.exists(DATABASE_PATH):
        print("⚠️ Database chưa được khởi tạo.")
        return False

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def insert_face_vector(user_id: int, embedding: list):
    """Lưu vector khuôn mặt vào bảng face_vectors."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO face_vectors (user_id, embedding)
        VALUES (?, ?)
    """, (user_id, json.dumps(embedding)))
    conn.commit()
    conn.close()


def get_all_face_vectors():
    """Lấy toàn bộ embedding trong DB."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, embedding FROM face_vectors")
    data = cursor.fetchall()
    conn.close()
    return data


def get_user_id(username: str):
    """Trả về id_user theo username."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id_user FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_username_by_id(user_id: int):
    """Trả về username dựa trên id_user."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id_user = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
