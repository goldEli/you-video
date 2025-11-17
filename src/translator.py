import os
import whisper
from pydub import AudioSegment
from deep_translator import GoogleTranslator
from typing import List, Dict, Any, Optional
import json
import tempfile

class AudioTranslator:
    """音频提取、语音识别和翻译器"""
    
    def __init__(self, model_name: str = "base"):
        """
        初始化翻译器
        
        Args:
            model_name: Whisper模型名称 (tiny, base, small, medium, large)
        """
        print(f"正在加载Whisper模型: {model_name}")
        self.whisper_model = whisper.load_model(model_name)
        self.translator = GoogleTranslator(source='en', target='zh-CN')
    
    def extract_audio(self, video_path: str) -> str:
        """
        从视频中提取音频
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            str: 提取的音频文件路径
        """
        try:
            print(f"正在从视频中提取音频: {video_path}")
            
            # 创建临时音频文件
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_dir = os.path.join(os.path.dirname(video_path), "audio")
            os.makedirs(audio_dir, exist_ok=True)
            audio_path = os.path.join(audio_dir, f"{base_name}.wav")
            
            # 使用pydub提取音频
            audio = AudioSegment.from_file(video_path, format="mp4")
            audio.export(audio_path, format="wav")
            
            print(f"音频提取完成: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"提取音频时出错: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_path: str, language: str = "en") -> Dict[str, Any]:
        """
        使用Whisper进行语音识别
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码，默认为英语
            
        Returns:
            Dict: 包含识别结果的字典
        """
        try:
            print(f"正在进行语音识别: {audio_path}")
            
            # 使用Whisper进行语音识别
            result = self.whisper_model.transcribe(audio_path, language=language)
            
            print(f"语音识别完成，检测到文本长度: {len(result['text'])} 字符")
            return result
            
        except Exception as e:
            print(f"语音识别时出错: {str(e)}")
            raise
    
    def translate_segments(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        翻译语音识别的片段
        
        Args:
            segments: Whisper识别的片段列表
            
        Returns:
            List[Dict]: 包含翻译后文本的片段列表
        """
        translated_segments = []
        
        for i, segment in enumerate(segments):
            try:
                # 翻译文本
                original_text = segment['text'].strip()
                if original_text:
                    translated_text = self.translator.translate(original_text)
                    
                    # 创建包含翻译的新片段
                    translated_segment = segment.copy()
                    translated_segment['translated_text'] = translated_text
                    translated_segments.append(translated_segment)
                    
                    print(f"翻译片段 {i+1}/{len(segments)}: {original_text[:30]}... -> {translated_text[:30]}...")
                else:
                    translated_segments.append(segment)
                    
            except Exception as e:
                print(f"翻译片段时出错: {str(e)}")
                # 出错时保留原文本
                translated_segments.append(segment)
        
        return translated_segments
    
    def generate_srt(self, segments: List[Dict[str, Any]], output_path: str, use_translated: bool = True) -> str:
        """
        生成SRT字幕文件
        
        Args:
            segments: 包含文本的片段列表
            output_path: 输出SRT文件的路径
            use_translated: 是否使用翻译后的文本
            
        Returns:
            str: SRT文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments):
                    # 写入序号
                    f.write(f"{i+1}\n")
                    
                    # 写入时间戳
                    start_time = self._format_time(segment['start'])
                    end_time = self._format_time(segment['end'])
                    f.write(f"{start_time} --> {end_time}\n")
                    
                    # 写入文本
                    if use_translated and 'translated_text' in segment:
                        f.write(f"{segment['translated_text']}\n")
                    else:
                        f.write(f"{segment['text']}\n")
                    
                    # 空行分隔
                    f.write("\n")
            
            print(f"SRT字幕文件已生成: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"生成SRT文件时出错: {str(e)}")
            raise
    
    def process_video(self, video_path: str) -> Dict[str, Any]:
        """
        处理视频文件：提取音频、语音识别、翻译
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            Dict: 包含处理结果的字典
        """
        # 提取音频
        audio_path = self.extract_audio(video_path)
        
        # 语音识别
        transcription_result = self.transcribe_audio(audio_path)
        
        # 翻译文本
        translated_segments = self.translate_segments(transcription_result['segments'])
        
        # 生成SRT文件
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        srt_dir = os.path.join(os.path.dirname(video_path), "subtitles")
        os.makedirs(srt_dir, exist_ok=True)
        
        # 生成原文字幕
        original_srt_path = os.path.join(srt_dir, f"{base_name}_en.srt")
        self.generate_srt(translated_segments, original_srt_path, use_translated=False)
        
        # 生成中文字幕
        translated_srt_path = os.path.join(srt_dir, f"{base_name}_zh.srt")
        self.generate_srt(translated_segments, translated_srt_path, use_translated=True)
        
        result = {
            'video_path': video_path,
            'audio_path': audio_path,
            'original_srt_path': original_srt_path,
            'translated_srt_path': translated_srt_path,
            'transcription': transcription_result['text'],
            'segments': translated_segments
        }
        
        return result
    
    def _format_time(self, seconds: float) -> str:
        """
        将秒数格式化为SRT时间戳格式
        
        Args:
            seconds: 秒数
            
        Returns:
            str: 格式化的时间戳 (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

# 简单的测试函数
if __name__ == "__main__":
    translator = AudioTranslator(model_name="base")
    print("Audio Translator module loaded successfully")