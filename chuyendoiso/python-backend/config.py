#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File cấu hình cho CDS Scanner
Các thông số và cài đặt hệ thống
"""

import os
from pathlib import Path
from typing import Dict, List, Any

# Đường dẫn gốc
BASE_DIR = Path(__file__).parent.parent
PYTHON_BACKEND_DIR = BASE_DIR / "python-backend"

# Cấu hình thư mục
UPLOAD_DIR = PYTHON_BACKEND_DIR / "uploads"
PROCESSED_DIR = PYTHON_BACKEND_DIR / "processed"
RESULTS_DIR = PYTHON_BACKEND_DIR / "results"
TEMP_DIR = PYTHON_BACKEND_DIR / "temp"

# Tạo thư mục nếu chưa có
for directory in [UPLOAD_DIR, PROCESSED_DIR, RESULTS_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# Cấu hình API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_DEBUG = True
API_RELOAD = True

# Cấu hình CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001"
]

# Cấu hình file upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/jpg", 
    "image/png",
    "image/bmp",
    "image/tiff",
    "image/tif"
]

# Cấu hình OCR
TESSERACT_CONFIG = {
    "lang": "vie+eng",
    "config": "--psm 6 --oem 3",
    "timeout": 30
}

# Cấu hình xử lý hình ảnh
IMAGE_PROCESSING = {
    "max_size": 448,
    "max_blocks": 12,
    "use_thumbnail": True,
    "interpolation": "bicubic"
}

# Cấu hình loại giấy tờ
DOCUMENT_TYPES = {
    "hop_dong_lao_dong": {
        "name": "Hợp đồng lao động",
        "description": "Hợp đồng lao động giữa công ty và nhân viên",
        "fields": [
            "ho_ten", "ma_nhan_vien", "chuc_danh", 
            "loai_hop_dong", "thoi_han_hop_dong"
        ],
        "keywords": [
            "HỢP ĐỒNG LAO ĐỘNG", "Hợp đồng lao động", "HĐLĐ",
            "BÊN A", "BÊN B", "Người lao động", "Người sử dụng lao động"
        ]
    },
    "quyet_dinh_bo_nhiem": {
        "name": "Quyết định bổ nhiệm",
        "description": "Quyết định bổ nhiệm chức vụ cho nhân viên",
        "fields": [
            "ho_ten", "chuc_vu_cu", "chuc_vu_moi", 
            "ngay_hieu_luc", "nguoi_ky"
        ],
        "keywords": [
            "QUYẾT ĐỊNH BỔ NHIỆM", "Quyết định bổ nhiệm", "Bổ nhiệm",
            "Chức vụ", "Bổ nhiệm chức vụ"
        ]
    },
    "quyet_dinh_dieu_chuyen": {
        "name": "Quyết định điều chuyển",
        "description": "Quyết định điều chuyển nhân viên giữa các bộ phận",
        "fields": [
            "ho_ten", "bo_phan_cu", "bo_phan_moi", 
            "ngay_dieu_chuyen", "nguoi_ky"
        ],
        "keywords": [
            "QUYẾT ĐỊNH ĐIỀU CHUYỂN", "Quyết định điều chuyển", "Điều chuyển",
            "Bộ phận", "Chuyển công tác"
        ]
    },
    "khen_thuong_ky_luat": {
        "name": "Khen thưởng/Kỷ luật",
        "description": "Quyết định khen thưởng hoặc kỷ luật nhân viên",
        "fields": [
            "ho_ten", "noi_dung_quyet_dinh", "ngay_ban_hanh", 
            "hinh_thuc", "nguoi_ky"
        ],
        "keywords": [
            "QUYẾT ĐỊNH KHEN THƯỞNG", "QUYẾT ĐỊNH KỶ LUẬT",
            "Khen thưởng", "Kỷ luật", "Thưởng", "Phạt"
        ]
    }
}

# Cấu hình regex patterns
REGEX_PATTERNS = {
    "vietnamese_name": r"[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+",
    "employee_code": r"[A-Z0-9]+",
    "date": r"\d{1,2}[/-]\d{1,2}[/-]\d{4}",
    "document_number": r"[A-Z0-9/-]+"
}

# Cấu hình logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": PYTHON_BACKEND_DIR / "logs" / "cds_scanner.log",
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

# Cấu hình database (nếu cần)
DATABASE_CONFIG = {
    "enabled": True,
    "type": "mssql",
    "host": "DESKTOP-SI9D9K9",  # ví dụ: DESKTOP-SI9D9K9 hoặc DESKTOP-SI9D9K9\\SQLEXPRESS
    "database": "CDS",
    "username": "",
    "password": "",
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": True,
    "trust_server_certificate": True,
    "echo": False,
    "sqlite_path": PYTHON_BACKEND_DIR / "data" / "cds_scanner.db"
}

# Cấu hình cache
CACHE_CONFIG = {
    "enabled": True,
    "type": "memory",  # memory, redis
    "ttl": 3600,  # 1 hour
    "max_size": 1000
}

# Cấu hình security
SECURITY_CONFIG = {
    "secret_key": "cds-scanner-secret-key-change-in-production",
    "algorithm": "HS256",
    "access_token_expire_minutes": 30,
    "password_min_length": 8,
    "max_login_attempts": 5,
    "lockout_duration_minutes": 15
}

# Cấu hình performance
PERFORMANCE_CONFIG = {
    "max_workers": 4,
    "max_concurrent_requests": 10,
    "request_timeout": 60,
    "image_processing_timeout": 30,
    "ocr_timeout": 45
}

# Cấu hình monitoring
MONITORING_CONFIG = {
    "enabled": True,
    "metrics_endpoint": "/metrics",
    "health_check_interval": 30,
    "performance_monitoring": True,
    "error_tracking": True
}

# Cấu hình backup
BACKUP_CONFIG = {
    "enabled": True,
    "auto_backup": True,
    "backup_interval_hours": 24,
    "backup_retention_days": 30,
    "backup_directory": PYTHON_BACKEND_DIR / "backups"
}

# Tạo thư mục backup nếu chưa có
BACKUP_CONFIG["backup_directory"].mkdir(exist_ok=True)

# Cấu hình notification
NOTIFICATION_CONFIG = {
    "enabled": False,
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "",
        "password": "",
        "use_tls": True
    },
    "webhook": {
        "url": "",
        "headers": {}
    }
}

# Cấu hình export
EXPORT_CONFIG = {
    "formats": ["json", "csv", "excel"],
    "default_format": "json",
    "include_metadata": True,
    "include_raw_text": False,
    "max_records_per_export": 1000
}

# Hàm tiện ích
def get_config_value(key: str, default: Any = None) -> Any:
    """Lấy giá trị cấu hình"""
    config_map = {
        "upload_dir": UPLOAD_DIR,
        "processed_dir": PROCESSED_DIR,
        "results_dir": RESULTS_DIR,
        "temp_dir": TEMP_DIR,
        "api_host": API_HOST,
        "api_port": API_PORT,
        "max_file_size": MAX_FILE_SIZE,
        "allowed_image_types": ALLOWED_IMAGE_TYPES,
        "document_types": DOCUMENT_TYPES,
        "regex_patterns": REGEX_PATTERNS
    }
    
    return config_map.get(key, default)

def validate_config() -> bool:
    """Kiểm tra tính hợp lệ của cấu hình"""
    try:
        # Kiểm tra thư mục
        for directory in [UPLOAD_DIR, PROCESSED_DIR, RESULTS_DIR, TEMP_DIR]:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
        
        # Kiểm tra port
        if not (1 <= API_PORT <= 65535):
            raise ValueError(f"Port không hợp lệ: {API_PORT}")
        
        # Kiểm tra kích thước file
        if MAX_FILE_SIZE <= 0:
            raise ValueError(f"Kích thước file không hợp lệ: {MAX_FILE_SIZE}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi cấu hình: {e}")
        return False

def print_config_summary():
    """In tóm tắt cấu hình"""
    print("🔧 CDS Scanner Configuration Summary")
    print("=" * 50)
    print(f"📁 Upload Directory: {UPLOAD_DIR}")
    print(f"📁 Processed Directory: {PROCESSED_DIR}")
    print(f"📁 Results Directory: {RESULTS_DIR}")
    print(f"🌐 API Host: {API_HOST}:{API_PORT}")
    print(f"📏 Max File Size: {MAX_FILE_SIZE / (1024*1024):.1f} MB")
    print(f"📋 Document Types: {len(DOCUMENT_TYPES)}")
    print(f"🔍 OCR Language: {TESSERACT_CONFIG['lang']}")
    print("✅ Configuration validated successfully!")

if __name__ == "__main__":
    # Test cấu hình
    if validate_config():
        print_config_summary()
    else:
        print("❌ Configuration validation failed!")
