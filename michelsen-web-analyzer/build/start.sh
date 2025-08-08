#!/bin/bash
echo "🚀 启动迈克尔逊干涉实验 AI 分析系统..."
echo

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 环境"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 创建必要目录
mkdir -p uploads static/screenshots static/videos static/images static/reports

# 启动服务器
echo
echo "🌐 系统地址: http://localhost:8080"
echo "📚 API文档: http://localhost:8080/docs"
echo "🛑 停止服务: Ctrl+C"
echo
python3 main.py
