import sys
print("Python version:", sys.version)
print("sys.path:", sys.path)

try:
    import moviepy
    print("moviepy imported successfully")
    print("moviepy version:", getattr(moviepy, '__version__', 'unknown'))
    print("moviepy path:", getattr(moviepy, '__file__', 'unknown'))
    
    # Try import paths compatible with MoviePy v1 and v2
    try:
        from moviepy.editor import VideoFileClip
        print("moviepy.editor imported successfully (v1 style)")
    except ImportError:
        try:
            from moviepy.video.io.VideoFileClip import VideoFileClip
            print("moviepy.video.io.VideoFileClip imported successfully")
        except ImportError:
            from moviepy import VideoFileClip
            print("moviepy top-level VideoFileClip imported successfully")
except ImportError as e:
    print("Failed to import moviepy:", e)

try:
    import yt_dlp
    print("yt_dlp imported successfully")
except ImportError as e:
    print("Failed to import yt_dlp:", e)