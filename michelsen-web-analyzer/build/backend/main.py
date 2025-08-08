from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn
import os
import shutil
from typing import List, Optional

from api.routers import analysis, upload
from core.config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title="迈克尔逊干涉实验 AI 分析 API",
    description="基于 AI 技术的迈克尔逊干浉实验教学视频分析系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建必要的目录
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/screenshots", exist_ok=True)
os.makedirs("static/videos", exist_ok=True)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])

@app.get("/")
async def root():
    return {
        "message": "迈克尔逊干涉实验 AI 分析系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )