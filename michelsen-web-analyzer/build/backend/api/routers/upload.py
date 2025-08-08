from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import os
import shutil
from typing import Optional
import uuid

from core.config import settings

router = APIRouter()

# 全局变量存储上传的文件信息
uploaded_files = {
    "teacher": None,
    "student": None
}

def validate_video_file(file: UploadFile) -> bool:
    """验证视频文件"""
    if not file.filename:
        return False
    
    # 检查文件扩展名
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_video_extensions:
        return False
    
    return True

@router.post("/teacher")
async def upload_teacher_video(file: UploadFile = File(...)):
    """上传老师示范视频"""
    
    # 验证文件
    if not validate_video_file(file):
        raise HTTPException(
            status_code=400, 
            detail="不支持的文件格式，请上传 mp4/avi/mov 格式的视频文件"
        )
    
    try:
        # 保存文件
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / "teacher.mp4"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 更新全局状态
        uploaded_files["teacher"] = {
            "filename": file.filename,
            "filepath": str(file_path),
            "size": file_path.stat().st_size
        }
        
        return {
            "success": True,
            "message": "老师视频上传成功",
            "filename": file.filename,
            "size": file_path.stat().st_size,
            "preview_url": f"/api/videos/teacher.mp4"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.post("/student")
async def upload_student_video(file: UploadFile = File(...)):
    """上传学生实验视频"""
    
    # 验证文件
    if not validate_video_file(file):
        raise HTTPException(
            status_code=400, 
            detail="不支持的文件格式，请上传 mp4/avi/mov 格式的视频文件"
        )
    
    try:
        # 保存文件
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / "student.mp4"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 更新全局状态
        uploaded_files["student"] = {
            "filename": file.filename,
            "filepath": str(file_path),
            "size": file_path.stat().st_size
        }
        
        return {
            "success": True,
            "message": "学生视频上传成功",
            "filename": file.filename,
            "size": file_path.stat().st_size,
            "preview_url": f"/api/videos/student.mp4"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/status")
async def get_upload_status():
    """获取上传状态"""
    return {
        "teacher_uploaded": uploaded_files["teacher"] is not None,
        "student_uploaded": uploaded_files["student"] is not None,
        "can_analyze": all(uploaded_files.values()),
        "files": uploaded_files
    }

@router.get("/videos/{video_type}")
async def get_video(video_type: str):
    """获取视频文件用于预览"""
    if video_type not in ["teacher", "student"]:
        raise HTTPException(status_code=404, detail="视频类型不存在")
    
    file_path = Path(settings.upload_dir) / f"{video_type}.mp4"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="视频文件不存在")
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=f"{video_type}.mp4"
    )