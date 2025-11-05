import time
import threading
import src.config as config

class InferenceWorker:
    def __init__(self, camera, inference_engine, callback, interval=0.2, timeout=10):
        self.camera = camera
        self.inference = inference_engine
        self.callback = callback
        self.interval = interval
        self.timeout = timeout
        self.running = False
        self.recognized = False
        self._thread = None
        self._lock = threading.Lock()

    def start(self):
        with self._lock:
            if self.running:
                print("⚠️ InferenceWorker is already running.")
                return

            if not self.camera or not self.camera.running:
                print("❌ Camera is not active.")
                return

            self.running = True
            self.recognized = False
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
            print("🚀 InferenceWorker thread started.")

    def _loop(self):
        start_time = time.time()
        last_time = 0

        while self.running and not self.recognized:
            if time.time() - start_time > self.timeout:
                print(f"⌛ Hết thời gian {self.timeout}s mà không phát hiện được khuôn mặt.")
                self.stop()
                break

            if time.time() - last_time >= self.interval:
                frame = self.camera.get_frame()
                if frame is not None:
                    results = self.inference.infer_frame(frame)
                    if results:
                        print(results)
                        if self._process_inference_results(frame, results):
                            return
                last_time = time.time()

            time.sleep(0.01)

        print("🛑 Inference loop stopped.")

    def _process_inference_results(self, frame, results, padding_ratio=0.2):
        """Xử lý đầu ra YOLO, cắt khuôn mặt với padding và nhận diện."""
        from src.services import recognize_user_from_frame

        if not results:
            return False

        frame_h, frame_w = frame.shape[:2]

        for r in results:
            conf = r.get("confidence", 0)
            if conf < config.FACE_DETEC_THRESHOLD:
                print(f"⚠️ YOLO phát hiện khuôn mặt nhưng độ tin cậy thấp ({conf:.2f})")
                continue

            print(f"👁️ Phát hiện khuôn mặt (YOLO conf={conf:.2f})")

            # Lấy tọa độ gốc
            x1 = int(r['x'])
            y1 = int(r['y'])
            x2 = int(x1 + r['width'])
            y2 = int(y1 + r['height'])

            # Tính padding
            pad_w = int((x2 - x1) * padding_ratio)
            pad_h = int((y2 - y1) * padding_ratio)

            # Mở rộng bounding box và đảm bảo không vượt quá kích thước ảnh
            x1_pad = max(0, x1 - pad_w)
            y1_pad = max(0, y1 - pad_h)
            x2_pad = min(frame_w, x2 + pad_w)
            y2_pad = min(frame_h, y2 + pad_h)

            # Cắt khuôn mặt với padding
            face = frame[y1_pad:y2_pad, x1_pad:x2_pad].copy()  # đảm bảo là numpy array độc lập

            recognized_user = recognize_user_from_frame(face, threshold=config.FACE_RECO_THRESHOLD)

            if recognized_user:
                username, match_conf = recognized_user
                if self._handle_recognition_result(username, match_conf):
                    return True
            else:
                print("❌ Không khớp với người dùng nào trong DB.")

        return False

    def _handle_recognition_result(self, username: str, match_conf: float) -> bool:
        """Xử lý khi có kết quả nhận diện người dùng."""
        if match_conf >= config.FACE_RECO_THRESHOLD:
            print(f"✅ Nhận diện thành công: {username} ({match_conf:.3f})")
            self.recognized = True
            self.callback(username, match_conf)
            self.stop()
            return True
        else:
            print(f"⚠️ Nhận diện được nhưng độ tin cậy thấp ({match_conf:.3f}), thử lại...")
            return False

    def stop(self):
        """Dừng vòng lặp nhận diện"""
        with self._lock:
            if not self.running:
                return

            self.running = False
            self.camera.stop()
            current = threading.current_thread()
            if self._thread and self._thread.is_alive() and self._thread != current:
                self._thread.join(timeout=1)

            print("✅ InferenceWorker stopped cleanly.")
