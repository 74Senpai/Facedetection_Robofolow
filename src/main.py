import threading
from tkinter import Tk
from src.services import InferenceService, InferenceWorker, CameraManager
from src.GUI import create_login_ui, show_notepad
from src.database import init_db, check_login
from src.repository import User
from src.config import API_KEY, API_URL, MODEL_ID, FACE_DETEC_THRESHOLD


# Khởi tạo kết nối tới database
init_db()
# 🧠 Khởi tạo inference service
inference = InferenceService(
    api_key = API_KEY,
    api_url = API_URL,
    model_id = MODEL_ID,
    conf_threshold= FACE_DETEC_THRESHOLD
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
