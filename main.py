#!/usr/bin/env python3
"""
YouTube Short 下载与中文字幕生成工具

本工具可以下载YouTube短视频，提取音频，进行语音识别，
将英文内容翻译成中文，并为视频添加中文字幕。
"""

import os
import sys
import argparse
import time
from typing import Optional

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入项目模块
from downloader import YouTubeDownloader
from translator import AudioTranslator
from compositor import VideoCompositor

def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='YouTube Short 下载与中文字幕生成工具')
    
    parser.add_argument('url', help='YouTube Short 视频的URL')
    parser.add_argument('--output-dir', '-o', default='./downloads',
                      help='输出目录，默认: ./downloads')
    parser.add_argument('--filename', '-f', help='自定义输出文件名（不含扩展名）')
    parser.add_argument('--model', '-m', default='base',
                      choices=['tiny', 'base', 'small', 'medium', 'large'],
                      help='Whisper 模型大小，默认: base')
    parser.add_argument('--font-size', type=int, default=24,
                      help='字幕字体大小，默认: 24')
    parser.add_argument('--font', default='SimHei',
                      help='字幕字体，默认: SimHei')
    parser.add_argument('--skip-download', action='store_true',
                      help='跳过下载步骤，直接处理本地视频')
    parser.add_argument('--video-path', help='本地视频文件路径（当使用--skip-download时）')
    parser.add_argument('--cookies', help='YouTube cookies文件路径，用于绕过机器人验证')
    
    return parser.parse_args()

def process_video(args):
    """
    处理视频的主函数
    
    Args:
        args: 命令行参数
    """
    start_time = time.time()
    
    try:
        # 创建输出目录
        os.makedirs(args.output_dir, exist_ok=True)
        
        # 1. 下载视频（如果需要）
        if args.skip_download:
            if not args.video_path:
                print("错误: 使用 --skip-download 时必须提供 --video-path")
                return
            if not os.path.exists(args.video_path):
                print(f"错误: 视频文件不存在: {args.video_path}")
                return
            video_info = {
                'video_path': args.video_path,
                'title': os.path.splitext(os.path.basename(args.video_path))[0]
            }
            print(f"跳过下载，使用本地视频: {args.video_path}")
        else:
            downloader = YouTubeDownloader(output_dir=args.output_dir)
            video_info = downloader.download_short(args.url, filename=args.filename, cookies=args.cookies)
        
        print("=" * 50)
        print(f"视频信息:")
        print(f"标题: {video_info['title']}")
        print(f"路径: {video_info['video_path']}")
        if 'duration' in video_info:
            print(f"时长: {video_info['duration']} 秒")
        print("=" * 50)
        
        # 2. 音频提取、语音识别和翻译
        print("\n开始处理音频和字幕...")
        translator = AudioTranslator(model_name=args.model)
        translation_result = translator.process_video(video_info['video_path'])
        
        print("=" * 50)
        print("语音识别和翻译完成:")
        print(f"原始英文字幕: {translation_result['original_srt_path']}")
        print(f"中文字幕: {translation_result['translated_srt_path']}")
        print(f"识别文本长度: {len(translation_result['transcription'])} 字符")
        print(f"字幕片段数量: {len(translation_result['segments'])}")
        print("=" * 50)
        
        # 3. 视频合成
        print("\n开始合成视频与字幕...")
        compositor = VideoCompositor()
        composition_result = compositor.process_video_with_subtitles(
            video_path=video_info['video_path'],
            subtitle_path=translation_result['translated_srt_path'],
            output_dir=args.output_dir
        )
        
        # 4. 总结
        end_time = time.time()
        total_time = end_time - start_time
        
        print("\n" + "=" * 50)
        print("✅ 处理完成！")
        print(f"📹 原始视频: {composition_result['original_video']}")
        print(f"📝 字幕文件: {composition_result['subtitle_file']}")
        print(f"🎬 输出视频: {composition_result['output_video']}")
        print(f"⏱️  总耗时: {total_time:.2f} 秒")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n❌ 处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

def check_dependencies():
    """
    检查系统依赖
    """
    try:
        # 尝试导入所有需要的库
        import yt_dlp
        import whisper
        import pydub
        import moviepy.editor
        import deep_translator
        return True
    except ImportError as e:
        print(f"依赖库缺失: {e}")
        print("请使用以下命令安装依赖:")
        print("  uv pip install -e .")
        return False

def main():
    """
    主函数
    """
    print("🎬 YouTube Short 下载与中文字幕生成工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 解析参数
    args = parse_arguments()
    
    # 处理视频
    process_video(args)

if __name__ == "__main__":
    main()