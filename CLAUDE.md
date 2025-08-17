# CLAUDE.md

该文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

此代码库包含两个用于迈克尔逊干涉仪物理实验AI分析的主要项目：

1. **michelsen-web-analyzer/**: 全栈Web应用程序 (FastAPI + Vue 3)，通过Web界面进行视频分析
2. **web/**: 独立的Python原型，用于命令行视频分析和设备检测

## 开发命令

### Web应用程序 (michelsen-web-analyzer/)

**一键开发启动（推荐）:**
```bash
cd michelsen-web-analyzer
python start-dev.py
```

**手动启动:**
```bash
# 仅后端
python start-backend.py

# 仅前端（单独终端）
node start-frontend.js
```

**包构建:**
```bash
# 构建所有包
npm run build
python build-package.py all

# 构建特定包
python build-package.py prod    # 生产包
python build-package.py dev     # 开发包
python build-executable.py     # 独立可执行文件
```

**前端开发:**
```bash
cd frontend
npm install
npm run dev                     # 开发服务器
npm run build                   # 生产构建
npm run type-check             # TypeScript检查
```

**后端开发:**
```bash
cd backend
pip install -r requirements.txt
python main.py                 # 启动FastAPI服务器
```

### 独立原型 (web/)

**快速分析模式:**
```bash
cd web
python experiment_analyzer_prototype.py    # 智能分析（自动检测文件）
python student_operation_analysis.py       # 学生操作分析
python quick_detection.py                  # 仅设备检测
python test_analyzer.py                    # 使用示例数据测试
```

## 架构

### Web应用程序架构

**后端 (FastAPI):**
- `backend/main.py`: FastAPI应用程序入口点，包含CORS和静态文件服务
- `backend/api/routers/`: 上传和分析的REST API端点
- `backend/services/`: 视频分析和AI处理的业务逻辑
- `backend/analyzer/`: 核心AI分析引擎（与独立原型相同）
- `backend/core/config.py`: 应用程序配置和设置

**前端 (Vue 3 + Vite):**
- `frontend/src/main.ts`: Vue 3应用程序引导，包含Pinia和Vue Router
- `frontend/src/views/`: 页面组件（Home、Analysis）
- `frontend/src/api/`: 与后端通信的HTTP客户端
- `frontend/src/types/`: TypeScript类型定义
- 使用DaisyUI + Tailwind CSS实现响应式UI组件

### AI分析引擎

两个项目共享相同的核心分析引擎（`MichelsonInterferometerAnalyzer`类）：

**主要功能:**
- 在预定义时间点提取和分析视频帧
- 使用OpenCV和SIFT/ORB特征匹配进行设备检测
- 实验步骤识别（6个标准步骤：设置、激光对准、干涉图样、测量等）
- 教师示范和学生视频之间的比较分析
- 带注释截图的可视化报告生成

**检测目标:**
- 7种物理设备：氦氖激光器、分束器、反射镜、精密测微头、扩束器、观察屏
- 6个实验步骤，包含时间验证和准确性评分

### 文件组织

**分析输出:**
- `backend/static/screenshots/`: 生成的分析截图
- `backend/uploads/`: 上传的视频文件
- `web/analysis_output/`: 独立原型输出
- `web/real_video_analysis/`: 带设备检测框的真实视频分析

## 环境设置

**必需的API密钥:**
```bash
# 设置ANTHROPIC_API_KEY环境变量
export ANTHROPIC_API_KEY="sk-ant-api03-your-key"

# 或在backend/目录下创建.env文件
echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key" > backend/.env
```

**依赖项:**
- Python 3.8+，包含OpenCV、NumPy、Matplotlib、FastAPI、Uvicorn
- Node.js 16+用于前端开发
- vision-agent包用于增强AI功能

## 生产部署配置

### 服务器部署（已配置完成）

**systemd服务管理:**
```bash
# 查看服务状态
systemctl status michelsen_analyzer.service

# 查看实时日志
journalctl -u michelsen_analyzer.service -f

# 重启服务
systemctl restart michelsen_analyzer.service
```

**部署架构:**
- **后端服务**: FastAPI (端口8080) 托管API和前端静态文件
- **Nginx代理**: 处理HTTPS、SSL证书和请求转发
- **域名**: https://lab-score.fantasy-lab.com/
- **架构优势**: 前后端统一域名，无跨域问题

**Nginx配置要点:**
```nginx
# API请求代理到后端
location /api/ {
    proxy_pass http://127.0.0.1:8080/api/;
    # ... 其他代理设置
}

# 前端静态文件代理到后端（后端托管dist）
location / {
    proxy_pass http://127.0.0.1:8080/;
    # ... 其他代理设置
}
```

**环境变量配置:**
- 位置: `/etc/systemd/system/michelsen_analyzer.env`
- 包含ANTHROPIC_API_KEY和其他必要环境变量
- 权限设置为600以确保安全

## 访问入口

**Web应用程序:**
- 生产环境: https://lab-score.fantasy-lab.com/
- 开发环境前端: http://localhost:3000
- 后端API: http://localhost:8080
- API文档: http://localhost:8080/docs

**分析工作流程:**
1. 上传教师示范视频 (teacher.mp4)
2. 上传学生实验视频 (student.mp4)
3. 通过Web界面触发AI分析
4. 查看带注释截图和比较分析的结果

## 关键实现要点

- 后端使用基于线程的执行进行视频分析以防止阻塞
- 前端通过API轮询实现实时进度跟踪
- 设备检测使用多尺度级别的模板匹配以增强鲁棒性
- 在matplotlib中配置中文语言支持用于报告生成
- 配置CORS以支持开发期间的前后端通信
- 文件上传限制为50MB，支持MP4/AVI/MOV格式

## 前端更新部署流程

### 本地开发环境更新

**方法1: 直接替换dist文件夹（推荐）**
```bash
# 备份当前dist
cd michelsen-web-analyzer/frontend
mv dist dist_backup_$(date +%Y%m%d_%H%M%S)

# 复制新的dist文件夹
cp -r /path/to/new/dist .

# 修复可能的硬编码HTTP URL
sed -i 's|http://lab-score.fantasy-lab.com/api|/api|g' dist/assets/*.js

# 启动后端测试
cd ../backend
python main.py
# 访问 http://localhost:8080
```

**方法2: 源码重构建**
```bash
cd michelsen-web-analyzer/frontend
npm run build
```

### 阿里云服务器更新

**完整更新流程:**
```bash
# 1. 本地提交更改
git add .
git commit -m "更新前端界面"
git push origin main

# 2. 服务器拉取更新
ssh your_server
cd /root/Code/vision_agent_test
git stash  # 保存本地更改
git pull origin main
git stash pop  # 恢复本地更改（如果需要）

# 3. 修复Mixed Content问题（如果新dist包含硬编码HTTP URL）
sed -i 's|http://lab-score.fantasy-lab.com/api|/api|g' michelsen-web-analyzer/frontend/dist/assets/*.js

# 4. 重启服务
systemctl restart michelsen_analyzer.service

# 5. 验证部署
curl -I https://lab-score.fantasy-lab.com/
curl -s https://lab-score.fantasy-lab.com/ | grep -i "迈克尔逊"
```

### 服务冲突解决

**停止冲突的服务:**
```bash
# 停止老的开发服务（如果存在）
systemctl stop michelsen_dev.service
systemctl disable michelsen_dev.service

# 确保只有生产服务运行
systemctl status michelsen_analyzer.service
ss -tulpn | grep :8080
```

## 故障排除

**常见问题:**
- **502错误**: 检查Nginx配置和后端服务状态
- **Mixed Content错误**: 前端使用HTTP请求HTTPS页面，需修复API URL
- **服务端口冲突**: 确保只有一个服务占用8080端口
- **API 404错误**: 检查路由注册和配置文件

**日志查看:**
```bash
# 实时日志
journalctl -u michelsen_analyzer.service -f

# 错误日志
journalctl -u michelsen_analyzer.service -p err

# 最近日志
journalctl -u michelsen_analyzer.service -n 100

# Nginx错误日志
tail -f /www/wwwlogs/lab-score.fantasy-lab.com.error.log
```

**API测试:**
```bash
# 测试后端健康
curl http://127.0.0.1:8080/health

# 测试前端访问
curl -I https://lab-score.fantasy-lab.com/

# 测试API端点
curl -X POST http://127.0.0.1:8080/api/upload/teacher -F "file=@test.mp4"
```