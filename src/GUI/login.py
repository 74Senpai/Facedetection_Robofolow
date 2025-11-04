import os
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from repository import User

def create_login_ui(root, face_detection_callback, check_login_callback, show_notepad_callback):
    """Tạo giao diện đăng nhập (CustomTkinter, có đổi theme realtime)"""

    # -----------------------------
    # Cấu hình cơ bản
    # -----------------------------
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root.title("VIP Login")
    root.geometry("400x500")
    root.resizable(False, False)

    frm = ctk.CTkFrame(root, corner_radius=20)
    frm.pack(expand=True, fill="both", padx=30, pady=30)
    
    # -----------------------------
    # Đường dẫn icon
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
    ICON_DIR = os.path.join(BASE_DIR, "icon")

    sun_icon = ctk.CTkImage(
        light_image=Image.open(os.path.join(ICON_DIR, "sun.png")),
        dark_image=Image.open(os.path.join(ICON_DIR, "sun.png")),
        size=(22, 22)
    )
    moon_icon = ctk.CTkImage(
        light_image=Image.open(os.path.join(ICON_DIR, "moon.png")),
        dark_image=Image.open(os.path.join(ICON_DIR, "moon.png")),
        size=(22, 22)
    )

    current_mode = ["light"]

    # -----------------------------
    # Hàm đổi trắng/đen
    # -----------------------------
    def update_background():
        mode = ctk.get_appearance_mode()
        bg_color = "#F2F2F2" if mode == "Light" else "#1E1E1E"
        root.configure(bg=bg_color)
        frm.configure(fg_color=bg_color)
    update_background()

    def toggle_theme():
        if current_mode[0] == "light":
            ctk.set_appearance_mode("dark")
            current_mode[0] = "dark"
            theme_btn.configure(image=moon_icon, fg_color=("white", "#000000"))
        else:
            ctk.set_appearance_mode("light")
            current_mode[0] = "light"
            theme_btn.configure(image=sun_icon, fg_color=("White", "#FFFFFF"))
        update_background()

    theme_btn = ctk.CTkButton(
        root,
        width=32,
        height=32,
        corner_radius=20,
        text="",
        image=sun_icon,
        fg_color=("White", "#FFFFFF"),
        hover_color=("#000000", "#FFFFFF"),
        command=toggle_theme
    )
    theme_btn.place(x=340, y=10)

    # -----------------------------
    # Thành phần giao diện
    # -----------------------------
    ctk.CTkLabel(frm, text="🔐 Đăng nhập", font=("Segoe UI", 24, "bold")).pack(pady=(0, 20))

    ctk.CTkLabel(frm, text="Email hoặc số điện thoại:", font=("Segoe UI", 14)).pack(anchor="w")
    username_entry = ctk.CTkEntry(frm, placeholder_text="Nhập email hoặc số điện thoại...",
                                  fg_color=("white", "#2b2b2b"))
    username_entry.pack(fill="x", pady=(5, 15))

    ctk.CTkLabel(frm, text="Mật khẩu:", font=("Segoe UI", 14)).pack(anchor="w")
    password_entry = ctk.CTkEntry(frm, placeholder_text="Nhập mật khẩu...", show="*",
                                  fg_color=("white", "#2b2b2b"))
    password_entry.pack(fill="x", pady=(5, 25))

    # -----------------------------
    # Xử lý đăng nhập
    # -----------------------------
    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        if check_login_callback(username, password):
            messagebox.showinfo("Thành công", f"Xin chào {username}!")
            show_notepad_callback(root, frm, User(username))
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu.")

    # -----------------------------
    # Các nút điều khiển
    # -----------------------------
    ctk.CTkButton(
        frm,
        text="Đăng nhập",
        command=handle_login,
        height=40,
        fg_color=("#2563eb", "#3b82f6"),
        hover_color=("#1d4ed8", "#60a5fa")
    ).pack(fill="x", pady=10)

    ctk.CTkButton(
        frm,
        text="Đăng nhập bằng Camera",
        fg_color=("#16a34a", "#15803d"),
        hover_color=("#22c55e", "#166534"),
        command=face_detection_callback
    ).pack(fill="x", pady=10)

    ctk.CTkButton(
        frm,
        text="Thoát",
        fg_color=("#dc2626", "#b91c1c"),
        hover_color=("#ef4444", "#7f1d1d"),
        command=root.destroy
    ).pack(side="bottom", fill="x", pady=(20, 10))

    return frm
