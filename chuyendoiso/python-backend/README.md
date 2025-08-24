# CDS Python Backend - Xử lý hình ảnh AI/ML

Backend Python này cung cấp các chức năng xử lý hình ảnh nâng cao sử dụng PyTorch, Transformers và các thư viện AI/ML hiện đại.

## 🚀 Cài đặt

Các thư viện đã được cài đặt sẵn:

```bash
# Các thư viện chính
torch>=2.0.0          # PyTorch - Deep Learning framework
torchvision>=0.15.0   # Torchvision - Computer Vision tools
timm>=0.9.0           # Timm - Image Models
transformers>=4.30.0  # Hugging Face Transformers

# Thư viện hỗ trợ
Pillow>=9.0.0         # PIL - Image processing
numpy>=1.21.0         # NumPy - Numerical computing
opencv-python>=4.8.0  # OpenCV - Computer vision

# Web framework
fastapi>=0.100.0      # FastAPI - Modern web framework
uvicorn>=0.23.0       # Uvicorn - ASGI server
python-multipart>=0.0.6 # File upload support
```

## 📁 Cấu trúc thư mục

```
python-backend/
├── requirements.txt      # Danh sách thư viện
├── image_processor.py   # Module xử lý hình ảnh chính
├── test_imports.py      # File test thư viện
└── README.md           # Hướng dẫn này
```

## 🔧 Sử dụng

### 1. Kiểm tra thư viện

```bash
py test_imports.py
```

### 2. Import và sử dụng

```python
from image_processor import process_image_file, load_image

# Xử lý file hình ảnh
pixel_values = process_image_file("path/to/image.jpg")

# Hoặc tải trực tiếp
pixel_values = load_image("path/to/image.jpg", input_size=448, max_num=12)
```

## 🖼️ Các hàm chính

### `build_transform(input_size)`
- Xây dựng pipeline transform cho hình ảnh
- Chuẩn hóa theo ImageNet mean/std
- Thay đổi kích thước và chuyển đổi thành tensor

### `find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size)`
- Tìm tỷ lệ khung hình gần nhất
- Tối ưu hóa việc chia hình ảnh thành các khối

### `dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False)`
- Tiền xử lý hình ảnh động
- Chia hình ảnh thành các khối có kích thước cố định
- Tự động tìm tỷ lệ khung hình tối ưu

### `load_image(image_file, input_size=448, max_num=12)`
- Tải và xử lý hình ảnh từ file
- Trả về tensor PyTorch đã được chuẩn hóa

### `process_image_file(image_path, input_size=448, max_num=12)`
- Hàm tiện ích để xử lý file hình ảnh
- Bao gồm xử lý lỗi và thông tin debug

## 🎯 Ứng dụng

Backend này có thể được sử dụng cho:

1. **Tiền xử lý hình ảnh** cho các mô hình AI/ML
2. **Chia hình ảnh** thành các khối nhỏ để xử lý
3. **Chuẩn hóa dữ liệu** theo chuẩn ImageNet
4. **Tích hợp với frontend** Next.js hiện tại
5. **API xử lý hình ảnh** sử dụng FastAPI

## 🔗 Tích hợp với Frontend

Để tích hợp với frontend Next.js, bạn có thể:

1. Tạo API endpoints sử dụng FastAPI
2. Xử lý hình ảnh upload từ frontend
3. Trả về kết quả xử lý dưới dạng JSON
4. Sử dụng kết quả để cải thiện OCR

## 🚀 Chạy

```bash
# Kiểm tra thư viện
py test_imports.py

# Chạy module chính
py image_processor.py
```

## 📝 Ghi chú

- Tất cả các thư viện đã được cài đặt và test thành công
- Hỗ trợ Python 3.13.4
- Tương thích với Windows
- Sẵn sàng tích hợp với dự án CDS Scanner 