import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.tools.subtitles import SubtitlesClip
from typing import Optional, Dict, Any, List
import tempfile

class VideoCompositor:
    """视频合成器，用于将原视频与字幕合并"""
    
    def __init__(self):
        """初始化视频合成器"""
        pass
    
    def create_subtitle_clip(self, subtitle_path: str, video_width: int, font_size: int = 24,
                           font: str = 'SimHei', color: str = 'white', stroke_color: str = 'black',
                           stroke_width: float = 1) -> List[TextClip]:
        """
        手动创建字幕剪辑列表，直接使用TextClip
        
        Args:
            subtitle_path: SRT字幕文件路径
            video_width: 视频宽度，用于字幕大小计算
            font_size: 字体大小
            font: 字体名称
            color: 字幕颜色
            stroke_color: 字幕边框颜色
            stroke_width: 字幕边框宽度
            
        Returns:
            List[TextClip]: 字幕文本剪辑列表
        """
        def parse_srt_for_manual(srt_path: str) -> list:
            """手动解析SRT文件，返回((start, end), text)格式"""
            subtitles = []
            try:
                with open(srt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    blocks = content.split('\n\n')
                    
                    for block in blocks:
                        if not block.strip():
                            continue
                        
                        lines = block.strip().split('\n')
                        if len(lines) < 3:
                            continue
                        
                        # 提取时间戳
                        time_line = lines[1]
                        if '--> ' not in time_line:
                            continue
                        
                        start_time_str, end_time_str = time_line.split('--> ')
                        start_time = self._time_to_seconds(start_time_str.strip())
                        end_time = self._time_to_seconds(end_time_str.strip())
                        
                        # 提取文本
                        text = '\n'.join(lines[2:])
                        
                        subtitles.append(((start_time, end_time), text))
            except Exception as e:
                print(f"解析SRT文件时出错: {str(e)}")
            
            return subtitles
        
        try:
            parsed_subtitles = parse_srt_for_manual(subtitle_path)
            subtitle_clips = []
            
            for (start_time, end_time), text in parsed_subtitles:
                try:
                    # 字体处理 - 使用系统Menlo字体
                    font_path = '/System/Library/Fonts/Menlo.ttc'  # 系统可用的字体
                    
                    # 创建文本剪辑 - 使用明确的字体参数
                    txt_clip = TextClip(
                        text=text,  # 在MoviePy v2.0中需要明确指定text参数
                        font=font_path,
                        font_size=int(font_size),  # 确保font_size是整数
                        color=color,
                        stroke_color=stroke_color,
                        stroke_width=stroke_width,
                        size=(video_width * 0.9, None),
                        method='caption'
                    )
                    
                    # 设置字幕的起始和结束时间
                    txt_clip = txt_clip.set_start(start_time).set_end(end_time)
                    
                    # 设置字幕位置在底部
                    txt_clip = txt_clip.with_position(('center', 'bottom')).with_margin({'bottom': 50})
                    
                    subtitle_clips.append(txt_clip)
                    
                except Exception as e:
                    print(f"创建字幕剪辑时出错: {str(e)}")
                    continue
            
            return subtitle_clips
            
        except Exception as e:
            print(f"手动创建字幕剪辑时出错: {str(e)}")
            return []
    
    def _create_subtitle_clip_fallback(self, subtitle_path: str, video_width: int, font_size: int = 24,
                                     font: str = 'SimHei', color: str = 'white', stroke_color: str = 'black',
                                     stroke_width: float = 1) -> SubtitlesClip:
        """
        备用方法创建字幕剪辑，手动解析SRT文件
        
        Args:
            与create_subtitle_clip相同
            
        Returns:
            SubtitlesClip: 字幕剪辑对象
        """
        def parse_srt(srt_path: str) -> list:
            """手动解析SRT文件"""
            subtitles = []
            try:
                with open(srt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    blocks = content.split('\n\n')
                    
                    for block in blocks:
                        if not block.strip():
                            continue
                        
                        lines = block.strip().split('\n')
                        if len(lines) < 3:
                            continue
                        
                        # 提取时间戳
                        time_line = lines[1]
                        if '--> ' not in time_line:
                            continue
                        
                        start_time_str, end_time_str = time_line.split('--> ')
                        start_time = self._time_to_seconds(start_time_str.strip())
                        end_time = self._time_to_seconds(end_time_str.strip())
                        
                        # 提取文本
                        text = '\n'.join(lines[2:])
                        
                        subtitles.append(((start_time, end_time), text))
            except Exception as e:
                print(f"解析SRT文件时出错: {str(e)}")
            
            return subtitles
        
        def make_textclip(txt: str) -> TextClip:
            """为每个字幕片段创建TextClip，确保字体参数处理正确"""
            try:
                # 确保传递字体名称字符串而非字体对象，避免'function' object has no attribute 'read'错误
                # 始终使用字符串类型的字体名称
                font_name = str(font) if font else 'SimHei'  # 提供默认字体作为备选
                text_clip = TextClip(
                    txt,
                    fontsize=font_size,
                    font=font_name,  # 使用处理过的字体名称字符串
                    color=color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_width,
                    bg_color=None,
                    size=(video_width * 0.9, None),
                    method='caption',
                    align='center'
                )
                return text_clip
            except Exception as e:
                print(f"创建文本剪辑时出错: {str(e)}")
                # 如果失败，返回空剪辑
                return ColorClip((0, 0), (0, 0, 0, 0))
        
        parsed_subtitles = parse_srt(subtitle_path)
        # 在MoviePy v2.0中，SubtitlesClip构造函数可能只接受一个参数
        # 尝试直接使用SRT解析结果创建字幕剪辑
        try:
            # 尝试使用SubtitlesClip的方式
            subtitles = SubtitlesClip(parsed_subtitles, make_textclip)
            return subtitles
        except Exception as e:
            print(f"SubtitlesClip创建失败，使用备用方法: {e}")
            # 如果失败，回到原始的视频复制方式
            return None
    
    def _time_to_seconds(self, time_str: str) -> float:
        """
        将SRT时间格式转换为秒数
        
        Args:
            time_str: SRT时间格式字符串 (HH:MM:SS,mmm)
            
        Returns:
            float: 秒数
        """
        try:
            # 替换逗号为点
            time_str = time_str.replace(',', '.')
            
            # 分割小时、分钟、秒
            parts = time_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = parts
                return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
            return 0.0
        except Exception:
            return 0.0
    
    def add_subtitles_to_video(self, video_path: str, subtitle_path: str, output_path: Optional[str] = None,
                             font_size: int = 24, font: str = 'SimHei', subtitle_position: tuple = ('center', 'bottom'),
                             margin: int = 50) -> str:
        """
        将字幕添加到视频中
        
        Args:
            video_path: 原始视频路径
            subtitle_path: SRT字幕文件路径
            output_path: 输出视频路径，默认在原视频同目录下添加_subtitled后缀
            font_size: 字体大小
            font: 字体名称
            subtitle_position: 字幕位置
            margin: 边距
            
        Returns:
            str: 输出视频路径
        """
        try:
            print(f"正在加载视频: {video_path}")
            # 使用上下文管理器加载视频以确保资源正确释放
            with VideoFileClip(video_path) as video:
                video_width = video.w
                
                # 创建字幕剪辑
                subtitle_clips = self.create_subtitle_clip(
                    subtitle_path=subtitle_path,
                    video_width=video_width,
                    font_size=font_size,
                    font=font
                )
                
                # 如果字幕创建失败，返回原始视频
                if not subtitle_clips:
                    print("字幕创建失败，返回原始视频")
                    return video_path
                
                print(f"成功创建 {len(subtitle_clips)} 个字幕剪辑")
                
                # 合成本视频和字幕
                print("正在合成视频和字幕...")
                final_clip = CompositeVideoClip([video] + subtitle_clips)
                
                # 生成输出路径
                if not output_path:
                    base_name = os.path.splitext(os.path.basename(video_path))[0]
                    output_dir = os.path.dirname(video_path)
                    output_path = os.path.join(output_dir, f"{base_name}_subtitled.mp4")
                
                # 写入输出视频
                print(f"正在保存视频: {output_path}")
                final_clip.write_videofile(
                    output_path,
                    fps=video.fps,
                    codec="libx264",
                    audio_codec="aac",
                    threads=4
                )
                
                print(f"字幕已成功添加到视频: {output_path}")
                return output_path
                
        except Exception as e:
            print(f"添加字幕时出错: {str(e)}")
            # 返回原始视频路径作为备选
            return video_path
    
    def process_video_with_subtitles(self, video_path: str, subtitle_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        处理视频并添加字幕的综合方法
        
        Args:
            video_path: 原始视频路径
            subtitle_path: SRT字幕文件路径
            output_dir: 输出目录
            
        Returns:
            Dict: 包含处理结果的字典
        """
        # 确定输出路径
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.basename(video_path)
            output_path = os.path.join(output_dir, f"subtitled_{base_name}")
        else:
            output_path = None
        
        # 添加字幕
        output_video_path = self.add_subtitles_to_video(
            video_path=video_path,
            subtitle_path=subtitle_path,
            output_path=output_path
        )
        
        return {
            'original_video': video_path,
            'subtitle_file': subtitle_path,
            'output_video': output_video_path
        }

# 简单的测试函数
if __name__ == "__main__":
    compositor = VideoCompositor()
    print("Video Compositor module loaded successfully")