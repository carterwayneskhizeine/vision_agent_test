# 迈克尔逊干涉实验 AI 视频分析 Web 应用

基于 AI 技术的迈克尔逊干涉实验教学视频分析系统，提供 Web 界面进行实验步骤智能解读。

## 🏗️ 项目结构

```
michelsen-web-analyzer/
├── frontend/                   # Vite + Vue 3 + DaisyUI 前端
├── backend/                    # FastAPI 后端
├── shared/                     # 共享资源 (视频、截图等)
└── docs/                       # 文档
```

## 🚀 快速开始

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

### 后端开发  
```bash
cd backend
pip install -r requirements.txt
python main.py
```

## ✨ 功能特性

- 🎥 支持上传老师示范视频 (teacher.mp4) 和学生实验视频 (student.mp4)
- 🔍 AI 智能分析实验步骤内容
- 📸 自动截图并生成步骤解释
- 📊 老师与学生步骤对比分析
- 🎯 实时分析进度显示
- 📱 响应式 Web 界面