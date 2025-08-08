# 🧪 测试指南

## 📋 测试步骤

### 1. 后端测试
```bash
# 启动后端
cd backend && python main.py

# 测试API（新开终端）
curl http://localhost:8080
curl http://localhost:8080/api/demo/hello
curl http://localhost:8080/api/demo/health

# 访问API文档
# 浏览器打开: http://localhost:8080/docs
```

### 2. 前端测试
```bash
# 启动前端（新开终端）
cd frontend && npm run dev

# 访问前端界面
# 浏览器打开: http://localhost:3000
```

### 3. 全栈测试
```bash
# 一键启动前后端
python start-dev.py

# 测试页面功能
# 1. 访问首页: http://localhost:3000
# 2. 点击"查看演示"
# 3. 测试API调用功能
```

## ✅ 预期结果

### 后端API响应
```json
{
  "message": "欢迎使用 空白项目模板",
  "version": "1.0.0",
  "docs": "/docs",
  "api_base": "/api"
}
```

### 演示页面功能
- ✅ Hello World API 调用成功
- ✅ 健康检查返回 "healthy"
- ✅ Echo API 回显数据正确
- ✅ 前后端代理工作正常

## 🐛 常见问题

**端口占用错误**
- 确保8080端口未被占用
- 或修改 `backend/core/config.py` 中的端口

**前端无法代理到后端**
- 检查 `vite.config.ts` 代理配置
- 确保后端已启动在8080端口

**依赖安装失败**
- 检查Python和Node.js版本
- 使用国内镜像源加速下载

## 📊 性能测试

```bash
# 简单压力测试（可选）
curl -w "@/dev/null" -o /dev/null -s -X GET http://localhost:8080/api/demo/hello
```

## 🔧 调试模式

开启详细日志：
```bash
# 后端调试
cd backend && uvicorn main:app --reload --log-level debug

# 前端调试  
cd frontend && npm run dev -- --debug
```
