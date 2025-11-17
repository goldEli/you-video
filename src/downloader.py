import os
import yt_dlp
from typing import Optional, Dict, Any

class YouTubeDownloader:
    """YouTube视频下载器，专注于short视频的下载"""
    
    def __init__(self, output_dir: str = "./downloads"):
        """
        初始化下载器
        
        Args:
            output_dir: 下载文件的输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_short(self, url: str, filename: Optional[str] = None, cookies: Optional[str] = None) -> Dict[str, Any]:
        """
        下载YouTube short视频
        
        Args:
            url: YouTube short视频的URL
            filename: 可选的输出文件名（不含扩展名）
            cookies: 可选的cookies文件路径，用于绕过YouTube的机器人验证
            
        Returns:
            Dict: 包含下载信息的字典，包括视频路径、标题等
        """
        # 确保URL是有效的YouTube short格式
        if not self._is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL")
        
        # 配置yt-dlp选项，添加额外的选项来尝试绕过验证
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': os.path.join(self.output_dir, f'{filename or "%(title)s"}.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'merge_output_format': 'mp4',
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }
            ],
            # 添加额外选项来绕过验证
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'geo_bypass': True,
            'ignoreerrors': False,
            'retries': 5,
            'fragment_retries': 10,
            'skip_unavailable_fragments': True,
        }
        
        try:
            # 尝试使用--cookies-from-browser来绕过验证
            # 这会自动从Chrome浏览器获取cookies
            try:
                print("尝试从Chrome浏览器自动获取cookies...")
                ydl_opts['cookiesfrombrowser'] = ('chrome',)
            except Exception as e:
                print(f"从浏览器获取cookies失败: {e}")
                print("尝试其他方法...")
                
                # 如果提供了cookies文件，添加到选项中
                if cookies:
                    print(f"使用提供的cookies文件: {cookies}")
                    ydl_opts['cookiefile'] = cookies
                else:
                    print("未提供cookies文件，可能会遇到机器人验证问题")
                    print("可以使用--cookies参数提供cookies文件")
            
            print(f"开始下载视频: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                
                # 获取下载后的文件路径
                video_path = ydl.prepare_filename(info_dict)
                
                # 如果文件扩展名不是mp4，修改为mp4
                if not video_path.endswith('.mp4'):
                    base, _ = os.path.splitext(video_path)
                    video_path = base + '.mp4'
                
                result = {
                    'video_path': video_path,
                    'title': info_dict.get('title', 'Untitled'),
                    'duration': info_dict.get('duration', 0),
                    'uploader': info_dict.get('uploader', 'Unknown'),
                    'url': url
                }
                
                print(f"视频下载完成: {result['video_path']}")
                return result
                
        except Exception as e:
            print(f"下载视频时出错: {str(e)}")
            print("提示：如果遇到YouTube的机器人验证问题，您可能需要提供cookies文件")
            print("请参考: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp")
            raise
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """
        检查URL是否为有效的YouTube链接
        
        Args:
            url: 要检查的URL
            
        Returns:
            bool: 如果是有效的YouTube URL则返回True
        """
        youtube_patterns = [
            'youtube.com',
            'youtu.be',
            'youtube-nocookie.com'
        ]
        return any(pattern in url for pattern in youtube_patterns)

# 简单的测试函数
if __name__ == "__main__":
    downloader = YouTubeDownloader()
    # 这里可以添加测试代码
    print("YouTube Downloader module loaded successfully")