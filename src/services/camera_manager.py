import cv2
import threading
import time

class CameraManager:
    def __init__(self, camera_source=0):
        self.cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
        self.running = False
        self.frame = None
        self.lock = threading.Lock()
        self._thread = None  # giữ thread hiện tại

    def start(self):
        """Khởi chạy camera nếu chưa chạy"""
        if self.running:
            print("⚠️ Camera is already running.")
            return

        if not self.cap.isOpened():
            print("❌ Cannot open camera source.")
            return

        self.running = True
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        print("🚀 Camera thread started.")

    def _update_loop(self):
        """Luồng nội bộ đọc frame từ camera"""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            else:
                print("⚠️ Failed to read frame.")
                break
            time.sleep(0.01)
        print("🛑 Camera update loop stopped.")

    def get_frame(self):
        """Lấy frame mới nhất"""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        """Dừng camera"""
        if not self.running:
            print("⚠️ Camera already stopped.")
            return

        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)

        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Camera stopped and resources released.")

    def show_view(self, window_name="Camera"):
        """Hiển thị khung hình camera"""
        if not self.running:
            print("⚠️ Camera is not running. Call start() first.")
            return

        print(f"📷 Showing camera view ({window_name})... Press 'q' to quit.")
        while self.running:
            frame = self.get_frame()
            if frame is not None:
                cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break
        print("🪟 Camera view loop exited.")
