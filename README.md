# 📝 Ứng dụng Notepad Bảo Mật Thông Tin

Ứng dụng **Notepad** được phát triển nhằm **bảo mật dữ liệu cá nhân**, hỗ trợ **đăng nhập bằng hai phương thức**:
- 🔐 **Mật khẩu (username & password)**
- 🧠 **Nhận diện khuôn mặt (Face Recognition)**

---

## 🔐 Phương Thức Đăng Nhập

### 1️⃣ Đăng nhập bằng Mật khẩu
Người dùng nhập **tên đăng nhập (username)** và **mật khẩu (password)** để truy cập ứng dụng.

### 2️⃣ Đăng nhập bằng Khuôn mặt
Ứng dụng sử dụng **mô hình AI** được huấn luyện trên **Roboflow** để nhận diện khuôn mặt và xác thực người dùng.

---

## ⚙️ Yêu cầu hệ thống (gợi ý)
- Python **3.8 – 3.12**
- pip (package installer)
- Kết nối Internet (để gọi API Roboflow)
- Camera (nếu dùng chức năng nhận diện khuôn mặt trên máy)

---

## ⚙️ Hướng Dẫn Cài Đặt

### Bước 1: Tải mã nguồn
Bạn có thể tải dự án về máy bằng Git hoặc cách khác:
```bash
git clone https://github.com/74Senpai/Facedetection_Robofolow.git
cd Facedetection_Robofolow
```

---

### Bước 2: Tạo và kích hoạt virtual environment (khuyến nghị)
Tạo môi trường ảo để tránh xung đột package.

Windows (PowerShell):
```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1
```
Windows (cmd):
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Bước 3: Cài đặt các thư viện cần thiết
Khi đã ở trong folder dự án và đã kích hoạt virtual environment, chạy:
```bash
pip install -r requirements.txt
```
Nếu bạn gặp lỗi quyền, thử:
```bash
pip install --user -r requirements.txt
```
hoặc đảm bảo virtual environment đang active.

---

### Bước 4: Cấu hình biến môi trường
Tạo file `.env` từ mẫu `.env.example` và điền các biến môi trường cần thiết.  
Ví dụ file `.env` có thể gồm:

```dotenv
API_KEY="your_api_key_here"
API_URL="https://serverless.roboflow.com"
MODEL_ID="your_model_id_here"
CONF_THRESHOLD="0.8"
```

Lưu ý: tên biến tùy thuộc vào cách project bạn implement — kiểm tra `.env.example` để biết chính xác tên biến.

---

### Bước 5: Kết nối và cấu hình Roboflow
1. Đăng nhập vào **Roboflow** (hoặc tạo tài khoản).
2. Vào **Dataset → Deployments → Hosted Image Inference**.
3. Chọn **deployment** (hoặc tạo deployment mới) cho model bạn muốn dùng.
4. Sao chép các thông tin: `api_key`, `api_url`, `model_id`.
5. Dán các giá trị này vào file `.env` tương ứng.

---

### Bước 6: Chạy ứng dụng
Từ thư mục gốc của dự án, chạy:
```bash
python src/main.py
```

Hoặc nếu bạn trên macOS/Linux và Python 3 là `python3`:

```bash
python3 src/main.py```


---

## 💡 Ghi chú & mẹo
- Kiểm tra phiên bản Python hiện tại:
  python --version
- Nếu gặp lỗi liên quan tới package, hãy thử cập nhật pip:
```bash
pip install --upgrade pip
```

---

## 📁 Cấu Trúc Thư Mục Dự Án (Gợi ý)

Facedetection_Robofolow/
```txt
│
├── src/
│   ├── main.py
│   ├── ui/                # Giao diện người dùng
│   ├── face_recognition/  # Xử lý nhận diện khuôn mặt (Roboflow API interaction)
│   └── utils/             # Các hàm hỗ trợ
│
├── .env.example
├── requirements.txt
└── README.md
```
---

## 🧪 Kiểm thử (Testing)
- Kiểm tra chức năng đăng nhập bằng password: tạo user test, thử đăng nhập đúng/sai.
- Kiểm tra chức năng nhận diện khuôn mặt: dùng camera để xác thực user có trong dataset hay không.
- Kiểm tra log/exception để phát hiện lỗi API hoặc kết nối.


## 🔒 Bảo mật
- Không commit file `.env` chứa api_key hoặc secret lên public repo.
- Sử dụng `.gitignore` để loại trừ `.env` và folder `.venv`.
