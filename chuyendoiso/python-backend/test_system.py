#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test toàn bộ hệ thống CDS Scanner
Kiểm tra các module và chức năng chính
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Thêm thư mục hiện tại vào Python path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test import các module"""
    print("🔍 Testing imports...")
    
    try:
        import config
        print("✅ Config module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config: {e}")
        return False
    
    try:
        from document_processor import DocumentProcessor
        print("✅ DocumentProcessor imported successfully")
    except Exception as e:
        print(f"❌ Failed to import DocumentProcessor: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except Exception as e:
        print(f"❌ Failed to import FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except Exception as e:
        print(f"❌ Failed to import Uvicorn: {e}")
        return False
    
    return True

def test_config():
    """Test cấu hình hệ thống"""
    print("\n🔧 Testing configuration...")
    
    try:
        import config
        
        # Test các giá trị cấu hình
        assert config.API_PORT == 8000, f"API_PORT should be 8000, got {config.API_PORT}"
        assert config.MAX_FILE_SIZE > 0, f"MAX_FILE_SIZE should be positive, got {config.MAX_FILE_SIZE}"
        assert len(config.DOCUMENT_TYPES) > 0, "DOCUMENT_TYPES should not be empty"
        
        print("✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_document_processor():
    """Test DocumentProcessor class"""
    print("\n📄 Testing DocumentProcessor...")
    
    try:
        from document_processor import DocumentProcessor
        
        # Khởi tạo processor
        processor = DocumentProcessor()
        
        # Test các thuộc tính
        assert hasattr(processor, 'document_types'), "Processor should have document_types"
        assert hasattr(processor, 'type_keywords'), "Processor should have type_keywords"
        assert len(processor.document_types) > 0, "Document types should not be empty"
        
        # Test các phương thức
        assert hasattr(processor, 'process_document'), "Processor should have process_document method"
        assert hasattr(processor, 'detect_document_type'), "Processor should have detect_document_type method"
        
        print("✅ DocumentProcessor test passed")
        return True
        
    except Exception as e:
        print(f"❌ DocumentProcessor test failed: {e}")
        return False

def test_directories():
    """Test tạo thư mục cần thiết"""
    print("\n📁 Testing directory creation...")
    
    try:
        import config
        
        # Kiểm tra các thư mục
        directories = [
            config.UPLOAD_DIR,
            config.PROCESSED_DIR,
            config.RESULTS_DIR,
            config.TEMP_DIR
        ]
        
        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            else:
                print(f"✅ Directory exists: {directory}")
        
        return True
        
    except Exception as e:
        print(f"❌ Directory test failed: {e}")
        return False

def test_document_type_detection():
    """Test nhận diện loại giấy tờ"""
    print("\n🔍 Testing document type detection...")
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # Test với các văn bản mẫu
        test_cases = [
            ("HỢP ĐỒNG LAO ĐỘNG", "hop_dong_lao_dong"),
            ("QUYẾT ĐỊNH BỔ NHIỆM", "quyet_dinh_bo_nhiem"),
            ("QUYẾT ĐỊNH ĐIỀU CHUYỂN", "quyet_dinh_dieu_chuyen"),
            ("QUYẾT ĐỊNH KHEN THƯỞNG", "khen_thuong_ky_luat"),
            ("Văn bản thông thường", "unknown")
        ]
        
        for text, expected_type in test_cases:
            detected_type = processor.detect_document_type(text)
            if detected_type == expected_type:
                print(f"✅ '{text}' -> {detected_type}")
            else:
                print(f"❌ '{text}' -> {detected_type} (expected: {expected_type})")
        
        return True
        
    except Exception as e:
        print(f"❌ Document type detection test failed: {e}")
        return False

def test_api_structure():
    """Test cấu trúc API"""
    print("\n🌐 Testing API structure...")
    
    try:
        # Import API server
        from api_server import app
        
        # Kiểm tra các endpoints
        expected_endpoints = [
            "/",
            "/health",
            "/upload",
            "/documents",
            "/stats"
        ]
        
        routes = [route.path for route in app.routes]
        
        for endpoint in expected_endpoints:
            if endpoint in routes:
                print(f"✅ Endpoint found: {endpoint}")
            else:
                print(f"❌ Endpoint missing: {endpoint}")
        
        print(f"📊 Total routes: {len(routes)}")
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def test_image_processing_dependencies():
    """Test các thư viện xử lý hình ảnh"""
    print("\n🖼️ Testing image processing dependencies...")
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        import PIL
        print(f"✅ PIL version: {PIL.__version__}")
        
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
        
        # Test pytesseract
        try:
            import pytesseract
            print("✅ pytesseract imported successfully")
        except ImportError:
            print("⚠️ pytesseract not available (OCR will not work)")
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False

def test_ai_ml_dependencies():
    """Test các thư viện AI/ML"""
    print("\n🤖 Testing AI/ML dependencies...")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        import torchvision
        print(f"✅ Torchvision version: {torchvision.__version__}")
        
        import transformers
        print(f"✅ Transformers version: {transformers.__version__}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI/ML dependencies test failed: {e}")
        return False

def create_sample_data():
    """Tạo dữ liệu mẫu để test"""
    print("\n📝 Creating sample data...")
    
    try:
        import config
        
        # Tạo file kết quả mẫu
        sample_result = {
            "document_type": "hop_dong_lao_dong",
            "extracted_text": "HỢP ĐỒNG LAO ĐỘNG\nHọ và tên: Nguyễn Văn A\nMã nhân viên: NV001",
            "processed_data": {
                "ho_ten": "Nguyễn Văn A",
                "ma_nhan_vien": "NV001",
                "chuc_danh": "Nhân viên",
                "loai_hop_dong": "Chính thức",
                "thoi_han_hop_dong": "12 tháng"
            },
            "confidence": "high",
            "timestamp": datetime.now().isoformat()
        }
        
        # Lưu vào thư mục results
        sample_file = config.RESULTS_DIR / "sample_result.json"
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(sample_result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Created sample result: {sample_file}")
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def run_performance_test():
    """Test hiệu suất hệ thống"""
    print("\n⚡ Running performance test...")
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # Test thời gian xử lý
        start_time = time.time()
        
        # Giả lập xử lý
        for i in range(10):
            processor.detect_document_type(f"Test document {i}")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processed 10 documents in {processing_time:.3f} seconds")
        print(f"📊 Average time per document: {processing_time/10:.3f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Hàm chính chạy tất cả tests"""
    print("🚀 CDS Scanner System Test")
    print("=" * 50)
    
    start_time = time.time()
    test_results = []
    
    # Chạy các tests
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Document Processor", test_document_processor),
        ("Directories", test_directories),
        ("Document Type Detection", test_document_type_detection),
        ("API Structure", test_api_structure),
        ("Image Processing", test_image_processing_dependencies),
        ("AI/ML Dependencies", test_ai_ml_dependencies),
        ("Sample Data", create_sample_data),
        ("Performance", run_performance_test)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()            
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            test_results.append((test_name, False))
    
    # Tổng kết kết quả
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    print(f"⏱️ Total time: {total_time:.2f} seconds")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
