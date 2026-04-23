"""
文件上传和YouTube自动上传API
独立的API服务，不依赖coze_coding_dev_sdk
"""
import os
import json
import logging
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="YouTube自动上传API", version="1.0.0")

# 添加CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取工作目录
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKSPACE_DIR = BASE_DIR / "workspace"
VIDEOS_DIR = WORKSPACE_DIR / "videos"
SCRIPTS_DIR = WORKSPACE_DIR / "scripts"
UPLOADED_DIR = WORKSPACE_DIR / "uploaded"

# 确保目录存在
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADED_DIR.mkdir(parents=True, exist_ok=True)

# 验证API key
def validate_api_key(request: Request) -> bool:
    """验证API key"""
    # 这里可以添加API key验证逻辑
    # 暂时允许所有请求
    return True


# ========================================
# YouTube上传工具集成
# ========================================

youtube_client = None
youtube_uploader = None

# OAuth2凭证文件路径
credentials_file = BASE_DIR / "workspace" / "youtube_credentials.json"
client_secrets_file = BASE_DIR / "config" / "youtube_client_secrets.json"

# 尝试初始化YouTube客户端
try:
    from youtube_uploader.youtube_client import YouTubeClient
    from youtube_uploader.uploader import YouTubeUploader
    from youtube_uploader.utils import (
        load_script,
        get_video_metadata,
        save_upload_record,
        validate_script,
    )

    if credentials_file.exists() and client_secrets_file.exists():
        try:
            youtube_client = YouTubeClient(
                str(client_secrets_file),
                str(credentials_file)
            )
            youtube_uploader = YouTubeUploader(
                youtube_client,
                VIDEOS_DIR,
                SCRIPTS_DIR,
                UPLOADED_DIR
            )
            logger.info("[API] YouTube客户端初始化成功")
        except Exception as e:
            logger.warning(f"[API] YouTube客户端初始化失败: {e}")
    else:
        logger.warning(f"[API] YouTube OAuth2未配置: credentials={credentials_file.exists()}, client_secrets={client_secrets_file.exists()}")
except ImportError as e:
    logger.warning(f"[API] YouTube上传工具未安装: {e}")
except Exception as e:
    logger.error(f"[API] YouTube客户端初始化错误: {e}")


# ========================================
# API端点
# ========================================

@app.get("/")
async def root():
    """根端点"""
    return {
        "service": "YouTube自动上传API",
        "version": "1.0.0",
        "status": "running",
        "youtube_configured": youtube_uploader is not None
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "youtube_configured": youtube_uploader is not None,
        "workspace": {
            "videos_dir": str(VIDEOS_DIR),
            "scripts_dir": str(SCRIPTS_DIR),
            "uploaded_dir": str(UPLOADED_DIR)
        }
    }


@app.post("/api/v1/upload/video")
async def upload_video(
    request: Request,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    auto_upload_youtube: bool = Form(False)
):
    """
    上传视频文件

    Args:
        file: 视频文件
        title: 视频标题（可选）
        description: 视频描述（可选）
        tags: 视频标签（逗号分隔，可选）
        auto_upload_youtube: 是否自动上传到YouTube（默认False）
    """
    try:
        # 验证API key
        if not validate_api_key(request):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

        # 验证文件类型
        allowed_extensions = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式，仅支持: {', '.join(allowed_extensions)}"
            )

        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        original_name = Path(file.filename).stem
        video_filename = f"{original_name}_{file_id}{file_ext}"
        video_path = VIDEOS_DIR / video_filename

        # 保存视频文件
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"[API] 视频上传成功: {video_filename} ({video_path.stat().st_size / 1024 / 1024:.2f} MB)")

        # 准备返回数据
        result = {
            "success": True,
            "message": "视频上传成功",
            "data": {
                "video_id": file_id,
                "video_filename": video_filename,
                "video_path": str(video_path),
                "video_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
                "original_filename": file.filename,
                "title": title,
                "description": description,
                "tags": tags.split(",") if tags else [],
            },
            "youtube_upload": None,
            "youtube_configured": youtube_uploader is not None
        }

        # 如果配置了自动上传YouTube
        if auto_upload_youtube and youtube_uploader:
            logger.info(f"[API] 开始自动上传到YouTube...")

            # 准备上传参数
            upload_params = {
                "video_path": video_path,
            }

            if title:
                upload_params["title"] = title
            if description:
                upload_params["description"] = description
            if tags:
                upload_params["tags"] = tags.split(",")

            # 上传到YouTube
            youtube_result = youtube_uploader.upload_video(**upload_params)
            result["youtube_upload"] = youtube_result

            if not youtube_result.get("success"):
                logger.error(f"[API] YouTube上传失败: {youtube_result.get('error')}")
            else:
                logger.info(f"[API] YouTube上传成功: {youtube_result.get('youtube_url')}")
        elif auto_upload_youtube:
            logger.warning(f"[API] 无法自动上传到YouTube（YouTube未配置）")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] 视频上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"视频上传失败: {str(e)}")


@app.post("/api/v1/upload/script")
async def upload_script(
    request: Request,
    file: UploadFile = File(...),
    video_filename: str = Form(...)
):
    """
    上传脚本文件

    Args:
        file: JSON脚本文件
        video_filename: 对应的视频文件名（不含路径）
    """
    try:
        # 验证API key
        if not validate_api_key(request):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

        # 验证文件类型
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="只支持JSON格式的脚本文件")

        # 验证脚本内容
        content = await file.read()
        try:
            script = json.loads(content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="脚本文件格式错误，必须是有效的JSON")

        # 验证脚本格式
        is_valid, error_msg = validate_script(script) if youtube_uploader else (True, "")
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"脚本格式错误: {error_msg}")

        # 保存脚本文件（使用视频文件名）
        script_filename = f"{Path(video_filename).stem}.json"
        script_path = SCRIPTS_DIR / script_filename

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(script, ensure_ascii=False, indent=2))

        logger.info(f"[API] 脚本上传成功: {script_filename}")

        return {
            "success": True,
            "message": "脚本上传成功",
            "data": {
                "script_filename": script_filename,
                "script_path": str(script_path),
                "video_filename": video_filename,
                "script": script
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] 脚本上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"脚本上传失败: {str(e)}")


@app.get("/api/v1/upload/list")
async def list_uploads(request: Request):
    """
    列出所有已上传的文件

    Returns:
        视频列表和脚本列表
    """
    try:
        # 验证API key
        if not validate_api_key(request):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

        # 获取所有视频文件
        video_files = []
        for video_file in VIDEOS_DIR.glob("*.mp4"):
            video_files.append({
                "filename": video_file.name,
                "path": str(video_file),
                "size_mb": round(video_file.stat().st_size / 1024 / 1024, 2),
                "created_time": datetime.fromtimestamp(video_file.stat().st_ctime).isoformat(),
                "has_script": (SCRIPTS_DIR / f"{video_file.stem}.json").exists()
            })

        # 获取所有脚本文件
        script_files = []
        for script_file in SCRIPTS_DIR.glob("*.json"):
            try:
                with open(script_file, 'r', encoding='utf-8') as f:
                    script = json.load(f)

                script_files.append({
                    "filename": script_file.name,
                    "path": str(script_file),
                    "title": script.get("title", ""),
                    "description": script.get("description", ""),
                    "tags": script.get("tags", [])
                })
            except Exception as e:
                logger.warning(f"[API] 读取脚本失败 {script_file}: {e}")

        # 获取上传记录
        upload_records = []
        for record_file in UPLOADED_DIR.glob("*.json"):
            try:
                with open(record_file, 'r', encoding='utf-8') as f:
                    record = json.load(f)

                upload_records.append({
                    "filename": record.get("video_name"),
                    "youtube_video_id": record.get("youtube_video_id"),
                    "youtube_url": record.get("youtube_url"),
                    "uploaded_at": record.get("uploaded_at")
                })
            except Exception as e:
                logger.warning(f"[API] 读取上传记录失败 {record_file}: {e}")

        return {
            "success": True,
            "data": {
                "videos": video_files,
                "scripts": script_files,
                "upload_records": upload_records,
                "statistics": {
                    "total_videos": len(video_files),
                    "total_scripts": len(script_files),
                    "total_uploads": len(upload_records),
                    "youtube_configured": youtube_uploader is not None
                }
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] 列出文件失败: {e}")
        raise HTTPException(status_code=500, detail=f"列出文件失败: {str(e)}")


@app.delete("/api/v1/upload/video/{filename}")
async def delete_video(filename: str, request: Request):
    """
    删除视频文件

    Args:
        filename: 视频文件名
    """
    try:
        # 验证API key
        if not validate_api_key(request):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

        video_path = VIDEOS_DIR / filename

        if not video_path.exists():
            raise HTTPException(status_code=404, detail="视频文件不存在")

        # 删除视频文件
        video_path.unlink()

        # 删除对应的脚本文件（如果存在）
        script_path = SCRIPTS_DIR / f"{video_path.stem}.json"
        if script_path.exists():
            script_path.unlink()

        logger.info(f"[API] 删除视频成功: {filename}")

        return {
            "success": True,
            "message": "视频删除成功"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] 删除视频失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除视频失败: {str(e)}")


@app.post("/api/v1/upload/youtube/{filename}")
async def upload_to_youtube(filename: str, request: Request):
    """
    手动上传视频到YouTube

    Args:
        filename: 视频文件名
    """
    try:
        # 验证API key
        if not validate_api_key(request):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

        if not youtube_uploader:
            raise HTTPException(
                status_code=400,
                detail="YouTube OAuth2未配置，无法上传到YouTube"
            )

        video_path = VIDEOS_DIR / filename

        if not video_path.exists():
            raise HTTPException(status_code=404, detail="视频文件不存在")

        logger.info(f"[API] 手动上传到YouTube: {filename}")

        # 上传到YouTube
        result = youtube_uploader.process_video(video_path)

        if result.get("success"):
            return {
                "success": True,
                "message": "上传成功",
                "data": result
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"YouTube上传失败: {result.get('error')}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] YouTube上传失败: {e}")
        raise HTTPException(status_code=500, detail=f"YouTube上传失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
