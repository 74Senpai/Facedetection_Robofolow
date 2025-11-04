import cv2
import numpy as np
import json
from insightface.app import FaceAnalysis
from tqdm import tqdm
from database import *

# Khởi tạo model nhận diện khuôn mặt
app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

def extract_face_embedding(image_path: str):
    """
    Trích xuất embedding khuôn mặt từ đường dẫn ảnh.
    (Dùng cho bước thêm dữ liệu người mới)
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"⚠️ Không thể đọc ảnh: {image_path}")
        return None

    faces = app.get(img)
    if len(faces) == 0:
        print(f"⚠️ Không tìm thấy khuôn mặt trong ảnh: {image_path}")
        return None

    face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return face.embedding


def extract_face_embedding_from_array(face_image: np.ndarray):
    """
    Trích xuất embedding từ ảnh numpy array (dùng cho real-time).
    """
    if face_image is None or face_image.size == 0:
        print("⚠️ Ảnh đầu vào trống hoặc không hợp lệ.")
        return None

    img = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

    faces = app.get(img)
    if len(faces) == 0:
        print("⚠️ Không tìm thấy khuôn mặt trong ảnh (array).")
        return None

    face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return face.embedding

def create_face_embeddings_for_user(username: str, image_folder: str):
    user_id = get_user_id(username)
    if not user_id:
        print(f"⚠️ User '{username}' không tồn tại trong DB.")
        return

    from os import listdir, path
    image_files = [f for f in listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    print(f"🧠 Đang xử lý {len(image_files)} ảnh cho user '{username}'...")

    count = 0
    for file in tqdm(image_files):
        img_path = path.join(image_folder, file)
        embedding = extract_face_embedding(img_path)
        if embedding is not None:
            insert_face_vector(user_id, embedding.tolist())
            count += 1

    print(f"✅ Đã lưu {count} vector cho user '{username}'.")

def recognize_user_from_image(image_path: str):
    from numpy.linalg import norm

    def cosine_similarity(v1, v2):
        return np.dot(v1, v2) / (norm(v1) * norm(v2))

    new_emb = extract_face_embedding(image_path)
    if new_emb is None:
        print("⚠️ Không phát hiện khuôn mặt trong ảnh.")
        return None

    data = get_all_face_vectors()
    if not data:
        print("⚠️ Database chưa có vector khuôn mặt.")
        return None

    best_score, best_user_id = 0, None

    for user_id, emb_str in data:
        emb = np.array(json.loads(emb_str))
        score = cosine_similarity(new_emb, emb)
        if score > best_score:
            best_score, best_user_id = score, user_id

    if best_user_id:
        username = get_username_by_id(best_user_id)
        print(f"🔍 Nhận diện: {username} (độ tin cậy: {best_score:.3f})")
        return username, best_score

    print("❌ Không tìm thấy người phù hợp.")
    return None

def recognize_user_from_frame(face_image: np.ndarray, threshold: float = 0.55):
    """
    Nhận diện khuôn mặt trực tiếp từ ảnh numpy array.
    Trả về (username, độ_tin_cậy) hoặc None nếu không khớp.
    """
    if face_image is None or face_image.size == 0:
        print("⚠️ Ảnh khuôn mặt rỗng hoặc không hợp lệ.")
        return None

    new_emb = extract_face_embedding_from_array(face_image)
    if new_emb is None:
        print("⚠️ Không thể trích xuất đặc trưng khuôn mặt (array).")
        return None

    data = get_all_face_vectors()
    if not data:
        print("⚠️ Database chưa có vector khuôn mặt.")
        return None

    from numpy.linalg import norm
    def cosine_similarity(v1, v2):
        return np.dot(v1, v2) / (norm(v1) * norm(v2))

    best_score, best_user = 0, None

    for user_id, emb_str in data:
        emb = np.array(json.loads(emb_str))
        score = cosine_similarity(new_emb, emb)
        if score > best_score:
            best_score, best_user = score, user_id

    if best_user and best_score >= threshold:
        username = get_username_by_id(best_user)
        print(f"✅ Khuôn mặt khớp: {username} ({best_score:.3f})")
        return username, float(best_score)

    print("❌ Không có người nào khớp trong DB.")
    return None
