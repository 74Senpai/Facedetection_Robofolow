import time
import threading
import config

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
                        if self._process_inference_results(frame, results):
                            return
                last_time = time.time()

            time.sleep(0.01)

        print("🛑 Inference loop stopped.")

    def _process_inference_results(self, frame, results):
        """Xử lý đầu ra YOLO, cắt khuôn mặt và nhận diện."""
        from services import recognize_user_from_frame
        conf = results[0].get("confidence", 0)

        if conf < config.FACE_DETEC_THRESHOLD:
            print(f"⚠️ YOLO phát hiện khuôn mặt nhưng độ tin cậy thấp ({conf:.2f})")
            return False

        print(f"👁️ Phát hiện khuôn mặt (YOLO conf={conf:.2f})")

        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                face = frame[y1:y2, x1:x2]

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
