from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def create_login_ui(
        root, 
        face_detection_callback, 
        check_login_callback,
        show_notepad_callback):
    """Tạo giao diện login (UI không xử lý logic, chỉ gọi callback)"""
    frm = ttk.Frame(root, padding=20)
    frm.pack(expand=True, fill=BOTH)

    root.title("Login")
    root.geometry("300x400")
    root.resizable(False, False)

    # ===== UI components =====
    ttk.Label(frm, text="Đăng nhập", font=("Arial", 20, "bold")).pack(pady=(0, 30))
    ttk.Label(frm, text="Email hoặc số điện thoại", font=("Arial", 14)).pack(anchor=W)
    username_entry = ttk.Entry(frm, font=("Arial", 14))
    username_entry.pack(fill=X, pady=10)

    ttk.Label(frm, text="Mật khẩu", font=("Arial", 14)).pack(anchor=W, pady=(10, 0))
    password_entry = ttk.Entry(frm, show="*", font=("Arial", 14))
    password_entry.pack(fill=X, pady=10)

    # ===== Callback handler =====
    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        if check_login_callback(username, password):
            messagebox.showinfo("Thành công", f"Xin chào {username}!")
            show_notepad_callback(root, frm)  # Mở notepad hoặc màn hình chính
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu.")

    # ===== Buttons =====
    ttk.Button(frm, text="Đăng nhập", command=handle_login).pack(pady=10, fill=X)
    ttk.Button(frm, text="Đăng nhập bằng Camera", command=face_detection_callback).pack(pady=10, fill=X)
    ttk.Button(frm, text="Thoát", command=root.destroy).pack(side=BOTTOM, fill=X)

    return frm
