"""
工具函数
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def load_script(video_path: Path, scripts_dir: Path) -> Optional[Dict]:
    """
    加载视频对应的脚本文件

    Args:
        video_path: 视频文件路径
        scripts_dir: 脚本目录路径

    Returns:
        脚本内容字典，如果不存在返回None
    """
    # 获取视频文件名（不含扩展名）
    video_name = video_path.stem

    # 查找对应的脚本文件
    script_files = list(scripts_dir.glob(f"{video_name}.*.json"))

    if not script_files:
        # 尝试直接匹配文件名
        script_file = scripts_dir / f"{video_name}.json"
        if script_file.exists():
            script_files = [script_file]

    if not script_files:
        logger.info(f"[Utils] 未找到视频 {video_name} 的脚本文件")
        return None

    # 使用第一个找到的脚本文件
    script_file = script_files[0]

    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            script = json.load(f)
        logger.info(f"[Utils] 成功加载脚本: {script_file}")
        return script
    except Exception as e:
        logger.error(f"[Utils] 加载脚本失败 {script_file}: {e}")
        return None


def save_upload_record(video_path: Path, youtube_video_id: str, uploaded_dir: Path, script: Optional[Dict] = None):
    """
    保存上传记录

    Args:
        video_path: 视频文件路径
        youtube_video_id: YouTube视频ID
        uploaded_dir: 上传记录目录
        script: 脚本内容（可选）
    """
    video_name = video_path.stem

    record = {
        "video_name": video_name,
        "video_path": str(video_path),
        "youtube_video_id": youtube_video_id,
        "youtube_url": f"https://www.youtube.com/watch?v={youtube_video_id}",
        "uploaded_at": datetime.now().isoformat(),
        "script": script,
    }

    record_file = uploaded_dir / f"{video_name}.json"

    try:
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        logger.info(f"[Utils] 保存上传记录: {record_file}")
    except Exception as e:
        logger.error(f"[Utils] 保存上传记录失败: {e}")


def is_video_file(file_path: Path, extensions: set) -> bool:
    """
    判断是否是视频文件

    Args:
        file_path: 文件路径
        extensions: 允许的扩展名集合

    Returns:
        是否是视频文件
    """
    return file_path.suffix.lower() in extensions


def get_video_metadata(video_path: Path) -> Dict:
    """
    获取视频元数据

    Args:
        video_path: 视频文件路径

    Returns:
        视频元数据字典
    """
    import subprocess

    metadata = {
        "filename": video_path.name,
        "size_bytes": video_path.stat().st_size,
        "size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
    }

    try:
        # 使用ffprobe获取视频信息
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)

            # 获取视频流信息
            video_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
            if video_streams:
                video_stream = video_streams[0]
                metadata.update({
                    "duration": float(video_stream.get("duration", 0)),
                    "width": video_stream.get("width"),
                    "height": video_stream.get("height"),
                    "fps": eval(video_stream.get("r_frame_rate", "0/1")),
                    "codec": video_stream.get("codec_name"),
                })

    except Exception as e:
        logger.warning(f"[Utils] 获取视频元数据失败: {e}")

    return metadata


def validate_script(script: Dict) -> Tuple[bool, str]:
    """
    验证脚本格式

    Args:
        script: 脚本内容字典

    Returns:
        (是否有效, 错误信息)
    """
    required_fields = ["title", "description"]

    for field in required_fields:
        if field not in script or not script[field]:
            return False, f"缺少必需字段: {field}"

    return True, ""
