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
    allow_origins=[
        "http://localhost:3000",
        "https://lab-score.fantasy-lab.com",
        "http://lab-score.fantasy-lab.com"
    ],
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

# 前端静态文件服务 - 放在最后，避免与API路由冲突
frontend_dist_path = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist_path), html=True), name="frontend")

@app.get("/api")
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