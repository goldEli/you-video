import sys
import os

# 检查moviepy的完整结构
moviepy_path = '/Users/eli/Documents/github/you-video1/.venv/lib/python3.13/site-packages/moviepy'
print("MoviePy files:")
for root, dirs, files in os.walk(moviepy_path):
    for file in files:
        if file.endswith('.py'):
            print(os.path.join(root, file))

# 尝试不同的导入方式
try:
    # 尝试直接导入VideoFileClip
    from moviepy.video.io.VideoFileClip import VideoFileClip
    print("直接导入VideoFileClip成功")
except ImportError as e:
    print("直接导入VideoFileClip失败:", e)

# 检查是否存在editor.py文件
editor_path = os.path.join(moviepy_path, 'editor.py')
if os.path.exists(editor_path):
    print("editor.py存在")
else:
    print("editor.py不存在，尝试创建一个简单的editor模块")
    # 创建一个简单的editor.py文件
    with open(editor_path, 'w') as f:
        f.write('"""MoviePy Editor - 简单替代模块"""\n')
        f.write('from moviepy.video.io.VideoFileClip import VideoFileClip\n')
        f.write('from moviepy.video.VideoClip import TextClip, ColorClip\n')
        f.write('from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip\n')
        f.write('\n__all__ = [\"VideoFileClip\", \"TextClip\", \"CompositeVideoClip\", \"ColorClip\"]\n')
    print("已创建简易editor.py模块")