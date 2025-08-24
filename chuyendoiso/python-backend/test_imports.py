#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File test để kiểm tra việc import các thư viện Python đã cài đặt
"""

def test_imports():
    """Kiểm tra việc import các thư viện"""
    try:
        print("🔍 Đang kiểm tra các thư viện...")
        
        # Test PyTorch
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        
        # Test Torchvision
        import torchvision
        print(f"✅ Torchvision: {torchvision.__version__}")
        
        # Test Transformers
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
        
        # Test PIL/Pillow
        from PIL import Image
        print(f"✅ PIL/Pillow: {Image.__version__}")
        
        # Test NumPy
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
        
        # Test OpenCV
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
        
        # Test FastAPI
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
        
        # Test Uvicorn
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
        
        print("\n🎉 Tất cả các thư viện đã được import thành công!")
        return True
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi khác: {e}")
        return False

def test_basic_functionality():
    """Kiểm tra chức năng cơ bản của các thư viện"""
    try:
        print("\n🧪 Đang kiểm tra chức năng cơ bản...")
        
        # Test PyTorch
        import torch
        x = torch.randn(3, 3)
        print(f"✅ PyTorch tensor: {x.shape}")
        
        # Test NumPy
        import numpy as np
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✅ NumPy array: {arr}")
        
        # Test PIL
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        print(f"✅ PIL Image: {img.size}")
        
        print("🎉 Tất cả các chức năng cơ bản hoạt động bình thường!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi chức năng: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Bắt đầu kiểm tra các thư viện Python...\n")
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎊 Hoàn thành! Tất cả các thư viện đã sẵn sàng sử dụng.")
        else:
            print("\n⚠️ Có vấn đề với chức năng của một số thư viện.")
    else:
        print("\n❌ Có vấn đề với việc import thư viện.") 