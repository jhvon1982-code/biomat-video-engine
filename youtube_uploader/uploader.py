"""
主上传逻辑
整合文件监控、脚本加载、YouTube上传
"""
import logging
import time
from pathlib import Path
from typing import Optional, Dict

from .config import (
    VIDEOS_DIR,
    SCRIPTS_DIR,
    UPLOADED_DIR,
    DEFAULT_CATEGORY,
    DEFAULT_PRIVACY,
    DEFAULT_IS_FOR_KIDS,
    DEFAULT_HAS_ALTERED_MEDIA,
)
from .youtube_client import YouTubeClient
from .utils import (
    load_script,
    save_upload_record,
    get_video_metadata,
    validate_script,
)

logger = logging.getLogger(__name__)


class YouTubeUploader:
    """YouTube上传器"""

    def __init__(
        self,
        youtube_client: YouTubeClient,
        videos_dir: Path = VIDEOS_DIR,
        scripts_dir: Path = SCRIPTS_DIR,
        uploaded_dir: Path = UPLOADED_DIR,
    ):
        """
        初始化上传器

        Args:
            youtube_client: YouTube客户端
            videos_dir: 视频目录
            scripts_dir: 脚本目录
            uploaded_dir: 上传记录目录
        """
        self.youtube_client = youtube_client
        self.videos_dir = videos_dir
        self.scripts_dir = scripts_dir
        self.uploaded_dir = uploaded_dir

    def upload_video(
        self,
        video_path: Path,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list] = None,
        category: str = DEFAULT_CATEGORY,
        privacy: str = DEFAULT_PRIVACY,
        is_for_kids: bool = DEFAULT_IS_FOR_KIDS,
        has_altered_media: bool = DEFAULT_HAS_ALTERED_MEDIA,
    ) -> Dict:
        """
        上传视频

        Args:
            video_path: 视频文件路径
            title: 视频标题（可选，如果不提供则从脚本读取）
            description: 视频描述（可选，如果不提供则从脚本读取）
            tags: 视频标签（可选，如果不提供则从脚本读取）
            category: 视频分类
            privacy: 隐私状态
            is_for_kids: 是否为儿童内容
            has_altered_media: 是否包含合成媒体

        Returns:
            上传结果字典
        """
        logger.info(f"[Uploader] 开始处理视频: {video_path}")

        # 1. 加载脚本（如果有）
        script = load_script(video_path, self.scripts_dir)

        if script:
            logger.info(f"[Uploader] 加载到脚本文件")

            # 验证脚本格式
            is_valid, error_msg = validate_script(script)
            if not is_valid:
                logger.warning(f"[Uploader] 脚本格式错误: {error_msg}，将使用默认值")

            # 从脚本获取元数据（如果没有提供）
            title = title or script.get("title", video_path.stem)
            description = description or script.get("description", "")
            tags = tags or script.get("tags", [])
            category = script.get("category", category)
        else:
            # 没有脚本，使用默认值
            logger.warning(f"[Uploader] 未找到脚本文件，使用默认值")
            title = title or video_path.stem
            description = description or ""
            tags = tags or []

        logger.info(f"[Uploader] 标题: {title}")
        logger.info(f"[Uploader] 描述: {description[:100]}..." if len(description) > 100 else f"[Uploader] 描述: {description}")
        logger.info(f"[Uploader] 标签: {tags}")

        # 2. 获取视频元数据
        video_metadata = get_video_metadata(video_path)
        logger.info(f"[Uploader] 视频大小: {video_metadata.get('size_mb')} MB")
        logger.info(f"[Uploader] 视频时长: {video_metadata.get('duration', 0)} 秒")

        # 3. 上传到YouTube
        result = self.youtube_client.upload_video(
            video_path=str(video_path),
            title=title,
            description=description,
            tags=tags,
            category_id=self._get_category_id(category),
            privacy_status=privacy,
            is_for_kids=is_for_kids,
            has_altered_media=has_altered_media,
        )

        # 4. 保存上传记录
        if result.get("success"):
            video_id = result.get("video_id")
            save_upload_record(video_path, video_id, self.uploaded_dir, script)
            logger.info(f"[Uploader] 上传完成: https://www.youtube.com/watch?v={video_id}")
        else:
            logger.error(f"[Uploader] 上传失败: {result.get('error')}")

        return result

    def _get_category_id(self, category_name: str) -> str:
        """
        获取YouTube分类ID

        Args:
            category_name: 分类名称

        Returns:
            分类ID
        """
        # YouTube分类ID映射
        category_map = {
            "Film & Animation": "1",
            "Autos & Vehicles": "2",
            "Music": "10",
            "Pets & Animals": "15",
            "Sports": "17",
            "Short Movies": "18",
            "Travel & Events": "19",
            "Gaming": "20",
            "Videoblogging": "21",
            "People & Blogs": "22",
            "Comedy": "23",
            "Entertainment": "24",
            "News & Politics": "25",
            "Howto & Style": "26",
            "Education": "27",
            "Science & Technology": "28",
            "Nonprofits & Activism": "29",
            "Movies": "30",
            "Anime/Animation": "31",
            "Action/Adventure": "32",
            "Classics": "33",
            "Comedy": "34",
            "Documentary": "35",
            "Drama": "36",
            "Family": "37",
            "Foreign": "38",
            "Horror": "39",
            "Sci-Fi/Fantasy": "40",
            "Thriller": "41",
            "Shorts": "42",
            "Shows": "43",
            "Trailers": "44",
        }

        return category_map.get(category_name, "22")  # 默认: People & Blogs

    def process_video(self, video_path: Path) -> Dict:
        """
        处理视频（自动加载脚本并上传）

        Args:
            video_path: 视频文件路径

        Returns:
            上传结果字典
        """
        return self.upload_video(video_path)

    def batch_upload(self, video_paths: list) -> list:
        """
        批量上传视频

        Args:
            video_paths: 视频文件路径列表

        Returns:
            上传结果列表
        """
        results = []

        for i, video_path in enumerate(video_paths, 1):
            logger.info(f"[Uploader] 批量上传 {i}/{len(video_paths)}: {video_path}")

            try:
                result = self.process_video(video_path)
                results.append(result)

                # 上传间隔，避免限流
                if i < len(video_paths):
                    time.sleep(10)

            except Exception as e:
                logger.error(f"[Uploader] 批量上传失败 {video_path}: {e}")
                results.append({
                    "success": False,
                    "error": str(e),
                    "video_path": str(video_path),
                })

        return results
