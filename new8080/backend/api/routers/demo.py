from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@router.get("/hello")
async def hello_world() -> Dict[str, Any]:
    """示例API端点"""
    return {
        "message": "Hello World!",
        "status": "success",
        "data": {
            "framework": "FastAPI",
            "port": 8080,
            "description": "这是一个空白项目模板的示例API"
        }
    }

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """健康检查端点"""
    return {"status": "healthy", "service": "backend"}

@router.post("/echo")
async def echo(data: Dict[str, Any]) -> Dict[str, Any]:
    """回显API，返回发送的数据"""
    return {
        "message": "数据接收成功",
        "received_data": data,
        "status": "success"
    }
