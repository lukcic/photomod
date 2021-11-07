import subprocess, sys, os, time, shutil

'''
Codec to use for image encoding. Can be any codec supported
by ffmpeg. 
https://en.wikipedia.org/wiki/FFmpeg#Supported_codecs_and_formats

If the filename is has extension '.mp4', '.ogv', '.webm',
the codec will be set accordingly, but you can still set it if you
don't like the default. For other extensions, the output filename
must be set accordingly.

Some examples of codecs are:

``'libx264'`` (default codec for file extension ``.mp4``)
makes well-compressed videos (quality tunable using 'bitrate').

``'mpeg4'`` (other codec for extension ``.mp4``) can be an alternative
to ``'libx264'``, and produces higher quality videos by default.

``'rawvideo'`` (use file extension ``.avi``) will produce
a video of perfect quality, of possibly very huge size.

``png`` (use file extension ``.avi``) will produce a video
of perfect quality, of smaller size than with ``rawvideo``.

``'libvorbis'`` (use file extension ``.ogv``) is a nice video
format, which is completely free/ open source. However not
everyone has the codecs installed by default on their machine.

``'libvpx'`` (use file extension ``.webm``) is tiny a video
format well indicated for web videos (with HTML5). Open source.

https://zulko.github.io/moviepy/_modules/moviepy/video/VideoClip.html
final_render.write_videofile('./videos/output_video.mp4', fps = 30, threads = 1, codec = "libx264")

rotate left:
C:\Users\lukcic\Desktop\ffmpeg-2021-11-03-git-08a501946f-full_build\bin\ffmpeg.exe  -i output4.mp4 -vf "transpose=2" output44.mp4
0=90CounterCLockwise and Vertical Flip  (default) 
1=90Clockwise 
2=90CounterClockwise 
3=90Clockwise and Vertical Flip


MTS:
C:\Users\lukcic\Desktop\ffmpeg-2021-11-03-git-08a501946f-full_build\bin\ffmpeg.exe -i 20130608_185224_167018496.MTS -vf scale=1920:1080 -preset slow -crf 18 output3.mp4
'''

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

def resizeVideo(srcFile, size, outFile):                #the output hight size in px
    if os.path.exists(str(srcFile)):
        clip = moviepy.editor.VideoFileClip(srcFile)
        clip_resized = clip.resize(height=size)         #make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
        clip_resized.write_videofile(outFile)           #clip_resized = clip.resize(newsize=(my_width,my_height))
    else:
        print('Incorrect file path!')

def rotateVideo(file, angle, output):                   #angle as int
    if os.path.exists(str(file)):
        clip = moviepy.editor.VideoFileClip(file)                     
        clip_resized = clip.rotate(angle)
        clip_resized.write_videofile(output)           
    else:
        print('Incorrect file path!')

def rename(fileList):
    for file in fileList:
        if os.path.isdir(file):                                                                                                                
            continue                                                                                                                            
        fileSize = str(os.path.getsize(file))

        newFileName = str(time.strftime('%Y%m%d_%H%M%S', 
        time.localtime(int(os.path.getmtime(file))))) + '_' \
        + fileSize.zfill(10) + '.' + file[-3:]                      #file[-3:] returns 3 last letters of filename (extension)

        destFile = os.path.join(os.getcwd(), newFileName)                                                                                     
        print(os.path.basename(file) + ' renamed to: ' + os.path.basename(destFile))
        shutil.move(file, destFile)  

moviesList = []

for file in os.listdir(os.getcwd()):
    if str(file).endswith('mp4'):
        moviesList.append(str(file))
    else:
        continue

if not os.path.exists('resized'):
    os.makedirs('resized')

print(moviesList)

for file in list(moviesList):
    resizeVideo(file, 720, str('resized/' + 'resized_' + file ))

os.chdir('resized')

moviesResizedList = []
for file in os.listdir(os.getcwd()):
    moviesResizedList.append(file)

print(moviesResizedList)    
rename(moviesResizedList)