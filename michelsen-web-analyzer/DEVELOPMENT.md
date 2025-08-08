# 开发指南

## 🚀 快速开始

### 1. 安装依赖

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 前端依赖
在安装前端依赖之前，请确保已安装 Node.js（推荐 LTS 版本）。可从官方中文页面下载：
https://nodejs.org/zh-cn
```bash
cd frontend
npm install
```

### 2. 开发环境启动

#### 方式 1: 一键启动（推荐）
```bash
python start-dev.py
```

#### 方式 2: 分别启动
```bash
# 终端 1: 启动后端
python start-backend.py

# 终端 2: 启动前端
node start-frontend.js
```

### 3. 访问地址
- 🌐 **前端应用**: http://localhost:3000
- 🔧 **后端 API**: http://localhost:8000
- 📚 **API 文档**: http://localhost:8000/docs

## 📝 项目结构

```
michelsen-web-analyzer/
├── frontend/                   # 前端代码 (Vite + Vue 3 + DaisyUI)
│   ├── src/
│   │   ├── components/        # Vue 组件
│   │   ├── views/             # 页面视图
│   │   ├── api/               # API 调用
│   │   ├── types/             # TypeScript 类型
│   │   └── router/            # 路由配置
│   ├── package.json           # 前端依赖
│   └── vite.config.ts         # Vite 配置
├── backend/                    # 后端代码 (FastAPI)
│   ├── api/                   # API 路由
│   ├── core/                  # 核心配置
│   ├── services/              # 业务逻辑
│   ├── analyzer/              # AI 分析器
│   ├── main.py                # 入口文件
│   └── requirements.txt       # 后端依赖
├── start-dev.py               # 一键开发启动
├── start-backend.py           # 后端启动脚本
├── start-frontend.js          # 前端启动脚本
└── README.md                  # 项目说明
```

## 🛠️ 开发流程

### 前端开发
1. **组件开发**: 在 `frontend/src/components/` 中创建新组件
2. **页面开发**: 在 `frontend/src/views/` 中创建新页面
3. **API 集成**: 在 `frontend/src/api/` 中添加 API 调用
4. **类型定义**: 在 `frontend/src/types/` 中定义 TypeScript 类型

### 后端开发
1. **API 路由**: 在 `backend/api/routers/` 中添加新的 API 路由
2. **业务逻辑**: 在 `backend/services/` 中实现业务逻辑
3. **数据模型**: 使用 Pydantic 定义数据模型
4. **配置管理**: 在 `backend/core/config.py` 中管理配置

## 📊 主要功能

### 已实现功能
- ✅ **视频上传**: 支持上传 teacher.mp4 和 student.mp4
- ✅ **视频预览**: 上传后可在线预览视频
- ✅ **AI 分析**: 集成现有的 Python 分析算法
- ✅ **实时进度**: 分析进度实时显示
- ✅ **结果展示**: 分析结果图文并茂显示
- ✅ **响应式设计**: 支持桌面和移动设备

### 待完善功能
- ⏳ **用户管理**: 登录注册功能
- ⏳ **历史记录**: 分析历史查看
- ⏳ **批量处理**: 多视频批量分析
- ⏳ **报告导出**: PDF/Word 报告导出

## 📚 技术栈

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 框架**: DaisyUI + Tailwind CSS
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP 客户端**: Axios

### 后端
- **框架**: FastAPI
- **异步处理**: AsyncIO
- **文件处理**: Python Multipart
- **AI 分析**: OpenCV + NumPy + PIL
- **服务器**: Uvicorn

## 🚑 部署说明

### 生产环境部署
1. **构建前端**:
   ```bash
   cd frontend
   npm run build
   ```

2. **配置后端**:
   - 修改 `backend/core/config.py` 中的生产配置
   - 设置环境变量

3. **启动服务**:
   ```bash
   # 生产模式启动
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Docker 部署（可选）
可以后续添加 Dockerfile 和 docker-compose.yml 来简化部署。

## 📝 注意事项

1. **文件大小**: 默认限制视频文件大小为 50MB
2. **文件格式**: 支持 MP4/AVI/MOV 格式
3. **浏览器兼容**: 推荐使用现代浏览器 (Chrome/Firefox/Safari/Edge)
4. **开发环境**: 需要 Python 3.8+ 和 Node.js 16+

## 🔍 故障排除

### 常见问题
1. **依赖安装失败**: 检查 Python 和 Node.js 版本
2. **端口占用**: 修改配置文件中的端口号
3. **CORS 错误**: 检查后端 CORS 配置
4. **文件上传失败**: 检查文件大小和格式

### 日志查看
- **前端**: 浏览器控制台
- **后端**: 终端输出日志

## 📞 技术支持

如遇到问题，可以：
1. 查看项目 README.md
2. 检查控制台错误日志
3. 参考 API 文档: http://localhost:8000/docs