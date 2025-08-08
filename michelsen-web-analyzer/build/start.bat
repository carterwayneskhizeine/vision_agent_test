@echo off
echo 🚀 启动迈克尔逊干涉实验 AI 分析系统...
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python 环境
    echo 请先安装 Python 3.8+ 
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 安装Python依赖...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 创建必要目录
if not exist "uploads" mkdir uploads
if not exist "static" mkdir static
if not exist "static\screenshots" mkdir static\screenshots  
if not exist "static\videos" mkdir static\videos
if not exist "static\images" mkdir static\images
if not exist "static\reports" mkdir static\reports

REM 启动服务器
echo.
echo 🌐 系统地址: http://localhost:8080
echo 📚 API文档: http://localhost:8080/docs  
echo 🛑 停止服务: Ctrl+C
echo.
python main.py

pause
