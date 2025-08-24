#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Server FastAPI cho CDS Scanner
Xử lý giấy tờ và tích hợp với frontend Next.js
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uvicorn

from document_processor import DocumentProcessor
from models import Base, Document
from db import ENGINE, db_session
from sqlalchemy import text

# Khởi tạo FastAPI app
app = FastAPI(
    title="CDS Scanner API",
    description="API xử lý giấy tờ nội bộ công ty với OCR thông minh",
    version="1.0.0"
)

# CORS middleware để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo processor
processor = DocumentProcessor()

# Thư mục lưu trữ file
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")
RESULTS_DIR = Path("results")

# Tạo thư mục nếu chưa có
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Models Pydantic
class DocumentResponse(BaseModel):
    """Response model cho kết quả xử lý giấy tờ"""
    success: bool
    document_type: Optional[str] = None
    extracted_text: Optional[str] = None
    processed_data: Optional[Dict[str, Any]] = None
    confidence: Optional[str] = None
    error: Optional[str] = None
    file_path: Optional[str] = None
    processing_time: Optional[float] = None

class DocumentListResponse(BaseModel):
    """Response model cho danh sách giấy tờ"""
    success: bool
    documents: List[Dict[str, Any]]
    total: int

class DocumentStatsResponse(BaseModel):
    """Response model cho thống kê"""
    success: bool
    total_documents: int
    by_type: Dict[str, int]
    by_date: Dict[str, int]

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CDS Scanner API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "upload": "/upload",
            "process": "/process/{filename}",
            "documents": "/documents",
            "stats": "/stats",
            "download": "/download/{filename}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/db/health")
async def db_health_check():
    """Kiểm tra kết nối database"""
    if ENGINE is None:
        return {"enabled": False, "status": "db_disabled"}
    try:
        with db_session() as session:
            session.execute(text("SELECT 1"))
        return {"enabled": True, "status": "ok"}
    except Exception as e:
        return {"enabled": True, "status": "error", "detail": str(e)}

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload file giấy tờ"""
    try:
        # Kiểm tra file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Chỉ chấp nhận file hình ảnh")
        
        # Tạo tên file unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / filename
        
        # Lưu file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return DocumentResponse(
            success=True,
            file_path=str(file_path),
            message=f"Đã upload file: {filename}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi upload: {str(e)}")

@app.post("/process/{filename}", response_model=DocumentResponse)
async def process_document(filename: str, background_tasks: BackgroundTasks):
    """Xử lý giấy tờ đã upload"""
    try:
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Không tìm thấy file")
        
        # Xử lý giấy tờ
        start_time = datetime.now()
        result = processor.process_document(str(file_path))
        processing_time = (datetime.now() - start_time).total_seconds()
        
        if "error" in result:
            return DocumentResponse(
                success=False,
                error=result["error"],
                file_path=str(file_path)
            )
        
        # Lưu kết quả vào file JSON
        result_filename = f"{Path(filename).stem}_result.json"
        result_path = RESULTS_DIR / result_filename
        
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # Lưu vào Database (nếu cấu hình bật)
        if ENGINE is not None:
            try:
                with db_session() as session:
                    doc = Document(
                        filename=filename,
                        document_type=result.get("document_type"),
                        extracted_text=result.get("extracted_text", "")[:4000],
                        processed_data=json.dumps(result.get("processed_data", {}), ensure_ascii=False),
                        confidence=str(result.get("confidence")) if result.get("confidence") is not None else None,
                    )
                    session.add(doc)
            except Exception as db_err:
                print(f"Lỗi lưu DB: {db_err}")
        
        # Di chuyển file đã xử lý
        processed_path = PROCESSED_DIR / filename
        shutil.move(str(file_path), str(processed_path))
        
        return DocumentResponse(
            success=True,
            document_type=result.get("document_type"),
            extracted_text=result.get("extracted_text", "")[:1000],  # Giới hạn độ dài
            processed_data=result.get("processed_data"),
            confidence=result.get("confidence"),
            file_path=str(processed_path),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")

@app.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    page: int = 1,
    limit: int = 10,
    doc_type: Optional[str] = None
):
    """Lấy danh sách giấy tờ đã xử lý"""
    try:
        documents = []
        
        # Đọc từ thư mục results
        for result_file in RESULTS_DIR.glob("*.json"):
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Lọc theo loại nếu có
                if doc_type and data.get("document_type") != doc_type:
                    continue
                
                documents.append({
                    "filename": result_file.stem,
                    "document_type": data.get("document_type"),
                    "processed_data": data.get("processed_data"),
                    "confidence": data.get("confidence"),
                    "created_at": result_file.stat().st_mtime
                })
                
            except Exception as e:
                print(f"Lỗi đọc file {result_file}: {e}")
                continue
        
        # Sắp xếp theo thời gian tạo
        documents.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Phân trang
        start = (page - 1) * limit
        end = start + limit
        paginated_docs = documents[start:end]
        
        return DocumentListResponse(
            success=True,
            documents=paginated_docs,
            total=len(documents)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy danh sách: {str(e)}")

@app.get("/stats", response_model=DocumentStatsResponse)
async def get_statistics():
    """Lấy thống kê xử lý giấy tờ"""
    try:
        total_documents = 0
        by_type = {}
        by_date = {}
        
        # Đếm từ thư mục results
        for result_file in RESULTS_DIR.glob("*.json"):
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                total_documents += 1
                
                # Thống kê theo loại
                doc_type = data.get("document_type", "unknown")
                by_type[doc_type] = by_type.get(doc_type, 0) + 1
                
                # Thống kê theo ngày
                created_date = datetime.fromtimestamp(result_file.stat().st_mtime).strftime("%Y-%m-%d")
                by_date[created_date] = by_date.get(created_date, 0) + 1
                
            except Exception as e:
                print(f"Lỗi đọc file {result_file}: {e}")
                continue
        
        return DocumentStatsResponse(
            success=True,
            total_documents=total_documents,
            by_type=by_type,
            by_date=by_date
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lấy thống kê: {str(e)}")

@app.get("/download/{filename}")
async def download_result(filename: str):
    """Download kết quả xử lý"""
    try:
        file_path = RESULTS_DIR / f"{filename}.json"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Không tìm thấy file kết quả")
        
        return FileResponse(
            path=str(file_path),
            filename=f"{filename}.json",
            media_type="application/json"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi download: {str(e)}")

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Xóa giấy tờ đã xử lý"""
    try:
        # Xóa file kết quả
        result_file = RESULTS_DIR / f"{filename}.json"
        if result_file.exists():
            result_file.unlink()
        
        # Xóa file đã xử lý
        processed_file = PROCESSED_DIR / f"{filename}"
        if processed_file.exists():
            processed_file.unlink()
        
        return {"success": True, "message": f"Đã xóa: {filename}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xóa: {str(e)}")

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Lỗi server nội bộ",
            "detail": str(exc)
        }
    )

# Background tasks
def cleanup_old_files():
    """Dọn dẹp file cũ"""
    try:
        current_time = datetime.now()
        
        # Xóa file upload cũ hơn 7 ngày
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_age.days > 7:
                    file_path.unlink()
                    print(f"Đã xóa file cũ: {file_path}")
                    
    except Exception as e:
        print(f"Lỗi dọn dẹp file: {e}")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Khởi tạo khi server start"""
    print("CDS Scanner API dang khoi dong...")
    print(f"Upload directory: {UPLOAD_DIR.absolute()}")
    print(f"Processed directory: {PROCESSED_DIR.absolute()}")
    print(f"Results directory: {RESULTS_DIR.absolute()}")
    print("API server da san sang!")
    # Tạo bảng nếu DB được bật
    try:
        if ENGINE is not None:
            Base.metadata.create_all(bind=ENGINE)
            print("Database connected, tables ensured.")
    except Exception as e:
        print(f"Lỗi khởi tạo DB: {e}")

if __name__ == "__main__":
    # Chạy server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
