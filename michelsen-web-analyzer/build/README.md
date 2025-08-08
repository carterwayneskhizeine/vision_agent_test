# 迈克尔逊干涉实验 AI 分析系统 - 发布版本

🎆 **版本**: v1.0.0  
📅 **构建时间**: 2025-08-09 00:32:04  
💻 **运行平台**: Windows / Linux / macOS

## 🚀 快速启动

### Windows 用户
```bash
# 双击运行
start.bat

# 或在命令行中运行
.\start.bat
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
