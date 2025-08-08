# 🚀 空白项目模板

基于 Vue 3 + FastAPI 的空白项目模板，端口配置为 8080。

## 📋 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 快速构建工具  
- **TypeScript** - 类型安全
- **DaisyUI** - 美观的UI组件库
- **Tailwind CSS** - 实用优先的CSS框架
- **Vue Router** - 路由管理
- **Pinia** - 状态管理
- **Axios** - HTTP客户端

### 后端
- **FastAPI** - 现代Python Web框架
- **Uvicorn** - ASGI服务器
- **Pydantic** - 数据验证
- **CORS** - 跨域支持

## 🚀 快速开始

### 安装依赖
```bash
# 安装前端依赖
cd frontend && npm install && cd ..

# 安装后端依赖  
cd backend && pip install -r requirements.txt && cd ..
```

### 启动服务

#### 方式一：一键启动（推荐）
```bash
python start-dev.py
```

#### 方式二：分别启动
```bash
# 启动后端（终端1）
cd backend && python main.py

# 启动前端（终端2）  
cd frontend && npm run dev
```

## 🌐 访问地址

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8080  
- **API文档**: http://localhost:8080/docs

## 📁 项目结构

```
new8080/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── components/      # 通用组件
│   │   ├── router/          # 路由配置
│   │   └── main.ts          # 入口文件
│   ├── package.json         # 前端依赖
│   └── vite.config.ts       # Vite配置
├── backend/                 # 后端项目  
│   ├── api/                 # API路由
│   ├── core/                # 核心配置
│   ├── main.py              # 主程序
│   └── requirements.txt     # 后端依赖
├── start-dev.py             # 开发环境启动
└── README.md                # 项目说明
```

## 🛠️ 开发说明

这是一个**空白项目模板**，包含：
- ✅ 基础的前后端框架配置
- ✅ 开发环境启动脚本
- ✅ 跨域配置和API代理
- ✅ 基本的路由和页面结构
- ✅ TypeScript 类型支持

你可以在此基础上快速开发你的应用！

## 📞 技术支持

如有问题，请参考：
- Vue 3 文档：https://vuejs.org/
- FastAPI 文档：https://fastapi.tiangolo.com/
- DaisyUI 文档：https://daisyui.com/
