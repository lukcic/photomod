import subprocess, sys, os, time, shutil

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