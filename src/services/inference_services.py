import cv2
import os
from inference_sdk import InferenceHTTPClient

class InferenceService:
    def __init__(self, api_key, api_url, model_id, conf_threshold=0.8):
        self.client = InferenceHTTPClient(
            api_url=api_url,
            api_key=api_key
        )
        self.model_id = model_id
        self.conf_threshold = conf_threshold

    def infer_frame(self, frame):
        tmp_path = "assets/temp_frame.jpg"
        cv2.imwrite(tmp_path, frame)

        try:
            resp = self.client.infer(tmp_path, model_id=self.model_id)
            predictions = resp.get("predictions", [])
            filtered = [
                p for p in predictions
                if p.get("confidence", 0) >= self.conf_threshold
            ]
            return filtered
        except Exception as e:
            print("Inference error:", e)
            return []
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
