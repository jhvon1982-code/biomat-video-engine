"""
YouTube API客户端
"""
import os
import logging
from pathlib import Path
from typing import Dict, Optional

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False

logger = logging.getLogger(__name__)


class YouTubeClient:
    """YouTube API客户端"""

    # OAuth2权限范围
    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
    ]

    def __init__(self, client_secrets_file: str, credentials_file: str):
        """
        初始化YouTube客户端

        Args:
            client_secrets_file: OAuth2客户端密钥文件路径
            credentials_file: 凭证保存文件路径
        """
        if not GOOGLE_LIBS_AVAILABLE:
            raise ImportError("Google API库未安装，请运行: pip install google-auth google-api-python-client")

        self.client_secrets_file = client_secrets_file
        self.credentials_file = credentials_file
        self.credentials = None
        self.service = None

        # 加载凭证
        self._load_credentials()

        # 构建服务
        self._build_service()

    def _load_credentials(self):
        """加载或刷新OAuth2凭证"""
        if os.path.exists(self.credentials_file):
            self.credentials = Credentials.from_authorized_user_file(
                self.credentials_file, self.SCOPES
            )

        # 如果凭证不存在或过期，刷新凭证
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                logger.info("[YouTubeClient] 凭证已过期，正在刷新...")
                self.credentials.refresh(Request())
            else:
                logger.error("[YouTubeClient] 凭证不存在或无法刷新，请先进行OAuth2认证")
                raise Exception("需要OAuth2认证")

            # 保存凭证
            with open(self.credentials_file, 'w') as token:
                token.write(self.credentials.to_json())

    def _build_service(self):
        """构建YouTube服务"""
        self.service = build(
            "youtube",
            "v3",
            credentials=self.credentials
        )
        logger.info("[YouTubeClient] YouTube服务已构建")

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: Optional[list] = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "public",
        is_for_kids: bool = False,
        has_altered_media: bool = False,
    ) -> Dict:
        """
        上传视频到YouTube

        Args:
            video_path: 视频文件路径
            title: 视频标题
            description: 视频描述
            tags: 视频标签列表
            category_id: 视频分类ID
            privacy_status: 隐私状态 (public, private, unlisted)
            is_for_kids: 是否为儿童内容
            has_altered_media: 是否包含合成媒体

        Returns:
            上传结果字典，包含video_id
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")

        if not self.service:
            raise Exception("YouTube服务未初始化")

        # 构建视频元数据
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": is_for_kids,
            },
        }

        # 如果包含合成媒体，添加声明
        if has_altered_media:
            body["status"]["containsSyntheticMedia"] = True

        logger.info(f"[YouTubeClient] 开始上传视频: {video_path}")
        logger.info(f"[YouTubeClient] 标题: {title}")

        # 创建上传请求
        media = MediaFileUpload(
            video_path,
            mimetype="video/*",
            resumable=True
        )

        request = self.service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        # 执行上传（带进度监控）
        response = None
        try:
            response = request.execute(num_retries=5)

            video_id = response.get("id")
            logger.info(f"[YouTubeClient] 上传成功! Video ID: {video_id}")
            logger.info(f"[YouTubeClient] YouTube URL: https://www.youtube.com/watch?v={video_id}")

            return {
                "success": True,
                "video_id": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "response": response,
            }

        except HttpError as e:
            logger.error(f"[YouTubeClient] 上传失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": e.resp.status,
            }

    def get_video_status(self, video_id: str) -> Dict:
        """
        获取视频状态

        Args:
            video_id: YouTube视频ID

        Returns:
            视频状态字典
        """
        try:
            response = self.service.videos().list(
                part="status,processingDetails",
                id=video_id
            ).execute()

            if not response.get("items"):
                return {"error": "视频不存在"}

            video = response["items"][0]
            status = video.get("status", {})
            processing = video.get("processingDetails", {})

            return {
                "uploadStatus": status.get("uploadStatus"),
                "privacyStatus": status.get("privacyStatus"),
                "license": status.get("license"),
                "processingStatus": processing.get("processingStatus"),
                "processingProgress": processing.get("processingProgress"),
            }

        except HttpError as e:
            logger.error(f"[YouTubeClient] 获取视频状态失败: {e}")
            return {"error": str(e)}


def authenticate(client_secrets_file: str, credentials_file: str):
    """
    OAuth2认证流程（本地运行时使用）

    Args:
        client_secrets_file: OAuth2客户端密钥文件路径
        credentials_file: 凭证保存文件路径
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        scopes=YouTubeClient.SCOPES
    )

    # 运行OAuth流程
    credentials = flow.run_local_server(port=0)

    # 保存凭证
    with open(credentials_file, 'w') as token:
        token.write(credentials.to_json())

    logger.info(f"[YouTubeClient] OAuth2认证成功，凭证已保存到: {credentials_file}")
