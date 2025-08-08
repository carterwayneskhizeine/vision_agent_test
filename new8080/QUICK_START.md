# ⚡ 快速启动指南

## 🚀 一键启动

```bash
# 进入项目目录
cd new8080

# 安装前端依赖（首次运行）
cd frontend && npm install && cd ..

# 安装后端依赖（首次运行）
cd backend && pip install -r requirements.txt && cd ..

# 一键启动前端+后端
python start-dev.py
```

## 🌐 访问地址

启动成功后，在浏览器中访问：
- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8080
- **API文档**: http://localhost:8080/docs

## 📦 项目特性

- ✅ **Vue 3** + TypeScript + Vite
- ✅ **DaisyUI** + Tailwind CSS 美观界面
- ✅ **FastAPI** + Uvicorn 高性能后端
- ✅ **热重载** 开发体验
- ✅ **API代理** 前后端无缝对接
- ✅ **响应式设计** 适配各种设备

## 🛠️ 分别启动（调试用）

```bash
# 启动后端（终端1）
cd backend && python main.py

# 启动前端（终端2）
cd frontend && npm run dev
```

## 🎯 开始开发

这是一个**空白模板**，你可以：
1. 在 `frontend/src/views/` 添加新页面
2. 在 `backend/api/routers/` 添加新API
3. 修改 `frontend/src/App.vue` 调整布局
4. 查看 `Demo.vue` 了解前后端交互

## 📚 更多信息

详细说明请查看 `README.md`
