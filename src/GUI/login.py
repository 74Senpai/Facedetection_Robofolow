from tkinter import *
from tkinter import ttk

def create_login_ui(root, face_detection_callback, show_notepad_callback):
    """Tạo giao diện login (UI không xử lý logic, chỉ gọi callback)"""
    frm = ttk.Frame(root, padding=20)
    frm.pack(expand=True, fill=BOTH)

    root.title("Login")
    root.geometry("300x400")
    root.resizable(False, False)

    ttk.Label(frm, text="Đăng nhập", font=("Arial", 20, "bold")).pack(pady=(0, 30))
    ttk.Label(frm, text="Email hoặc số điện thoại", font=("Arial", 14)).pack(anchor=W)
    username_entry = ttk.Entry(frm, font=("Arial", 14))
    username_entry.pack(fill=X, pady=10)

    ttk.Label(frm, text="Mật khẩu", font=("Arial", 14)).pack(anchor=W, pady=(10, 0))
    password_entry = ttk.Entry(frm, show="*", font=("Arial", 14))
    password_entry.pack(fill=X, pady=10)

    ttk.Button(frm, text="Đăng nhập", command=lambda: show_notepad_callback(root, frm)).pack(pady=10, fill=X)
    ttk.Button(frm, text="Đăng nhập bằng Camera", command=face_detection_callback).pack(pady=10, fill=X)
    ttk.Button(frm, text="Thoát", command=root.destroy).pack(side=BOTTOM, fill=X)

    return frm
