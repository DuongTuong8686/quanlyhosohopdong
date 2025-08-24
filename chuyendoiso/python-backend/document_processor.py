#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý giấy tờ chuyên biệt cho CDS Scanner
Xử lý các loại giấy tờ nội bộ công ty với OCR thông minh
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Cấu hình Tesseract cho tiếng Việt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@dataclass
class EmployeeInfo:
    """Thông tin nhân viên cơ bản"""
    ho_ten: str = ""
    ma_nhan_vien: str = ""
    chuc_danh: str = ""
    bo_phan: str = ""

@dataclass
class LaborContract:
    """Thông tin hợp đồng lao động"""
    ho_ten: str = ""
    ma_nhan_vien: str = ""
    chuc_danh: str = ""
    loai_hop_dong: str = ""
    thoi_han_hop_dong: str = ""
    ngay_ky: str = ""
    ngay_hieu_luc: str = ""
    nguoi_ky: str = ""

@dataclass
class AppointmentDecision:
    """Thông tin quyết định bổ nhiệm"""
    ho_ten: str = ""
    chuc_vu_cu: str = ""
    chuc_vu_moi: str = ""
    ngay_hieu_luc: str = ""
    nguoi_ky: str = ""
    so_quyet_dinh: str = ""

@dataclass
class TransferDecision:
    """Thông tin quyết định điều chuyển"""
    ho_ten: str = ""
    bo_phan_cu: str = ""
    bo_phan_moi: str = ""
    chuc_vu: str = ""
    ngay_dieu_chuyen: str = ""
    nguoi_ky: str = ""
    so_quyet_dinh: str = ""

@dataclass
class RewardDiscipline:
    """Thông tin khen thưởng/kỷ luật"""
    ho_ten: str = ""
    noi_dung_quyet_dinh: str = ""
    ngay_ban_hanh: str = ""
    hinh_thuc: str = ""  # "khen_thuong" hoặc "ky_luat"
    so_quyet_dinh: str = ""
    nguoi_ky: str = ""

class DocumentProcessor:
    """Xử lý giấy tờ chuyên biệt"""
    
    def __init__(self):
        self.document_types = {
            "hop_dong_lao_dong": self._extract_labor_contract,
            "quyet_dinh_bo_nhiem": self._extract_appointment_decision,
            "quyet_dinh_dieu_chuyen": self._extract_transfer_decision,
            "khen_thuong_ky_luat": self._extract_reward_discipline
        }
        
        # Từ khóa nhận diện loại giấy tờ
        self.type_keywords = {
            "hop_dong_lao_dong": [
                "HỢP ĐỒNG LAO ĐỘNG", "Hợp đồng lao động", "HĐLĐ",
                "BÊN A", "BÊN B", "Người lao động", "Người sử dụng lao động"
            ],
            "quyet_dinh_bo_nhiem": [
                "QUYẾT ĐỊNH BỔ NHIỆM", "Quyết định bổ nhiệm", "Bổ nhiệm",
                "Chức vụ", "Bổ nhiệm chức vụ"
            ],
            "quyet_dinh_dieu_chuyen": [
                "QUYẾT ĐỊNH ĐIỀU CHUYỂN", "Quyết định điều chuyển", "Điều chuyển",
                "Bộ phận", "Chuyển công tác"
            ],
            "khen_thuong_ky_luat": [
                "QUYẾT ĐỊNH KHEN THƯỞNG", "QUYẾT ĐỊNH KỶ LUẬT",
                "Khen thưởng", "Kỷ luật", "Thưởng", "Phạt"
            ]
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Tiền xử lý hình ảnh để cải thiện OCR"""
        try:
            # Đọc hình ảnh
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Không thể đọc hình ảnh: {image_path}")
            
            # Chuyển sang grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Loại bỏ nhiễu
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Tăng độ tương phản
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # Nhị phân hóa thích ứng
            binary = cv2.adaptiveThreshold(
                enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            return binary
            
        except Exception as e:
            print(f"Lỗi tiền xử lý hình ảnh: {e}")
            return None
    
    def extract_text(self, image_path: str) -> str:
        """Trích xuất văn bản từ hình ảnh"""
        try:
            # Tiền xử lý hình ảnh
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return ""
            
            # OCR với Tesseract
            text = pytesseract.image_to_string(
                processed_image, 
                lang='vie+eng',
                config='--psm 6 --oem 3'
            )
            
            return text
            
        except Exception as e:
            print(f"Lỗi OCR: {e}")
            return ""
    
    def detect_document_type(self, text: str) -> str:
        """Nhận diện loại giấy tờ dựa trên nội dung"""
        text_upper = text.upper()
        
        for doc_type, keywords in self.type_keywords.items():
            for keyword in keywords:
                if keyword.upper() in text_upper:
                    return doc_type
        
        return "unknown"
    
    def _extract_labor_contract(self, text: str) -> LaborContract:
        """Trích xuất thông tin hợp đồng lao động"""
        contract = LaborContract()
        
        # Tìm họ tên nhân viên
        name_patterns = [
            r"Họ và tên[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Người lao động[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"BÊN B[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contract.ho_ten = match.group(1).strip()
                break
        
        # Tìm mã nhân viên
        ma_patterns = [
            r"Mã nhân viên[:\s]+([A-Z0-9]+)",
            r"MSNV[:\s]+([A-Z0-9]+)",
            r"Mã số[:\s]+([A-Z0-9]+)"
        ]
        
        for pattern in ma_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contract.ma_nhan_vien = match.group(1).strip()
                break
        
        # Tìm chức danh
        chuc_patterns = [
            r"Chức danh[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Vị trí công việc[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in chuc_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contract.chuc_danh = match.group(1).strip()
                break
        
        # Tìm loại hợp đồng
        loai_patterns = [
            r"Loại hợp đồng[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Thời hạn[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in loai_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contract.loai_hop_dong = match.group(1).strip()
                break
        
        # Tìm thời hạn hợp đồng
        thoi_han_patterns = [
            r"Từ ngày[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"Đến ngày[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"Thời hạn[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
        ]
        
        for pattern in thoi_han_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contract.thoi_han_hop_dong = match.group(1).strip()
                break
        
        return contract
    
    def _extract_appointment_decision(self, text: str) -> AppointmentDecision:
        """Trích xuất thông tin quyết định bổ nhiệm"""
        decision = AppointmentDecision()
        
        # Tìm họ tên
        name_patterns = [
            r"Ông[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Bà[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Họ và tên[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.ho_ten = match.group(1).strip()
                break
        
        # Tìm chức vụ mới
        chuc_moi_patterns = [
            r"Bổ nhiệm[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Chức vụ[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in chuc_moi_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.chuc_vu_moi = match.group(1).strip()
                break
        
        # Tìm ngày hiệu lực
        ngay_patterns = [
            r"Ngày hiệu lực[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"Có hiệu lực từ[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
        ]
        
        for pattern in ngay_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.ngay_hieu_luc = match.group(1).strip()
                break
        
        # Tìm người ký
        nguoi_ky_patterns = [
            r"Người ký[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Ký tên[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in nguoi_ky_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.nguoi_ky = match.group(1).strip()
                break
        
        return decision
    
    def _extract_transfer_decision(self, text: str) -> TransferDecision:
        """Trích xuất thông tin quyết định điều chuyển"""
        decision = TransferDecision()
        
        # Tìm họ tên
        name_patterns = [
            r"Ông[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Bà[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Họ và tên[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.ho_ten = match.group(1).strip()
                break
        
        # Tìm bộ phận cũ
        bo_phan_cu_patterns = [
            r"Từ[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Bộ phận[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in bo_phan_cu_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.bo_phan_cu = match.group(1).strip()
                break
        
        # Tìm bộ phận mới
        bo_phan_moi_patterns = [
            r"Sang[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Đến[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in bo_phan_moi_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.bo_phan_moi = match.group(1).strip()
                break
        
        # Tìm ngày điều chuyển
        ngay_patterns = [
            r"Ngày điều chuyển[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"Từ ngày[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
        ]
        
        for pattern in ngay_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.ngay_dieu_chuyen = match.group(1).strip()
                break
        
        return decision
    
    def _extract_reward_discipline(self, text: str) -> RewardDiscipline:
        """Trích xuất thông tin khen thưởng/kỷ luật"""
        decision = RewardDiscipline()
        
        # Tìm họ tên
        name_patterns = [
            r"Ông[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Bà[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Họ và tên[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.ho_ten = match.group(1).strip()
                break
        
        # Xác định loại (khen thưởng hay kỷ luật)
        if any(keyword in text.upper() for keyword in ["KHEN THƯỞNG", "THƯỞNG"]):
            decision.hinh_thuc = "khen_thuong"
        elif any(keyword in text.upper() for keyword in ["KỶ LUẬT", "PHẠT", "KỶ LUẬT"]):
            decision.hinh_thuc = "ky_luat"
        
        # Tìm nội dung quyết định
        noi_dung_patterns = [
            r"Nội dung[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)",
            r"Lý do[:\s]+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]+)"
        ]
        
        for pattern in noi_dung_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.noi_dung_quyet_dinh = match.group(1).strip()
                break
        
        # Tìm ngày ban hành
        ngay_patterns = [
            r"Ngày ban hành[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
            r"Ngày[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
        ]
        
        for pattern in ngay_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                decision.ngay_ban_hanh = match.group(1).strip()
                break
        
        return decision
    
    def process_document(self, image_path: str) -> Dict[str, Any]:
        """Xử lý giấy tờ và trả về kết quả"""
        try:
            # Trích xuất văn bản
            text = self.extract_text(image_path)
            if not text:
                return {"error": "Không thể trích xuất văn bản từ hình ảnh"}
            
            # Nhận diện loại giấy tờ
            doc_type = self.detect_document_type(text)
            if doc_type == "unknown":
                return {
                    "error": "Không thể nhận diện loại giấy tờ",
                    "extracted_text": text[:500] + "..." if len(text) > 500 else text
                }
            
            # Xử lý theo loại giấy tờ
            if doc_type in self.document_types:
                result = self.document_types[doc_type](text)
                return {
                    "document_type": doc_type,
                    "extracted_text": text,
                    "processed_data": asdict(result),
                    "confidence": "high"
                }
            
            return {"error": f"Loại giấy tờ không được hỗ trợ: {doc_type}"}
            
        except Exception as e:
            return {"error": f"Lỗi xử lý giấy tờ: {str(e)}"}
    
    def save_result(self, result: Dict[str, Any], output_path: str):
        """Lưu kết quả xử lý vào file JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Đã lưu kết quả vào: {output_path}")
        except Exception as e:
            print(f"Lỗi lưu file: {e}")

# Hàm tiện ích để test
def test_document_processor():
    """Test module xử lý giấy tờ"""
    processor = DocumentProcessor()
    
    print("🔍 CDS Document Processor - Test Mode")
    print("=" * 50)
    
    # Test các pattern nhận diện
    print("📋 Các loại giấy tờ được hỗ trợ:")
    for doc_type, keywords in processor.type_keywords.items():
        print(f"  • {doc_type.replace('_', ' ').title()}")
        for keyword in keywords[:3]:  # Chỉ hiển thị 3 từ khóa đầu
            print(f"    - {keyword}")
    
    print("\n✅ Module đã sẵn sàng sử dụng!")
    print("\n📝 Cách sử dụng:")
    print("  processor = DocumentProcessor()")
    print("  result = processor.process_document('path/to/image.jpg')")
    print("  processor.save_result(result, 'output.json')")

if __name__ == "__main__":
    test_document_processor()
