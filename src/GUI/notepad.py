from tkinter import Label,Button,Frame,BOTH,WORD,Text,END,FLAT
from tkinter import messagebox
from src.repository import User


def show_notepad(root, frm, user: User):
    """Hiển thị giao diện notepad"""
    # Dọn sạch frame cũ
    for widget in frm.winfo_children():
        widget.destroy()

    root.geometry("500x500")
    root.title(f"Mini Notepad - {user.username}")
    root.configure(bg="#181818")

    # ===== Tiêu đề =====
    title = Label(frm,
                  text=f"📝 Ghi chú của {user.username}",
                  font=("Segoe UI", 18, "bold"),
                  bg="#181818", fg="white")
    title.pack(pady=(10, 10))

    # ===== Ô nhập văn bản =====
    text = Text(frm,
                wrap=WORD,
                font=("Consolas", 12),
                bg="#222222",
                fg="white",
                insertbackground="white",
                relief=FLAT,
                padx=10,
                pady=10)
    text.pack(expand=True, fill=BOTH, padx=10, pady=(0, 10))

    # Hiển thị ghi chú đã lưu nếu có
    if user.note:
        text.insert(END, user.note)

    # Trạng thái lưu
    saved_state = {"saved": True}

    def on_text_change(event=None):
        saved_state["saved"] = False

    text.bind("<Key>", on_text_change)

    # ===== Chức năng =====
    def save_note():
        """Lưu nội dung ghi chú"""
        new_note = text.get("1.0", END).strip()
        user.update_note(new_note)
        saved_state["saved"] = True
        messagebox.showinfo("💾 Đã lưu", "Ghi chú đã được lưu thành công!")

    def confirm_exit():
        """Hỏi xác nhận thoát"""
        if not saved_state["saved"]:
            res = messagebox.askyesnocancel(
                "Xác nhận thoát",
                "Ghi chú của bạn chưa được lưu.\nBạn có muốn lưu trước khi thoát không?",
                icon="warning"
            )
            if res is None:
                return
            elif res:
                save_note()
        root.destroy()
    # ===== Nút Lưu =====
    
    Button(frm, text="💾 Lưu", command=save_note, bg="#3a86ff", fg="white", font=("Segoe UI", 11, "bold"), relief=FLAT, cursor="hand2").pack(side="bottom", fill="x", padx=10, pady=10, ipady=6)

    # Khi nhấn nút X
    root.protocol("WM_DELETE_WINDOW", confirm_exit)
