import subprocess
import sys

def install_package(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
#    finally:
#        globals()[moviepy] = importlib.import_module(moviepy)


install_package('moviepy')

import moviepy.editor 

clip = moviepy.editor.VideoFileClip("VID_20211016_091124.mp4")
clip_resized = clip.resize(height=720)                      # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
clip_resized = clip.rotate(90)
clip_resized.write_videofile("movie_resized.mp4")           #clip_resized = clip.resize(newsize=(my_width,my_height))


