import sys
from src.database import init_db
from src.services import facedetection_service

if len(sys.argv) < 2:
    print("Cách dùng: python save_face_embed.py username image_folder")
    sys.exit()

username = sys.argv[1]
image_folder = sys.argv[2]

print(f"Username: {username}")
print(f"Thư mục ảnh: {image_folder}")

init_db()
facedetection_service.create_face_embeddings_for_user(username=username, image_folder=image_folder)


