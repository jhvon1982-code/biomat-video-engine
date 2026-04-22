"""
YouTube自动上传工具 - 主入口
"""
import sys
import os
import logging
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_uploader.config import (
    BASE_DIR,
    WORKSPACE_DIR,
    VIDEOS_DIR,
    SCRIPTS_DIR,
    UPLOADED_DIR,
    YOUTUBE_CONFIG,
    LOG_FILE,
    LOG_LEVEL,
    WATCH_INTERVAL,
)
from youtube_uploader.youtube_client import YouTubeClient, authenticate
from youtube_uploader.watcher import VideoWatcher, SimpleVideoScanner
from youtube_uploader.uploader import YouTubeUploader


def setup_logging():
    """配置日志"""
    log_file = WORKSPACE_DIR / LOG_FILE

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("YouTube自动上传工具启动")
    logger.info(f"工作空间: {WORKSPACE_DIR}")
    logger.info(f"视频目录: {VIDEOS_DIR}")
    logger.info(f"脚本目录: {SCRIPTS_DIR}")
    logger.info(f"上传记录: {UPLOADED_DIR}")
    logger.info("=" * 60)


def create_youtube_client():
    """创建YouTube客户端"""
    client_secrets_file = BASE_DIR / YOUTUBE_CONFIG["client_secrets_file"]
    credentials_file = WORKSPACE_DIR / YOUTUBE_CONFIG["credentials_file"]

    logger = logging.getLogger(__name__)

    if not client_secrets_file.exists():
        logger.error(f"OAuth2客户端密钥文件不存在: {client_secrets_file}")
        logger.error("请按照README.md中的说明配置OAuth2认证")
        sys.exit(1)

    try:
        client = YouTubeClient(
            str(client_secrets_file),
            str(credentials_file)
        )
        logger.info("YouTube客户端创建成功")
        return client
    except Exception as e:
        logger.error(f"创建YouTube客户端失败: {e}")
        logger.error("如果凭证文件不存在，请先运行: python main.py --auth")
        sys.exit(1)


def cmd_auth(args):
    """OAuth2认证命令"""
    logger = logging.getLogger(__name__)

    client_secrets_file = BASE_DIR / YOUTUBE_CONFIG["client_secrets_file"]
    credentials_file = WORKSPACE_DIR / YOUTUBE_CONFIG["credentials_file"]

    if not client_secrets_file.exists():
        logger.error(f"OAuth2客户端密钥文件不存在: {client_secrets_file}")
        sys.exit(1)

    logger.info("开始OAuth2认证流程...")
    authenticate(str(client_secrets_file), str(credentials_file))
    logger.info("认证完成！")


def cmd_upload(args):
    """上传单个视频命令"""
    logger = logging.getLogger(__name__)

    video_path = Path(args.video)
    if not video_path.exists():
        logger.error(f"视频文件不存在: {video_path}")
        sys.exit(1)

    # 创建客户端和上传器
    client = create_youtube_client()
    uploader = YouTubeUploader(
        client,
        VIDEOS_DIR,
        SCRIPTS_DIR,
        UPLOADED_DIR
    )

    # 上传视频
    result = uploader.process_video(video_path)

    if result.get("success"):
        logger.info("上传成功!")
        logger.info(f"YouTube URL: {result.get('youtube_url')}")
    else:
        logger.error(f"上传失败: {result.get('error')}")
        sys.exit(1)


def cmd_watch(args):
    """监控模式命令"""
    logger = logging.getLogger(__name__)

    # 创建客户端和上传器
    client = create_youtube_client()
    uploader = YouTubeUploader(
        client,
        VIDEOS_DIR,
        SCRIPTS_DIR,
        UPLOADED_DIR
    )

    # 创建监控器
    if args.simple:
        logger.info("使用简单轮询模式")
        scanner = SimpleVideoScanner(
            VIDEOS_DIR,
            callback=uploader.process_video,
            interval=args.interval or WATCH_INTERVAL
        )
        scanner.run()
    else:
        logger.info("使用文件系统监控模式（需要watchdog库）")
        watcher = VideoWatcher(
            VIDEOS_DIR,
            callback=uploader.process_video
        )

        try:
            watcher.start()
            logger.info("监控器已启动，按Ctrl+C停止")
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("收到中断信号")
        finally:
            watcher.stop()


def cmd_batch(args):
    """批量上传命令"""
    logger = logging.getLogger(__name__)

    # 扫描所有视频
    video_files = list(VIDEOS_DIR.glob("*.mp4")) + list(VIDEOS_DIR.glob("*.mov"))

    if not video_files:
        logger.info(f"视频目录中没有视频文件: {VIDEOS_DIR}")
        return

    logger.info(f"找到 {len(video_files)} 个视频文件")

    # 创建客户端和上传器
    client = create_youtube_client()
    uploader = YouTubeUploader(
        client,
        VIDEOS_DIR,
        SCRIPTS_DIR,
        UPLOADED_DIR
    )

    # 批量上传
    results = uploader.batch_upload(video_files)

    # 统计结果
    success_count = sum(1 for r in results if r.get("success"))
    logger.info(f"批量上传完成: {success_count}/{len(results)} 成功")


def cmd_status(args):
    """查看状态命令"""
    logger = logging.getLogger(__name__)

    logger.info(f"工作空间: {WORKSPACE_DIR}")
    logger.info(f"视频目录: {VIDEOS_DIR}")

    # 统计视频数量
    video_files = list(VIDEOS_DIR.glob("*.mp4")) + list(VIDEOS_DIR.glob("*.mov"))
    logger.info(f"视频文件数量: {len(video_files)}")

    # 统计脚本数量
    script_files = list(SCRIPTS_DIR.glob("*.json"))
    logger.info(f"脚本文件数量: {len(script_files)}")

    # 统计上传记录
    upload_records = list(UPLOADED_DIR.glob("*.json"))
    logger.info(f"上传记录数量: {len(upload_records)}")

    # 列出最近的上传记录
    if upload_records:
        logger.info("\n最近的上传记录:")
        import json
        from datetime import datetime

        # 按上传时间排序
        upload_records.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        for record_file in upload_records[:10]:
            with open(record_file, 'r') as f:
                record = json.load(f)

            uploaded_time = datetime.fromisoformat(record.get("uploaded_at"))
            logger.info(f"  - {record.get('video_name')}")
            logger.info(f"    URL: {record.get('youtube_url')}")
            logger.info(f"    时间: {uploaded_time}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="YouTube自动上传工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # auth命令
    auth_parser = subparsers.add_parser("auth", help="OAuth2认证")
    auth_parser.set_defaults(func=cmd_auth)

    # upload命令
    upload_parser = subparsers.add_parser("upload", help="上传单个视频")
    upload_parser.add_argument("video", help="视频文件路径")
    upload_parser.set_defaults(func=cmd_upload)

    # watch命令
    watch_parser = subparsers.add_parser("watch", help="监控模式（自动上传新视频）")
    watch_parser.add_argument("--simple", action="store_true", help="使用简单轮询模式")
    watch_parser.add_argument("--interval", type=int, help="轮询间隔（秒）")
    watch_parser.set_defaults(func=cmd_watch)

    # batch命令
    batch_parser = subparsers.add_parser("batch", help="批量上传所有视频")
    batch_parser.set_defaults(func=cmd_batch)

    # status命令
    status_parser = subparsers.add_parser("status", help="查看状态")
    status_parser.set_defaults(func=cmd_status)

    # 解析参数
    args = parser.parse_args()

    # 设置日志
    setup_logging()

    # 如果没有指定命令，显示帮助
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行命令
    args.func(args)


if __name__ == "__main__":
    main()
