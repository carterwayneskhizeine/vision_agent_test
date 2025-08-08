# 🚀 快速打包指南

## ⚡ 一键打包

```bash
# 进入项目目录
cd michelsen-web-analyzer

# 完整打包（推荐）
python build-package.py all

# 仅生产版本
python build-package.py prod

# 仅开发版本  
python build-package.py dev
```

## 📦 打包输出

| 文件 | 大小 | 用途 |
|------|------|------|
| `michelsen-analyzer-dev-YYYYMMDD.zip` | ~85KB | 开发调试版（含源码） |
| `michelsen-analyzer-v1.0.0-YYYYMMDD.zip` | ~164KB | 生产部署版（优化） |

## 🎯 使用方法

### 生产版本部署
1. **解压** `michelsen-analyzer-v1.0.0-*.zip`
2. **Windows**: 双击 `start.bat`
3. **Linux/Mac**: 运行 `./start.sh`
4. **访问**: http://localhost:8080

### 系统要求
- Python 3.8+
- 4GB+ RAM
- 2GB+ 磁盘空间

## 🛠️ 高级选项

```bash
# 清理构建文件
python build-package.py clean

# 仅构建前端
python build-package.py frontend

# 仅准备后端
python build-package.py backend

# 使用 npm 脚本
npm run build         # 完整构建
npm run build:prod    # 生产版本
npm run build:dev     # 开发版本
```

## 📞 支持

遇到问题？查看 `BUILD.md` 获取详细说明。
