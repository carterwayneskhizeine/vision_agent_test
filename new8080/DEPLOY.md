# 🚀 部署指南

## 📦 项目打包

### 开发环境部署
```bash
# 克隆/复制项目到目标服务器
cp -r new8080 /path/to/deployment/

# 安装依赖
cd /path/to/deployment/new8080
cd frontend && npm install && cd ..
cd backend && pip install -r requirements.txt && cd ..

# 启动服务
python start-dev.py
```

### 生产环境部署

#### 1. 前端构建
```bash
cd frontend
npm run build
# 构建输出在 frontend/dist/ 目录
```

#### 2. 反向代理配置（Nginx示例）
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/new8080/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API代理
    location /api {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # API文档
    location /docs {
        proxy_pass http://localhost:8080;
    }
}
```

#### 3. 后端服务管理（systemd示例）
```ini
# /etc/systemd/system/blank-template.service
[Unit]
Description=Blank Template API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/new8080/backend
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## 🐳 Docker 部署

### Dockerfile 示例
```dockerfile
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
COPY --from=frontend-build /app/frontend/dist /app/static

EXPOSE 8080
CMD ["python", "main.py"]
```

### docker-compose.yml 示例
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ENV=production
    restart: unless-stopped
```

## ☁️ 云平台部署

### Vercel (前端)
1. 连接GitHub仓库
2. 设置构建命令：`cd frontend && npm run build`
3. 设置输出目录：`frontend/dist`
4. 配置API代理到后端服务

### Railway/Heroku (后端)
1. 添加 `Procfile`：
```
web: cd backend && python main.py
```
2. 设置环境变量
3. 配置端口动态绑定

## 🔧 配置修改

### 生产环境配置
```python
# backend/core/config.py
class Settings(BaseSettings):
    app_name: str = "空白项目模板"
    debug: bool = False  # 生产环境关闭调试
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", 8080))  # 支持动态端口
    
    # 生产环境CORS设置
    allowed_origins: List[str] = [
        "https://your-domain.com",
        "https://www.your-domain.com"
    ]
```

### 环境变量
```bash
# .env 文件
ENV=production
DEBUG=false
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

## 📊 监控和日志

### 日志配置
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### 健康检查
```bash
# 自动健康检查脚本
#!/bin/bash
curl -f http://localhost:8080/api/demo/health || exit 1
```

## 🔒 安全建议

1. **HTTPS配置**：生产环境必须使用HTTPS
2. **API限流**：添加请求频率限制
3. **输入验证**：严格验证所有用户输入
4. **错误处理**：不暴露敏感错误信息
5. **依赖更新**：定期更新依赖包

## 📈 性能优化

1. **前端优化**
   - 启用gzip压缩
   - 配置CDN
   - 图片懒加载

2. **后端优化**
   - 使用连接池
   - 启用缓存
   - 数据库索引优化

## 🆘 故障排除

常见问题和解决方案请参考 `TEST_GUIDE.md`
