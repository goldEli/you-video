import sys
print("Python version:", sys.version)
print("sys.path:", sys.path)

try:
    import moviepy
    print("moviepy imported successfully")
    print("moviepy version:", getattr(moviepy, '__version__', 'unknown'))
    print("moviepy path:", getattr(moviepy, '__file__', 'unknown'))
    
    try:
        from moviepy.editor import VideoFileClip
        print("moviepy.editor imported successfully")
    except ImportError as e:
        print("Failed to import moviepy.editor:", e)
except ImportError as e:
    print("Failed to import moviepy:", e)

try:
    import yt_dlp
    print("yt_dlp imported successfully")
except ImportError as e:
    print("Failed to import yt_dlp:", e)