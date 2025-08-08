#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迈克尔逊干涉实验 AI 分析系统 - 项目打包工具
支持多种打包方式：开发版、生产版、完整可执行程序
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

class ProjectBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.frontend_dir = self.project_root / "frontend"
        self.backend_dir = self.project_root / "backend"
        
    def clean(self):
        """清理构建目录"""
        print("🧹 清理构建目录...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        print("✅ 构建目录已清理")
    
    def build_frontend(self):
        """构建前端生产版本"""
        print("🎨 构建前端...")
        
        # 检查 Node.js 环境
        try:
            result = subprocess.run(["node", "--version"], check=True, capture_output=True, text=True, shell=True)
            print(f"✅ Node.js 版本: {result.stdout.strip()}")
            result = subprocess.run(["npm", "--version"], check=True, capture_output=True, text=True, shell=True)
            print(f"✅ npm 版本: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("❌ Node.js 或 npm 未安装或未添加到 PATH")
        
        # 安装依赖
        print("📦 安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=self.frontend_dir, check=True, shell=True)
        
        # 构建生产版本
        print("⚡ 构建前端生产版本...")
        subprocess.run(["npm", "run", "build"], cwd=self.frontend_dir, check=True, shell=True)
        
        # 复制构建结果
        frontend_dist = self.frontend_dir / "dist"
        if frontend_dist.exists():
            shutil.copytree(frontend_dist, self.build_dir / "frontend_dist")
            print("✅ 前端构建完成")
        else:
            raise RuntimeError("❌ 前端构建失败")
    
    def prepare_backend(self):
        """准备后端文件"""
        print("🔧 准备后端文件...")
        
        backend_build = self.build_dir / "backend"
        backend_build.mkdir(exist_ok=True)
        
        # 复制后端源码
        for item in self.backend_dir.iterdir():
            if item.name in ["__pycache__", "uploads", "static"]:
                continue
            if item.is_dir():
                dest_dir = backend_build / item.name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(item, dest_dir)
            else:
                shutil.copy2(item, backend_build / item.name)
        
        # 创建启动脚本
        self.create_production_scripts()
        
        print("✅ 后端文件准备完成")
    
    def create_production_scripts(self):
        """创建生产环境启动脚本"""
        print("📝 创建生产环境脚本...")
        
        # Windows 启动脚本
        windows_script = self.build_dir / "start.bat"
        windows_script.write_text("""@echo off
echo 🚀 启动迈克尔逊干涉实验 AI 分析系统...
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python 环境
    echo 请先安装 Python 3.8+ 
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 安装Python依赖...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 创建必要目录
if not exist "uploads" mkdir uploads
if not exist "static" mkdir static
if not exist "static\\screenshots" mkdir static\\screenshots  
if not exist "static\\videos" mkdir static\\videos
if not exist "static\\images" mkdir static\\images
if not exist "static\\reports" mkdir static\\reports

REM 启动服务器
echo.
echo 🌐 系统地址: http://localhost:8080
echo 📚 API文档: http://localhost:8080/docs  
echo 🛑 停止服务: Ctrl+C
echo.
python main.py

pause
""", encoding='utf-8')
        
        # Linux/Mac 启动脚本
        linux_script = self.build_dir / "start.sh"
        linux_script.write_text("""#!/bin/bash
echo "🚀 启动迈克尔逊干涉实验 AI 分析系统..."
echo

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 环境"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 创建必要目录
mkdir -p uploads static/screenshots static/videos static/images static/reports

# 启动服务器
echo
echo "🌐 系统地址: http://localhost:8080"
echo "📚 API文档: http://localhost:8080/docs"
echo "🛑 停止服务: Ctrl+C"
echo
python3 main.py
""", encoding='utf-8')
        
        # 设置执行权限
        if os.name != 'nt':  # 非 Windows 系统
            os.chmod(linux_script, 0o755)
        
        print("✅ 生产环境脚本创建完成")
    
    def create_readme(self):
        """创建打包版本的说明文档"""
        readme_content = f"""# 迈克尔逊干涉实验 AI 分析系统 - 发布版本

🎆 **版本**: v1.0.0  
📅 **构建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
💻 **运行平台**: Windows / Linux / macOS

## 🚀 快速启动

### Windows 用户
```bash
# 双击运行
start.bat

# 或在命令行中运行
.\\start.bat
```

### Linux/macOS 用户
```bash
# 赋予执行权限并运行
chmod +x start.sh
./start.sh
```

## 📋 系统要求

### 最低要求
- **Python**: 3.8 或更高版本
- **内存**: 4GB RAM
- **硬盘**: 2GB 可用空间
- **网络**: 用于AI模型下载（首次运行）

### 推荐配置
- **Python**: 3.10+
- **内存**: 8GB RAM
- **硬盘**: 5GB 可用空间
- **GPU**: 支持CUDA（可选，用于加速AI分析）

## 🌐 访问地址

启动成功后，在浏览器中访问：
- **系统主页**: http://localhost:8080
- **API文档**: http://localhost:8080/docs

## 📁 目录结构

```
michelsen-analyzer/
├── backend/                 # 后端API服务
│   ├── main.py             # 主程序入口
│   ├── requirements.txt    # Python依赖
│   └── ...
├── frontend_dist/          # 前端静态文件 
├── start.bat              # Windows启动脚本
├── start.sh               # Linux/Mac启动脚本
└── README.md              # 本文件
```

## 🔧 故障排除

### 常见问题

1. **端口占用错误**
   - 确保 8080 端口未被其他程序占用
   - 或修改 `backend/core/config.py` 中的端口设置

2. **Python依赖安装失败**
   - 确保网络连接正常
   - 尝试使用国内镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

3. **AI分析失败**
   - 确保视频文件格式正确（支持 .mp4, .avi, .mov）
   - 检查视频文件大小（建议小于 50MB）

### 技术支持

如需技术支持，请提供以下信息：
- 操作系统版本
- Python版本
- 错误信息截图
- 日志文件内容

## 📚 使用说明

1. **上传视频**: 分别上传老师示范视频和学生实验视频
2. **开始分析**: 点击"开始AI分析"按钮
3. **查看结果**: 分析完成后自动跳转到结果页面
4. **导出报告**: 可下载分析报告和截图

## ⚡ 性能优化建议

- 使用 SSD 硬盘提升文件读写速度
- 关闭不必要的后台程序释放内存
- 首次运行需要下载AI模型，请耐心等待

---

🎯 **项目主页**: 迈克尔逊干涉实验 AI 分析系统  
📧 **技术支持**: 请参考项目文档或联系开发团队
"""
        
        readme_file = self.build_dir / "README.md"
        readme_file.write_text(readme_content, encoding='utf-8')
        
        print("✅ 说明文档创建完成")
    
    def package_development(self):
        """打包开发版本（包含源码）"""
        print("📦 创建开发版本包...")
        
        dev_package = self.dist_dir / f"michelsen-analyzer-dev-{datetime.now().strftime('%Y%m%d')}.zip"
        
        with zipfile.ZipFile(dev_package, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 添加所有源码文件
            for root, dirs, files in os.walk(self.project_root):
                # 排除不需要的目录
                dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'build', 'dist', 'uploads', 'static']]
                
                for file in files:
                    if file.endswith(('.pyc', '.pyo', '.log', '.tmp')):
                        continue
                    
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.project_root)
                    zf.write(file_path, arc_path)
        
        print(f"✅ 开发版本包创建完成: {dev_package}")
        return dev_package
    
    def package_production(self):
        """打包生产版本"""
        print("📦 创建生产版本包...")
        
        prod_package = self.dist_dir / f"michelsen-analyzer-v1.0.0-{datetime.now().strftime('%Y%m%d')}.zip"
        
        with zipfile.ZipFile(prod_package, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 添加构建文件
            for root, dirs, files in os.walk(self.build_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.build_dir)
                    zf.write(file_path, arc_path)
        
        print(f"✅ 生产版本包创建完成: {prod_package}")
        return prod_package
    
    def build_all(self):
        """完整构建流程"""
        print("🎆 开始完整构建流程...")
        print("=" * 60)
        
        try:
            # 1. 清理目录
            self.clean()
            
            # 2. 构建前端
            self.build_frontend()
            
            # 3. 准备后端
            self.prepare_backend()
            
            # 4. 创建生产脚本
            self.create_readme()
            
            # 5. 打包
            dev_package = self.package_development()
            prod_package = self.package_production()
            
            print("=" * 60)
            print("🎉 构建完成！")
            print(f"📦 开发版本: {dev_package}")
            print(f"🚀 生产版本: {prod_package}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ 构建失败: {e}")
            return False

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "all"
    
    builder = ProjectBuilder()
    
    if command == "clean":
        builder.clean()
    elif command == "frontend":
        builder.build_frontend()
    elif command == "backend":
        builder.prepare_backend()
    elif command == "dev":
        builder.clean()
        builder.package_development()
    elif command == "prod":
        builder.clean()
        builder.build_frontend()
        builder.prepare_backend()
        builder.create_readme()
        builder.package_production()
    elif command == "all":
        builder.build_all()
    else:
        print("""
🎆 迈克尔逊干涉实验 AI 分析系统 - 构建工具

用法: python build-package.py [command]

命令:
  all      完整构建（默认）
  clean    清理构建目录
  frontend 仅构建前端
  backend  仅准备后端
  dev      打包开发版本
  prod     打包生产版本

示例:
  python build-package.py all
  python build-package.py prod
        """)

if __name__ == "__main__":
    main()
