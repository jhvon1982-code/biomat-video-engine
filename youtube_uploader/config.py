"""
YouTube上传工具配置
"""
import os
from pathlib import Path

# 基础路径
BASE_DIR = Path(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"))

# 工作空间路径
WORKSPACE_DIR = BASE_DIR / "workspace"
VIDEOS_DIR = WORKSPACE_DIR / "videos"
SCRIPTS_DIR = WORKSPACE_DIR / "scripts"
UPLOADED_DIR = WORKSPACE_DIR / "uploaded"

# 监控间隔（秒）
WATCH_INTERVAL = 60

# 支持的视频格式
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# 支持的脚本格式
SCRIPT_EXTENSIONS = {".json"}

# YouTube配置
YOUTUBE_CONFIG = {
    "client_secrets_file": "config/youtube_client_secrets.json",
    "credentials_file": "workspace/youtube_credentials.json",
    "api_service_name": "youtube",
    "api_version": "v3",
}

# 默认视频分类
DEFAULT_CATEGORY = "People & Blogs"

# 默认隐私状态
DEFAULT_PRIVACY = "public"

# 默认儿童内容标记
DEFAULT_IS_FOR_KIDS = False

# 默认合成媒体标记
DEFAULT_HAS_ALTERED_MEDIA = False

# 日志配置
LOG_FILE = "youtube_uploader.log"
LOG_LEVEL = "INFO"

# 通知配置
ENABLE_NOTIFICATIONS = False
NOTIFICATION_WEBHOOK = None  # 可以配置webhook URL

# 确保目录存在
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADED_DIR.mkdir(parents=True, exist_ok=True)
