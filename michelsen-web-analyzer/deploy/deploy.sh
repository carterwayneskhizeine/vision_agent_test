#!/bin/bash
# 迈克尔逊干涉实验AI分析系统部署脚本

set -e

echo "🚀 开始部署迈克尔逊干涉实验AI分析系统..."

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请以root用户运行此脚本"
    exit 1
fi

# 项目路径
PROJECT_ROOT="/root/Code/vision_agent_test/michelsen-web-analyzer"
DEPLOY_DIR="$PROJECT_ROOT/deploy"

echo "📁 项目路径: $PROJECT_ROOT"

# 1. 构建前端
echo "🎨 构建前端..."
cd "$PROJECT_ROOT/frontend"
npm run build

# 2. 配置systemd服务
echo "⚙️ 配置systemd服务..."
cp "$DEPLOY_DIR/michelsen_analyzer.service" /etc/systemd/system/
cp "$DEPLOY_DIR/michelsen_analyzer.env" /etc/systemd/system/
chmod 600 /etc/systemd/system/michelsen_analyzer.env

# 提示用户设置API密钥
echo "🔑 请设置API密钥:"
echo "编辑文件: /etc/systemd/system/michelsen_analyzer.env"
echo "设置: ANTHROPIC_API_KEY=your_actual_api_key"

# 3. 启用并启动服务
echo "🔄 启用并启动服务..."
systemctl daemon-reload
systemctl enable michelsen_analyzer.service
systemctl start michelsen_analyzer.service

# 4. 检查服务状态
echo "📊 检查服务状态..."
systemctl status michelsen_analyzer.service --no-pager

# 5. 检查端口监听
echo "🔌 检查端口监听..."
ss -lntp | grep :8080 || echo "❌ 8080端口未监听"

# 6. 显示Nginx配置提示
echo "📝 Nginx配置:"
echo "请将以下配置添加到宝塔Nginx中:"
echo "配置文件位置: $DEPLOY_DIR/nginx_lab_score.conf"
echo ""
echo "或者手动添加server块到Nginx配置中"

echo "✅ 部署完成！"
echo ""
echo "🌐 访问地址: https://lab-score.fantasy-lab.com"
echo "🔧 后端健康检查: curl http://127.0.0.1:8080/health"
echo "📚 查看日志: journalctl -u michelsen_analyzer.service -f"