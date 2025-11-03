from tkinter import *
from tkinter import ttk, messagebox
from repository import User

def show_notepad(root, frm, user: User):
    """Hiển thị giao diện notepad"""
    for widget in frm.winfo_children():
        widget.destroy()

    root.geometry("400x500")
    root.title(f"Mini Notepad - {user.username}")

    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=1)

    text = Text(frm, wrap=WORD, font=("Arial", 12))
    text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    if user.note:
        text.insert(END, user.note)

    saved_state = {"saved": True}

    def on_text_change(event=None):
        saved_state["saved"] = False

    text.bind("<Key>", on_text_change)

    def save_note():
        """Lưu lại note vào DB"""
        new_note = text.get("1.0", END).strip()
        user.update_note(new_note)
        saved_state["saved"] = True
        messagebox.showinfo("Đã lưu", "Ghi chú đã được lưu thành công!")

    def on_close():
        """Xử lý khi nhấn X"""
        if not saved_state["saved"]:
            res = messagebox.askyesnocancel(
                "Xác nhận thoát",
                "Ghi chú của bạn chưa được lưu.\nBạn có muốn lưu trước khi thoát không?"
            )
            if res is None:
                return
            elif res: 
                save_note()
        root.destroy()

    def save_and_close():
        """Nút 'Thoát' — luôn lưu rồi thoát"""
        save_note()
        root.destroy()

    btn = ttk.Button(frm, text="💾 Lưu và Thoát", command=save_and_close)
    btn.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_close)
