from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routers import demo
from core.config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description="基于 Vue 3 + FastAPI 的空白项目模板",
    version=settings.version
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(demo.router, prefix="/api/demo", tags=["demo"])

@app.get("/")
async def root():
    return {
        "message": f"欢迎使用 {settings.app_name}",
        "version": settings.version,
        "docs": "/docs",
        "api_base": "/api"
    }

@app.get("/api")
async def api_info():
    return {
        "message": "API 基础信息",
        "version": settings.version,
        "endpoints": {
            "demo": "/api/demo",
            "health": "/api/demo/health",
            "hello": "/api/demo/hello"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
