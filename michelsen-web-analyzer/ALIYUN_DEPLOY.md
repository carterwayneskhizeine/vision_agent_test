# 阿里云服务器部署指南

## 🚀 快速部署配置

### 1. 🔧 服务器网络配置

已配置支持外网访问：
- **后端服务**: `0.0.0.0:8080`  
- **前端服务**: `0.0.0.0:3000`

### 2. 🛡️ 阿里云安全组配置

**必须开放以下端口**：

| 端口 | 协议 | 源地址 | 用途 |
|------|------|--------|------|
| 3000 | TCP | 0.0.0.0/0 | 前端访问 |
| 8080 | TCP | 0.0.0.0/0 | 后端API |
| 22 | TCP | 0.0.0.0/0 | SSH连接 |

#### 🔐 安全组配置步骤：

1. 登录阿里云控制台
2. 进入 **云服务器ECS** → **实例**
3. 找到您的服务器实例，点击 **管理**
4. 左侧菜单选择 **安全组**
5. 点击安全组ID进入详情
6. 点击 **入方向** → **手动添加**
7. 添加以下规则：

```
端口范围: 3000/3000
协议类型: TCP
授权对象: 0.0.0.0/0
描述: 前端服务

端口范围: 8080/8080  
协议类型: TCP
授权对象: 0.0.0.0/0
描述: 后端API服务
```

### 3. 🌐 获取服务器公网IP

```bash
# 查看服务器公网IP
curl ifconfig.me
# 或者
curl ipinfo.io/ip
```

### 4. 🚀 启动服务

```bash
cd /root/Code/vision_agent_test/michelsen-web-analyzer
python start-dev.py
```

### 5. 🎯 访问地址

启动成功后，使用以下地址访问：

- **前端网站**: `http://YOUR_PUBLIC_IP:3000`
- **后端API**: `http://YOUR_PUBLIC_IP:8080`  
- **API文档**: `http://YOUR_PUBLIC_IP:8080/docs`

将 `YOUR_PUBLIC_IP` 替换为您的服务器公网IP地址。

### 6. 🔍 常见问题排查

#### 无法访问网站？

1. **检查安全组配置**
   ```bash
   # 测试端口是否开放
   telnet YOUR_PUBLIC_IP 3000
   telnet YOUR_PUBLIC_IP 8080
   ```

2. **检查服务状态**
   ```bash
   # 查看端口监听状态
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8080
   ```

3. **检查防火墙**
   ```bash
   # Ubuntu/Debian
   sudo ufw status
   sudo ufw allow 3000
   sudo ufw allow 8080
   
   # CentOS/RHEL
   sudo firewall-cmd --list-ports
   sudo firewall-cmd --add-port=3000/tcp --permanent
   sudo firewall-cmd --add-port=8080/tcp --permanent
   sudo firewall-cmd --reload
   ```

4. **检查服务日志**
   ```bash
   # 查看服务运行日志
   python start-dev.py
   ```

#### 性能优化建议

1. **使用生产环境构建**
   ```bash
   # 构建前端生产版本
   cd frontend && npm run build
   
   # 使用nginx服务静态文件（可选）
   sudo apt install nginx
   ```

2. **启用HTTPS（推荐）**
   - 申请SSL证书
   - 配置nginx反向代理
   - 使用443端口

### 7. 🔄 重启服务

```bash
# 停止服务
Ctrl+C

# 重新启动
python start-dev.py
```

### 8. 📊 监控服务

```bash
# 查看系统资源使用情况  
top
htop

# 查看网络连接
ss -tulpn
```

## 🎉 部署完成！

配置完成后，您可以通过公网IP地址访问迈克尔逊干涉实验AI分析系统！
