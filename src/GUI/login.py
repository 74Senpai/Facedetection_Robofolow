from tkinter import *
from tkinter import ttk, messagebox
from repository import User


def create_login_ui(root, face_detection_callback, check_login_callback, show_notepad_callback):
    # Xóa mọi UI cũ
    for widget in root.winfo_children():
        widget.destroy()

    # ===== Cấu hình cửa sổ =====
    root.title("VIP Login")
    root.geometry("340x460")
    root.resizable(False, False)
    root.configure(bg="#181818")  # nền tối nhẹ

    # ===== Frame chính =====
    frm = Frame(root, bg="#181818")
    frm.pack(expand=True, fill=BOTH)

    # ===== Tiêu đề =====
    Label(frm, text="🔐 Đăng nhập", font=("Segoe UI", 22, "bold"),
          bg="#181818", fg="white").pack(pady=(30, 25))

    # ===== Email/SĐT =====
    Label(frm, text="Email hoặc số điện thoại", font=("Segoe UI", 11),
          bg="#181818", fg="#cccccc").pack(anchor="w", padx=30)
    username_entry = Entry(frm, font=("Segoe UI", 12), bg="#2A2A2A",
                           fg="white", insertbackground="white", relief=FLAT)
    username_entry.pack(fill=X, padx=30, pady=(5, 15), ipady=6)

    # ===== Mật khẩu =====
    Label(frm, text="Mật khẩu", font=("Segoe UI", 11),
          bg="#181818", fg="#cccccc").pack(anchor="w", padx=30)
    password_entry = Entry(frm, font=("Segoe UI", 12), bg="#2A2A2A",
                           fg="white", show="*", insertbackground="white", relief=FLAT)
    password_entry.pack(fill=X, padx=30, pady=(5, 25), ipady=6)

    # ===== Hàm xử lý đăng nhập =====
    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        if check_login_callback(username, password):
            messagebox.showinfo("Thành công", f"Xin chào {username}!")
            show_notepad_callback(root, frm, User(username))  # ✅ truyền đúng frm
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu.")

    # ===== Hàm tạo nút (có hover) =====
    def make_button(text, cmd, bg, hover, pady=6):
        def on_enter(e): e.widget.config(bg=hover)
        def on_leave(e): e.widget.config(bg=bg)

        btn = Button(frm, text=text, command=cmd, bg=bg, fg="white",
                     font=("Segoe UI", 11, "bold"), relief=FLAT,
                     cursor="hand2", activebackground=hover,
                     activeforeground="white")
        btn.pack(fill=X, padx=30, pady=pady, ipady=6)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # ===== Các nút =====
    make_button("Đăng nhập", handle_login, "#3a86ff", "#265ecf", pady=8)
    make_button("Đăng nhập bằng Camera", face_detection_callback, "#2a9d8f", "#1d726a", pady=8)
    make_button("Thoát", root.destroy, "#d62828", "#9d0208", pady=15)

    return frm
