#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动开发环境
同时启动前端和后端服务
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from threading import Thread

def run_backend():
    """运行后端服务"""
    try:
        print("🚀 正在启动后端服务...")
        subprocess.run([sys.executable, "start-backend.py"])
    except Exception as e:
        print(f"❌ 后端服务失败: {e}")

def run_frontend():
    """运行前端服务"""
    try:
        print("🎨 正在启动前端服务...")
        subprocess.run(["node", "start-frontend.js"])
    except Exception as e:
        print(f"❌ 前端服务失败: {e}")

def main():
    print("🎆 迈克尔逊干涉实验 AI 分析系统 - 开发环境")
    print("=" * 60)
    
    # 获取服务器IP地址
    try:
        import sys
        sys.path.append('.')
        from get_server_ip import get_server_ip
        local_ip = get_server_ip()
        
        if local_ip != "localhost":
            print(f"🌐 本地访问: http://localhost:3000")
            print(f"🌍 外网访问: http://{local_ip}:3000")
            print(f"🔧 后端 API: http://{local_ip}:8080")
            print(f"📚 API 文档: http://{local_ip}:8080/docs")
        else:
            print("🌐 前端地址: http://localhost:3000")
            print("🔧 后端 API: http://localhost:8080") 
            print("📚 API 文档: http://localhost:8080/docs")
    except:
        print("🌐 前端地址: http://localhost:3000")
        print("🔧 后端 API: http://localhost:8080")
        print("📚 API 文档: http://localhost:8080/docs")
    
    print("🛑 停止服务: Ctrl+C")
    print("💡 提示: 需要配置阿里云安全组开放3000和8080端口")
    print("=" * 60)
    
    # 检查必要的文件
    required_files = [
        "start-backend.py",
        "start-frontend.js",
        "backend/main.py",
        "frontend/package.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return 1
    
    # 启动服务
    try:
        # 在后台线程中启动后端
        backend_thread = Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # 等待一下让后端先启动
        time.sleep(3)
        
        # 在后台线程中启动前端
        frontend_thread = Thread(target=run_frontend, daemon=True)
        frontend_thread.start()
        
        print("✨ 开发环境已启动！")
        print("⚡ 正在等待服务启动...")
        
        # 保持主线程运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在停止所有服务...")
    except Exception as e:
        print(f"\n❌ 开发环境启动失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 程序已退出")