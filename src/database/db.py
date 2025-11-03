import sqlite3
import os

DB_PATH = "src/database/roboflow.db"

def init_db():
    """
    Tạo database và bảng users nếu chưa tồn tại.
    Đồng thời chèn các user mẫu nếu bảng đang trống.
    """
    # Kết nối hoặc tạo mới DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tạo bảng nếu chưa có
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            note TEXT
        )
    """)

    # Kiểm tra xem bảng có dữ liệu chưa
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    # Nếu chưa có, thêm dữ liệu mẫu
    if count == 0:
        users = [
            ("Thong Senpai", "123456", "Hello world"),
            ("Tam Cter", "baque", "Tribeti"),
            ("Thong", "123123", "Day la notepad sieu cap vip pro"),
            ("Huy", "363636", "Day la notpad content")
        ]
        cursor.executemany("INSERT INTO users (username, password, note) VALUES (?, ?, ?)", users)
        print("✅ Database initialized with sample users.")
    else:
        print("ℹ️ Database already initialized.")

    conn.commit()
    conn.close()


def check_login(username: str, password: str) -> bool:
    """
    Kiểm tra thông tin đăng nhập.
    Trả về True nếu username và password đúng, ngược lại False.
    """
    if not os.path.exists(DB_PATH):
        print("⚠️ Database chưa được khởi tạo. Gọi init_db() trước.")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    conn.close()
    return user is not None

