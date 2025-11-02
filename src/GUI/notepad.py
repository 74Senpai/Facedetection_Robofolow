from tkinter import *
from tkinter import ttk

def show_notepad(root, frm):
    """Hiển thị giao diện notepad"""
    for widget in frm.winfo_children():
        widget.destroy()
    root.geometry("300x400")
    root.title("Mini Notepad")

    text = Text(frm, wrap=WORD, font=("Arial", 12))
    text.pack(expand=True, fill=BOTH, padx=5, pady=5)

    ttk.Button(frm, text="Thoát", command=root.destroy).pack(pady=5, fill=X, padx=5)
