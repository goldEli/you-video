"""YouTube Short 下载与中文字幕生成工具包"""

# 从各个模块导入主要类和函数
from .downloader import YouTubeDownloader
from .translator import AudioTranslator
# 暂时移除compositor的导入，避免依赖问题

__version__ = "0.1.0"
__all__ = [
    "YouTubeDownloader",
    "AudioTranslator",
    # "VideoCompositor"
]