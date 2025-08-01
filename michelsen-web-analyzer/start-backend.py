#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端开发服务器启动脚本
用于开发环境下启动 FastAPI 后端服务
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 启动迈克尔逊干涉实验 AI 分析后端服务...")
    
    # 检查工作目录
    backend_dir = Path(__file__).parent / "backend"
    if not backend_dir.exists():
        print(f"❌ 错误: 未找到 backend 目录")
        return 1
    
    # 检查依赖
    requirements_file = backend_dir / "requirements.txt"
    if not requirements_file.exists():
        print(f"❌ 错误: 未找到 {requirements_file}")
        return 1
    
    # 检查是否安装依赖
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI 和 Uvicorn 已安装")
    except ImportError:
        print("⚠️  检测到未安装依赖，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
    
    # 进入 backend 目录
    os.chdir(backend_dir)
    
    # 创建必要的目录
    for directory in ["uploads", "static", "static/screenshots", "static/videos"]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print(f"🌐 正在启动服务器: http://localhost:8000")
    print(f"📚 API 文档: http://localhost:8000/docs")
    print(f"⚙️  开发模式: 已启用热重载")
    print(f"🛑 停止服务: Ctrl+C")
    print("-" * 50)
    
    # 启动 FastAPI 服务器
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动服务器失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())