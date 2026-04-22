"""
文件监控系统
监控指定文件夹，检测新视频文件
"""
import logging
import time
from pathlib import Path
from typing import Callable, Optional, Set

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

from .config import (
    VIDEOS_DIR,
    VIDEO_EXTENSIONS,
    WATCH_INTERVAL,
)
from .utils import is_video_file

logger = logging.getLogger(__name__)


class VideoFileHandler(FileSystemEventHandler):
    """视频文件事件处理器"""

    def __init__(self, callback: Callable[[Path], None], extensions: Set[str]):
        """
        初始化处理器

        Args:
            callback: 检测到新视频时的回调函数
            extensions: 支持的视频扩展名集合
        """
        super().__init__()
        self.callback = callback
        self.extensions = extensions
        self.processed_files: Set[Path] = set()

    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if is_video_file(file_path, self.extensions):
            logger.info(f"[VideoFileHandler] 检测到新视频: {file_path}")

            # 避免重复处理
            if file_path not in self.processed_files:
                self.processed_files.add(file_path)

                # 等待文件完全写入
                self._wait_for_file_ready(file_path)

                # 调用回调
                try:
                    self.callback(file_path)
                except Exception as e:
                    logger.error(f"[VideoFileHandler] 处理视频失败: {e}")

    def on_moved(self, event):
        """文件移动事件"""
        if event.is_directory:
            return

        dest_path = Path(event.dest_path)

        if is_video_file(dest_path, self.extensions):
            logger.info(f"[VideoFileHandler] 检测到移动的视频: {dest_path}")

            if dest_path not in self.processed_files:
                self.processed_files.add(dest_path)
                self._wait_for_file_ready(dest_path)

                try:
                    self.callback(dest_path)
                except Exception as e:
                    logger.error(f"[VideoFileHandler] 处理视频失败: {e}")

    def _wait_for_file_ready(self, file_path: Path, timeout: int = 30):
        """
        等待文件完全写入

        Args:
            file_path: 文件路径
            timeout: 超时时间（秒）
        """
        start_time = time.time()
        last_size = 0

        while time.time() - start_time < timeout:
            try:
                current_size = file_path.stat().st_size

                # 文件大小稳定，认为写入完成
                if current_size > 0 and current_size == last_size:
                    time.sleep(1)  # 再等待1秒确保稳定
                    return

                last_size = current_size
                time.sleep(0.5)

            except FileNotFoundError:
                # 文件被删除或移动
                time.sleep(0.5)

        logger.warning(f"[VideoFileHandler] 文件 {file_path} 可能在 {timeout} 秒后仍在写入")


class VideoWatcher:
    """视频文件监控器"""

    def __init__(
        self,
        watch_dir: Path = VIDEOS_DIR,
        callback: Optional[Callable[[Path], None]] = None,
        extensions: Optional[Set[str]] = None,
    ):
        """
        初始化监控器

        Args:
            watch_dir: 监控的目录
            callback: 检测到新视频时的回调函数
            extensions: 支持的视频扩展名集合
        """
        if not WATCHDOG_AVAILABLE:
            raise ImportError("watchdog库未安装，请运行: pip install watchdog")

        self.watch_dir = watch_dir
        self.callback = callback or self._default_callback
        self.extensions = extensions or VIDEO_EXTENSIONS
        self.observer = None

        # 确保监控目录存在
        self.watch_dir.mkdir(parents=True, exist_ok=True)

    def _default_callback(self, file_path: Path):
        """默认回调函数"""
        logger.info(f"[VideoWatcher] 检测到新视频: {file_path}")

    def start(self):
        """启动监控"""
        if self.observer is not None and self.observer.is_alive():
            logger.warning("[VideoWatcher] 监控器已在运行")
            return

        # 创建事件处理器
        event_handler = VideoFileHandler(self.callback, self.extensions)

        # 创建观察者
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_dir), recursive=False)

        # 启动观察者
        self.observer.start()
        logger.info(f"[VideoWatcher] 开始监控目录: {self.watch_dir}")

    def stop(self):
        """停止监控"""
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            logger.info("[VideoWatcher] 已停止监控")

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()


class SimpleVideoScanner:
    """简单的视频扫描器（轮询方式）"""

    def __init__(
        self,
        scan_dir: Path = VIDEOS_DIR,
        callback: Optional[Callable[[Path], None]] = None,
        extensions: Optional[Set[str]] = None,
        interval: int = WATCH_INTERVAL,
    ):
        """
        初始化扫描器

        Args:
            scan_dir: 扫描的目录
            callback: 检测到新视频时的回调函数
            extensions: 支持的视频扩展名集合
            interval: 扫描间隔（秒）
        """
        self.scan_dir = scan_dir
        self.callback = callback or self._default_callback
        self.extensions = extensions or VIDEO_EXTENSIONS
        self.interval = interval
        self.processed_files: Set[Path] = set()

        # 确保扫描目录存在
        self.scan_dir.mkdir(parents=True, exist_ok=True)

    def _default_callback(self, file_path: Path):
        """默认回调函数"""
        logger.info(f"[SimpleVideoScanner] 检测到新视频: {file_path}")

    def scan_once(self):
        """执行一次扫描"""
        # 获取所有视频文件
        video_files = [
            f for f in self.scan_dir.iterdir()
            if f.is_file() and is_video_file(f, self.extensions)
        ]

        for video_file in video_files:
            if video_file not in self.processed_files:
                self.processed_files.add(video_file)
                logger.info(f"[SimpleVideoScanner] 发现新视频: {video_file}")

                try:
                    self.callback(video_file)
                except Exception as e:
                    logger.error(f"[SimpleVideoScanner] 处理视频失败: {e}")

    def run(self):
        """持续运行扫描"""
        logger.info(f"[SimpleVideoScanner] 开始扫描目录: {self.scan_dir}")
        logger.info(f"[SimpleVideoScanner] 扫描间隔: {self.interval}秒")

        try:
            while True:
                self.scan_once()
                time.sleep(self.interval)

        except KeyboardInterrupt:
            logger.info("[SimpleVideoScanner] 收到中断信号，停止扫描")
        except Exception as e:
            logger.error(f"[SimpleVideoScanner] 扫描出错: {e}")

    def clear_processed(self):
        """清除已处理记录"""
        self.processed_files.clear()
        logger.info("[SimpleVideoScanner] 已清除已处理记录")
