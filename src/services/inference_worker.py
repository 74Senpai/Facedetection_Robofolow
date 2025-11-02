import time
import threading

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
            # timeout
            if time.time() - start_time > self.timeout:
                print(f"⌛ Hết thời gian {self.timeout}s mà không phát hiện được khuôn mặt.")
                self.stop()
                break

            # interval infer
            if time.time() - last_time >= self.interval:
                frame = self.camera.get_frame()
                if frame is not None:
                    results = self.inference.infer_frame(frame)
                    if results:
                        label = results[0].get("class", "Unknown")
                        conf = results[0].get("confidence", 0)

                        if conf >= 0.8:
                            print(f"✅ Face recognized! Label: {label}, Confidence: {conf:.2f}")
                            self.recognized = True
                            self.callback(label, conf)
                            self.stop()
                            break
                        else:
                            print(f"⚠️ Phát hiện khuôn mặt nhưng độ tin cậy thấp ({conf:.2f})")

                last_time = time.time()

            time.sleep(0.01)

        print("🛑 Inference loop stopped.")

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
