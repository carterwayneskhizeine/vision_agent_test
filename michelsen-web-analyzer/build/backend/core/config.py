from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "迈克尔逊干涉实验 AI 分析系统"
    debug: bool = True
    version: str = "1.0.0"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8080
    
    # CORS 配置
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # 文件上传配置
    upload_dir: str = "uploads"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_video_extensions: List[str] = [".mp4", ".avi", ".mov"]
    
    # 静态文件配置
    static_dir: str = "static"
    screenshots_dir: str = "static/screenshots"
    videos_dir: str = "static/videos"
    
    # AI 分析配置
    analysis_timeout: int = 300  # 5分钟
    default_frame_interval: int = 30  # 30秒
    
    # 外部 API 配置
    anthropic_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()