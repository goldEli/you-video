# YouTube Short 下载与中文字幕生成工具

一个自动化工具，用于下载 YouTube Short 视频，提取音频，进行语音识别，将英文内容翻译成中文，并为视频添加中文字幕。

## 功能特点

- 📥 自动下载 YouTube Short 视频
- 🔊 从视频中提取音频
- 🎤 使用 OpenAI Whisper 进行语音识别（英文）
- 🌐 将英文内容翻译成中文
- 📝 生成 SRT 格式的英文字幕和中文字幕
- 🎬 将中文字幕添加到视频中
- 🎯 支持命令行操作，易于使用

## 安装说明

### 1. 环境要求

- Python 3.10 或更高版本
- uv 包管理器
- FFmpeg（用于音频提取和视频处理）

### 2. 安装依赖

首先确保已安装 FFmpeg。在不同系统上的安装方法：

**macOS**:
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**:
- 下载 FFmpeg 二进制文件：https://ffmpeg.org/download.html
- 将 FFmpeg 添加到系统 PATH

### 3. 安装项目

使用 uv 安装项目及其依赖：

```bash
# 克隆仓库后进入项目目录
cd you-video1

# 使用 uv 安装
uv pip install -e .
```

## 使用方法

### 基本使用

下载 YouTube Short 并生成带中文字幕的视频：

```bash
python main.py "https://www.youtube.com/shorts/视频ID"
```

### 指定输出目录

```bash
python main.py "https://www.youtube.com/shorts/视频ID" --output-dir ./my_videos
```

### 自定义文件名

```bash
python main.py "https://www.youtube.com/shorts/视频ID" --filename "my_short"
```

### 使用更大的 Whisper 模型（提高识别准确率）

```bash
python main.py "https://www.youtube.com/shorts/视频ID" --model medium
```

### 自定义字幕字体大小

```bash
python main.py "https://www.youtube.com/shorts/视频ID" --font-size 28
```

### 处理本地视频文件

```bash
python main.py "" --skip-download --video-path ./local_video.mp4
```

```bash
uv run python3 main.py "url" \
    --font "Hiragino Sans GB" --font-size 10;
```

## 命令行参数

- `url`: YouTube Short 视频的 URL（必需，除非使用 --skip-download）
- `--output-dir`, `-o`: 输出目录，默认: `./downloads`
- `--filename`, `-f`: 自定义输出文件名（不含扩展名）
- `--model`, `-m`: Whisper 模型大小，可选值: `tiny`, `base`, `small`, `medium`, `large`，默认: `base`
- `--font-size`: 字幕字体大小，默认: 24
- `--font`: 字幕字体，默认: `SimHei`
- `--skip-download`: 跳过下载步骤，直接处理本地视频
- `--video-path`: 本地视频文件路径（当使用 --skip-download 时必需）

## 项目结构

```
you-video1/
├── main.py               # 主脚本
├── pyproject.toml        # 项目配置和依赖
├── README.md             # 本说明文档
└── src/                  # 源代码目录
    ├── __init__.py       # 包初始化
    ├── downloader.py     # YouTube 视频下载模块
    ├── translator.py     # 音频提取和翻译模块
    └── compositor.py     # 视频合成模块
```

## 工作流程

1. **下载视频**：使用 yt-dlp 下载 YouTube Short 视频
2. **提取音频**：从视频中提取音频轨道
3. **语音识别**：使用 Whisper 模型识别英文语音
4. **翻译文本**：将英文文本翻译成中文
5. **生成字幕**：创建 SRT 格式的英文字幕和中文字幕
6. **视频合成**：将中文字幕添加到原始视频中

## 注意事项

1. **首次使用**：首次运行时，Whisper 会自动下载指定大小的模型文件，这可能需要一些时间
2. **处理时间**：视频处理时间取决于视频长度和选择的模型大小，较大的模型准确率更高但处理时间更长
3. **中文字体**：确保系统中安装了支持中文的字体，如 SimHei、Microsoft YaHei 等
4. **网络要求**：需要网络连接以下载视频和翻译服务
5. **存储空间**：处理过程中会生成临时文件，确保有足够的存储空间

## 依赖说明

- **yt-dlp**: 强大的视频下载工具
- **openai-whisper**: 用于语音识别的模型
- **deep-translator**: 提供翻译功能
- **moviepy**: 视频编辑和合成
- **pydub**: 音频处理
- **ffmpeg**: 底层音频视频处理（系统依赖）

## 常见问题

### 1. 下载失败

- 检查网络连接
- 确保 YouTube URL 正确且可访问
- 某些视频可能受版权保护无法下载

### 2. 语音识别不准确

- 尝试使用更大的模型（如 `--model medium` 或 `--model large`）
- 确保音频质量良好
- 对于口音较重的视频，识别准确率可能会降低

### 3. 字幕显示问题

- 确保系统中安装了中文字体
- 可以尝试更改字体设置（`--font` 参数）
- 调整字体大小以获得更好的显示效果

## 许可证

本项目采用 MIT 许可证。

## 免责声明

请遵守相关法律法规，仅用于合法用途。本工具仅供学习和个人使用，不得用于侵犯版权或其他违法行为。