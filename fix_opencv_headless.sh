#!/bin/bash
# OpenCV无头版本修复脚本

echo "🔧 正在修复OpenCV依赖问题..."

# 1. 卸载现有的opencv-python
echo "📦 卸载旧版本OpenCV..."
pip uninstall opencv-python opencv-contrib-python -y

# 2. 安装无头版本
echo "🚀 安装OpenCV无头版本..."
pip install opencv-python-headless>=4.8.1

# 3. 验证安装
echo "✅ 验证安装..."
python -c "import cv2; print(f'OpenCV版本: {cv2.__version__}')"

echo "🎉 修复完成！可以重新启动后端服务。"
