import os
import threading
from tkinter import Tk
from dotenv import load_dotenv
from services import InferenceService, InferenceWorker, CameraManager
from GUI import create_login_ui, show_notepad
from database import init_db, check_login
from repository import User

load_dotenv()

# Khởi tạo kết nối tới database
init_db()
# 🧠 Khởi tạo inference service
inference = InferenceService(
    api_key= os.getenv("API_KEY"),
    api_url=os.getenv("API_URL"),
    model_id=os.getenv("MODEL_ID"),
    conf_threshold=float(os.getenv("CONF_THRESHOLD", 0.5))
)

root = Tk()

def face_detection():
    cam = CameraManager()
    cam.start()

    infer = InferenceWorker(
        camera=cam,
        inference_engine=inference,
        callback=lambda label, conf: show_notepad(root, frm, User(label)),
        timeout=10,
        interval=0.2
    )

    threading.Thread(target=cam.show_view, daemon=True).start()
    infer.start()

    threading.Thread(target=lambda: monitor(cam, infer), daemon=True).start()

def monitor(cam, infer):
    while cam.running and infer.running:
        pass


frm = create_login_ui(root, face_detection, check_login, show_notepad)
root.mainloop()
