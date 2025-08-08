# 🚀 项目打包指南

迈克尔逊干涉实验 AI 分析系统提供了多种打包方式，适应不同的部署需求。

## 📋 打包方式总览

| 打包方式 | 适用场景 | 文件大小 | 运行要求 |
|----------|----------|----------|----------|
| **开发版包** | 开发/调试/源码分享 | ~50MB | Python + Node.js |
| **生产版包** | 服务器部署/用户安装 | ~30MB | Python |
| **可执行文件** | 单机部署/免环境运行 | ~500MB | 无需其他环境 |

## 🛠️ 打包前准备

### 1. 检查环境
```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 Node.js 版本（需要 16+）
node --version
npm --version

# 检查 Git 状态
git status
```

### 2. 安装打包依赖
```bash
# 安装前端依赖
cd frontend && npm install && cd ..

# 安装后端依赖  
pip install -r backend/requirements.txt

# 安装可执行文件打包工具（可选）
pip install pyinstaller
```

## 🎯 快速打包

### 方式一：使用项目脚本（推荐）
```bash
# 进入项目目录
cd michelsen-web-analyzer

# 完整打包（生产版 + 开发版）
python build-package.py all

# 仅打包生产版本
python build-package.py prod

# 仅打包开发版本
python build-package.py dev
```

### 方式二：使用 npm 脚本
```bash
# 完整构建
npm run build

# 仅构建前端
npm run build:frontend

# 打包生产版
npm run build:prod

# 打包开发版
npm run build:dev

# 创建可执行文件
npm run build:exe
```

## 📦 详细打包说明

### 1. 开发版包 📚
**用途**: 开发调试、源码分享、二次开发

```bash
python build-package.py dev
```

**包含内容**:
- 完整源代码
- 配置文件
- 启动脚本
- 文档说明

**运行要求**:
- Python 3.8+
- Node.js 16+ 
- npm 包管理器

### 2. 生产版包 🚀
**用途**: 服务器部署、最终用户安装

```bash
python build-package.py prod
```

**包含内容**:
- 前端构建后的静态文件
- 后端 Python 源码
- 自动启动脚本（Windows/Linux）
- 用户说明文档

**运行要求**:
- Python 3.8+
- pip 包管理器

### 3. 可执行文件 💎
**用途**: 单机部署、无环境依赖运行

```bash
python build-executable.py
```

**特点**:
- 无需 Python 环境
- 一键启动
- 文件较大（~500MB）
- 启动稍慢

## 📁 输出文件说明

打包完成后，文件位于 `dist/` 目录：

```
dist/
├── michelsen-analyzer-dev-20241213.zip     # 开发版包
├── michelsen-analyzer-v1.0.0-20241213.zip # 生产版包  
└── michelsen-analyzer/                     # 可执行文件目录
    ├── michelsen-analyzer.exe              # 可执行文件（Windows）
    ├── michelsen-analyzer                   # 可执行文件（Linux/Mac）
    └── ...                                 # 依赖文件
```

## 🎯 用户使用说明

### 生产版包使用
1. **解压文件**到目标目录
2. **Windows**: 双击 `start.bat`
3. **Linux/Mac**: 运行 `./start.sh` 
4. **浏览器打开**: http://localhost:8080

### 可执行文件使用
1. **解压文件**到目标目录
2. **Windows**: 双击 `michelsen-analyzer.exe`
3. **Linux/Mac**: 运行 `./michelsen-analyzer`
4. **浏览器打开**: http://localhost:8080

## 🔧 高级选项

### 自定义构建配置

编辑 `build-package.py` 可以自定义：
- 输出目录
- 包含/排除的文件
- 版本号和构建信息
- 启动脚本内容

### 优化可执行文件大小

```bash
# 使用 UPX 压缩（需要单独安装 UPX）
python build-executable.py --upx

# 排除不需要的模块
# 编辑 build-executable.py 中的 excludes 列表
```

## 🐛 常见问题

### 1. 前端构建失败
```bash
# 清理 node_modules 重新安装
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 2. 可执行文件过大
- 检查是否包含了不必要的依赖
- 使用虚拟环境减少依赖冲突
- 考虑使用 Docker 容器化部署

### 3. 打包后运行失败
- 检查 Python 路径是否正确
- 确保所有依赖都在 requirements.txt 中
- 检查文件权限设置

## 📊 性能建议

### 打包性能优化
- 使用 SSD 硬盘提升构建速度
- 关闭杀毒软件实时扫描
- 使用本地镜像源加速下载

### 运行性能优化
- 生产版包启动最快
- 可执行文件首次启动较慢
- 建议运行内存 4GB+

## 📝 版本管理

```bash
# 更新版本号（在 package.json 中）
{
  "version": "1.1.0"
}

# 构建时会自动包含版本信息
python build-package.py prod

# 生成的文件名包含版本
michelsen-analyzer-v1.1.0-20241213.zip
```

---

🎯 更多信息请参考 `README.md` 和 `DEVELOPMENT.md`  
📧 技术支持：请联系开发团队
