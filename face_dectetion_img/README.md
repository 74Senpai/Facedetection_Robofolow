## Thư mục chứa những thư mục chứa ảnh muốn đăng ký nhận diện bằng khuôn mặt

### Cách đăng ký
1. Tạo một thư mục mới sau đó thêm ảnh khuôn mặt muốn đăng ký vào.
**Nên để ảnh cắt sãn hoặc ảnh chỉ có 1 khuôn mặt**

2. Vào scripts chạy script `save_face_embed username folderpath`.
- `username` là tên người dùng đã có trong Database
- `folderpath` là thư mục chưa ảnh được tạo để đăng ký nhận diện khuôn măt
```bash 
    py -m src.scripts.save_face_embed username src\face_dectetion_img\foldername
```

**Lưu ý** : Chỉ nên để số lượng ảnh mỗi khuôn mặt ít và nên để nhiều góc chụp

**Note** : Nếu lỗi không tìm thấy model thì chạy main nếu thấy model được tải về thì chạy lại script
