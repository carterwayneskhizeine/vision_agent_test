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

### 方式一：一键启动（推荐）
```bash
# 进入项目根目录
cd michelsen-web-analyzer

# 如果未安装 Node.js，请先从官方中文页面安装（推荐 LTS 版本）：
# https://nodejs.org/zh-cn

# 安装前端依赖（首次运行需要）
cd frontend && npm install && cd ..

# 安装后端依赖（首次运行需要）
cd backend && pip install -r requirements.txt && cd ..

# 一键启动前端+后端
python start-dev.py
```

启动后访问：
- 🌐 **前端界面**: http://localhost:3000 （或 http://localhost:3001）
- 🔧 **后端API**: http://localhost:8080  
- 📚 **API文档**: http://localhost:8080/docs

### 方式二：分别启动（开发调试用）

**启动后端**：
```bash
cd michelsen-web-analyzer/backend
python main.py
```

**启动前端**（新开一个终端）：
```bash
cd michelsen-web-analyzer/frontend  
npm run dev
```

## 🔐 环境变量与 API 密钥

本项目后端可从环境变量或 `.env` 文件读取外部 API 密钥（如 `ANTHROPIC_API_KEY`）。请使用您自己的密钥，切勿将真实密钥提交到仓库。

### Windows 设置方式
- **图形界面（系统变量）**：
  1. 打开"控制面板 → 系统和安全 → 系统"或"设置 → 系统 → 关于"
  2. 点击"高级系统设置 → 环境变量"
  3. 在"系统变量"中点击"新建"，名称填写 `ANTHROPIC_API_KEY`，值填写您的密钥（例如 `sk-ant-api03-...`）
  4. 确定保存，关闭窗口，重新打开终端

- **命令行（PowerShell）**：
  ```powershell
  setx ANTHROPIC_API_KEY "sk-ant-api03-你的完整密钥" /M
  ```
  注意：需要重新打开一个新终端后生效。

### Ubuntu 设置方式
- **临时（当前会话）**：
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-api03-你的完整密钥"
  ```
- **永久（追加到 Shell 启动文件）**：
  ```bash
  echo 'export ANTHROPIC_API_KEY="sk-ant-api03-你的完整密钥"' >> ~/.bashrc && source ~/.bashrc
  # 或 Zsh 用户：
  echo 'export ANTHROPIC_API_KEY="sk-ant-api03-你的完整密钥"' >> ~/.zshrc && source ~/.zshrc
  ```

### 使用 `.env` 文件（推荐用于本地开发）
在后端目录 `michelsen-web-analyzer/backend/` 下创建 `.env` 文件，内容示例：
```
ANTHROPIC_API_KEY=sk-ant-api03-你的完整密钥
```
后端基于配置会自动读取 `.env`。

## 📋 使用步骤

1. **启动服务**：使用上面的方式一或方式二启动前后端
2. **打开前端界面**：访问 http://localhost:3000
3. **上传视频**：分别上传老师示范视频和学生实验视频
4. **开始分析**：点击"开始AI分析"按钮
5. **查看结果**：等待分析完成，查看实验步骤截图和详细解释

## 🛑 停止服务

- **方式一用户**：在运行 `python start-dev.py` 的终端按 `Ctrl+C`
- **方式二用户**：分别在前端和后端终端按 `Ctrl+C`

## ✨ 功能特性

- 🎥 支持上传老师示范视频 (teacher.mp4) 和学生实验视频 (student.mp4)
- 🔍 AI 智能分析实验步骤内容，基于原版 `experiment_analyzer_prototype.py`
- 📸 自动截图并生成步骤解释（每个步骤对应的截图和文字说明）
- 📊 老师与学生步骤对比分析，识别操作差异和完整性
- 🎯 实时分析进度显示
- 📱 响应式 Web 界面，使用 DaisyUI 组件库

## 📁 生成文件

分析完成后，会在以下位置生成文件：
- `backend/static/screenshots/` - 实验步骤截图
- `backend/static/reports/` - JSON格式的分析报告
- `backend/uploads/` - 上传的视频文件

## 🛠️ 技术栈

**前端**：
- Vue 3 + TypeScript
- Vite 构建工具
- DaisyUI + Tailwind CSS
- Axios API调用

**后端**：
- FastAPI + Python
- OpenCV 视频处理
- NumPy + Matplotlib 数据处理
- Uvicorn ASGI服务器

## 📋 答疑

**Q: 我应该用哪种方式启动？**  
A: 推荐使用**方式一**（`python start-dev.py`），一个命令就能启动前后端，简单方便。

**Q: 如果端口被占用怎么办？**  
A: 前端会自动尝试下一个端口（3001, 3002...），后端固定使用8080端口。

**Q: 分析需要多长时间？**  
A: 一般1-2分钟，取决于视频长度和计算机性能。分析过程中可以在终端看到进度。