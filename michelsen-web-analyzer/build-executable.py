#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迈克尔逊干涉实验 AI 分析系统 - 可执行文件打包工具
使用 PyInstaller 创建独立的可执行程序
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """检查并安装 PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("📦 正在安装 PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller 安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller 安装失败")
            return False

def create_pyinstaller_spec():
    """创建 PyInstaller 规格文件"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有需要的数据文件
datas = [
    ('backend/analyzer', 'analyzer'),
    ('backend/api', 'api'),
    ('backend/core', 'core'),
    ('backend/services', 'services'),
    ('frontend/dist', 'static'),
]

# 收集隐藏的导入
hiddenimports = [
    'fastapi',
    'uvicorn',
    'uvicorn.lifespan.on',
    'uvicorn.lifespan.off',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.http.auto',
    'multipart',
    'cv2',
    'numpy',
    'PIL',
    'matplotlib',
    'imageio',
    'skimage',
    'anthropic',
    'vision_agent',
]

a = Analysis(
    ['backend/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='michelsen-analyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='michelsen-analyzer'
)
"""
    
    spec_file = Path("michelsen-analyzer.spec")
    spec_file.write_text(spec_content)
    return spec_file

def build_executable():
    """构建可执行文件"""
    print("🚀 开始构建可执行文件...")
    
    # 检查环境
    if not check_pyinstaller():
        return False
    
    # 确保前端已构建
    frontend_dist = Path("frontend/dist")
    if not frontend_dist.exists():
        print("🎨 构建前端...")
        try:
            subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)
        except subprocess.CalledProcessError:
            print("❌ 前端构建失败")
            return False
    
    # 创建规格文件
    spec_file = create_pyinstaller_spec()
    
    try:
        # 运行 PyInstaller
        print("⚡ 使用 PyInstaller 构建...")
        subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--clean", 
            str(spec_file)
        ], check=True)
        
        # 清理临时文件
        spec_file.unlink()
        if Path("build").exists():
            shutil.rmtree("build")
        
        print("✅ 可执行文件构建完成！")
        print(f"📁 输出目录: {Path('dist/michelsen-analyzer').absolute()}")
        print("🚀 运行方式: ./dist/michelsen-analyzer/michelsen-analyzer")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
