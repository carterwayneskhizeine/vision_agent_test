#!/bin/bash
# 修复阿里云服务器依赖问题

echo "🔧 修复迈克尔逊干涉实验系统依赖问题"
echo "========================================"

# 1. 安装系统级FFmpeg库（解决av库问题）
echo "📦 安装FFmpeg系统库..."
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    pkg-config

# 2. 检查Python环境
echo "🐍 检查Python环境..."
echo "当前Python版本: $(python --version)"
echo "当前pip位置: $(which pip)"

# 3. 清理并重新安装关键依赖
echo "🧹 清理并重新安装依赖..."

# 移除可能冲突的包
pip uninstall -y uvicorn fastapi vision-agent av

# 重新安装核心依赖
pip install uvicorn[standard]>=0.24.0
pip install fastapi>=0.104.1

# 4. 尝试安装vision-agent（跳过av如果仍然失败）
echo "🎬 尝试安装vision-agent..."
if pip install vision-agent; then
    echo "✅ vision-agent安装成功"
else
    echo "⚠️  vision-agent安装失败，尝试不依赖av库的替代方案..."
    pip install --no-deps vision-agent
fi

# 5. 验证安装
echo "✅ 验证安装结果..."
python -c "
try:
    import uvicorn
    print('✅ uvicorn 导入成功')
except ImportError as e:
    print(f'❌ uvicorn 导入失败: {e}')

try:
    import fastapi
    print('✅ fastapi 导入成功')
except ImportError as e:
    print(f'❌ fastapi 导入失败: {e}')

try:
    import cv2
    print('✅ opencv 导入成功')
except ImportError as e:
    print(f'❌ opencv 导入失败: {e}')
"

echo ""
echo "🎉 依赖修复完成！可以重新启动服务了。"
echo "执行: python start-dev.py"
