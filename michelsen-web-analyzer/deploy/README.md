# 部署说明

## 服务器端部署步骤

### 1. 同步代码
```bash
cd /root/Code/vision_agent_test
git pull
```

### 2. 运行部署脚本
```bash
cd /root/Code/vision_agent_test/michelsen-web-analyzer
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

### 3. 设置API密钥
```bash
# 编辑环境变量文件
nano /etc/systemd/system/michelsen_analyzer.env

# 设置你的API密钥
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key
```

### 4. 重启服务
```bash
systemctl restart michelsen_analyzer.service
```

### 5. 配置Nginx
在宝塔面板中添加网站配置，或将 `deploy/nginx_lab_score.conf` 的内容添加到Nginx配置中。

关键配置点：
- 前端静态文件：`/root/Code/vision_agent_test/michelsen-web-analyzer/frontend/dist`
- 后端代理：`http://127.0.0.1:8080`
- 域名：`lab-score.fantasy-lab.com`

### 6. 验证部署
```bash
# 检查服务状态
systemctl status michelsen_analyzer.service

# 检查端口监听
ss -lntp | grep :8080

# 测试后端
curl http://127.0.0.1:8080/health

# 查看日志
journalctl -u michelsen_analyzer.service -f
```

## 常见问题

### 服务无法启动
```bash
# 查看详细错误
journalctl -u michelsen_analyzer.service -n 50

# 检查环境变量
cat /etc/systemd/system/michelsen_analyzer.env

# 手动测试启动
cd /root/Code/vision_agent_test/michelsen-web-analyzer/backend
/root/miniconda3/envs/va/bin/python main.py
```

### 前端无法访问
- 确保Nginx配置正确
- 检查前端是否已构建：`ls /root/Code/vision_agent_test/michelsen-web-analyzer/frontend/dist`
- 检查域名解析

### API调用失败
- 检查CORS配置
- 确认后端服务在8080端口监听
- 检查API密钥是否设置正确