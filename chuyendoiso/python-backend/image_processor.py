import os
import numpy as np
import torch
import torchvision
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
import transformers

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def build_transform(input_size):
    """Xây dựng pipeline transform cho hình ảnh"""
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    """Tìm tỷ lệ khung hình gần nhất với tỷ lệ hiện tại"""
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    """Tiền xử lý hình ảnh động với việc chia thành các khối"""
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height
    
    # Tạo danh sách các tỷ lệ khung hình mục tiêu
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) 
        for i in range(1, n + 1) 
        for j in range(1, n + 1) 
        if i * j <= max_num and i * j >= min_num
    )
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])
    
    # Tìm tỷ lệ khung hình gần nhất
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size
    )
    
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]
    
    # Thay đổi kích thước hình ảnh
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    
    # Chia hình ảnh thành các khối
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    
    assert len(processed_images) == blocks
    
    # Thêm thumbnail nếu cần
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    
    return processed_images

def load_image(image_file, input_size=448, max_num=12):
    """Tải và xử lý hình ảnh từ file"""
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    
    # Tiền xử lý hình ảnh
    images = dynamic_preprocess(
        image, 
        image_size=input_size, 
        use_thumbnail=True, 
        max_num=max_num
    )
    
    # Chuyển đổi thành tensor
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    
    return pixel_values

def process_image_file(image_path, input_size=448, max_num=12):
    """Hàm tiện ích để xử lý file hình ảnh"""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Không tìm thấy file: {image_path}")
        
        # Tải và xử lý hình ảnh
        pixel_values = load_image(image_path, input_size, max_num)
        
        print(f"Đã xử lý hình ảnh: {image_path}")
        print(f"Kích thước tensor: {pixel_values.shape}")
        print(f"Số khối hình ảnh: {pixel_values.shape[0]}")
        
        return pixel_values
        
    except Exception as e:
        print(f"Lỗi khi xử lý hình ảnh: {e}")
        return None

# Ví dụ sử dụng
if __name__ == "__main__":
    # Kiểm tra xem có thể import các thư viện không
    print("Kiểm tra các thư viện đã cài đặt:")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Torchvision version: {torchvision.__version__}")
    print(f"Transformers version: {transformers.__version__}")
    print(f"PIL version: {Image.__version__}")
    print(f"NumPy version: {np.__version__}")
    
    print("\nCác hàm đã sẵn sàng sử dụng:")
    print("- build_transform(input_size)")
    print("- find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size)")
    print("- dynamic_preprocess(image, min_num, max_num, image_size, use_thumbnail)")
    print("- load_image(image_file, input_size, max_num)")
    print("- process_image_file(image_path, input_size, max_num)") 