from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import json
import uuid
from typing import Dict, Any, Optional
import asyncio

from core.config import settings
from services.analyzer_service import ExperimentAnalysisService
from api.routers.upload import uploaded_files

router = APIRouter()

# 全局变量存储分析结果
analysis_results: Dict[str, Dict[str, Any]] = {}
analysis_status: Dict[str, Dict[str, Any]] = {}

@router.post("/start")
async def start_analysis(background_tasks: BackgroundTasks, include_device_detection: bool = True):
    """开始 AI 分析"""
    
    # 检查文件是否已上传
    if not all(uploaded_files.values()):
        raise HTTPException(
            status_code=400, 
            detail="请先上传老师示范视频和学生实验视频"
        )
    
    # 生成分析 ID
    analysis_id = str(uuid.uuid4())
    
    # 初始化分析状态
    analysis_status[analysis_id] = {
        "status": "running",
        "progress": 0,
        "current_step": "正在初始化分析...",
        "include_device_detection": include_device_detection,
        "created_at": "",  # TODO: 添加时间戳
        "error": None
    }
    
    # 后台异步执行分析
    background_tasks.add_task(run_analysis, analysis_id, include_device_detection)
    
    return {
        "success": True,
        "analysis_id": analysis_id,
        "message": "分析已开始，请查询进度"
    }

async def run_analysis(analysis_id: str, include_device_detection: bool):
    """异步执行分析任务"""
    try:
        service = ExperimentAnalysisService()
        
        # 获取上传的文件路径
        teacher_path = uploaded_files["teacher"]["filepath"]
        student_path = uploaded_files["student"]["filepath"]
        
        # 执行分析，传递进度回调
        async def progress_callback(step: str, progress: int):
            analysis_status[analysis_id].update({
                "current_step": step,
                "progress": progress
            })
        
        # 调用分析服务
        result = await service.analyze_experiment(
            teacher_path=teacher_path,
            student_path=student_path,
            include_device_detection=include_device_detection,
            progress_callback=progress_callback
        )
        
        # 保存结果
        analysis_results[analysis_id] = result
        analysis_status[analysis_id].update({
            "status": "completed",
            "progress": 100,
            "current_step": "分析完成!"
        })
        
    except Exception as e:
        analysis_status[analysis_id].update({
            "status": "error",
            "error": str(e),
            "current_step": f"分析失败: {str(e)}"
        })

@router.get("/progress/{analysis_id}")
async def get_analysis_progress(analysis_id: str):
    """获取分析进度"""
    if analysis_id not in analysis_status:
        raise HTTPException(status_code=404, detail="分析任务不存在")
    
    return analysis_status[analysis_id]

@router.get("/results/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """获取分析结果"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    return analysis_results[analysis_id]

@router.get("/screenshots/{filename}")
async def get_screenshot(filename: str):
    """获取分析截图"""
    screenshot_path = Path(settings.screenshots_dir) / filename
    
    if not screenshot_path.exists():
        raise HTTPException(status_code=404, detail="截图文件不存在")
    
    return FileResponse(
        path=screenshot_path,
        media_type="image/png",
        filename=filename
    )

@router.get("/list")
async def list_analyses():
    """获取所有分析记录"""
    return {
        "analyses": list(analysis_status.keys()),
        "count": len(analysis_status)
    }

@router.delete("/clear")
async def clear_analyses():
    """清空所有分析记录"""
    global analysis_results, analysis_status
    analysis_results.clear()
    analysis_status.clear()
    
    return {
        "success": True,
        "message": "所有分析记录已清空"
    }