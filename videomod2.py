import subprocess, os

ffmpegBin = 'C:\\Users\\lukcic\\Desktop\\ffmpeg-2021-11-03-git-08a501946f-full_build\\bin\\ffmpeg.exe'
ffprobeBin = 'C:\\Users\\lukcic\\Desktop\\ffmpeg-2021-11-03-git-08a501946f-full_build\\bin\\ffprobe.exe' 
crfValue = '18'

def makeFileList(path):
    fileList = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            fileList.append(str(os.path.join(root, name)))
            print(os.path.join(root, name))
    return fileList

def getInputScale(file):
    subObj1 = subprocess.run([ffprobeBin, '-v', 'error', '-select_streams', 'v:0' ,'-show_entries', 'stream=width', '-of', 'default=nw=1:nk=1', file],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subObj2 = subprocess.run([ffprobeBin, '-v', 'error', '-select_streams', 'v:0' ,'-show_entries', 'stream=height', '-of', 'default=nw=1:nk=1', file],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    width = int(str(subObj1.stdout).partition('\n')[0])             #partition command cuts string into separate lines using '\n'
    height = int(str(subObj2.stdout).partition('\n')[0])            #needed for mts files which have multiple streams 

    return(width, height)

def resize(inputFile, width, height, outputFile):
    scale=str('scale=' + width + 'x' + height)
    consoleOut = subprocess.run([ffmpegBin, '-i', inputFile, '-vf', scale, '-preset', 'slow','-crf', crfValue, outputFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(consoleOut.stdout, consoleOut.stderr)

files = makeFileList(os.getcwd())

if not os.path.exists('resized'):
    os.makedirs('resized')

#MTS Support
for file in files:
    if str(file).endswith('.MTS'):
        outputFile = os.path.join('resized', str(os.path.basename(file.replace('MTS','mp4'))))
        width = str(int(getInputScale(file)[0]/2))
        height = str(int(getInputScale(file)[1]/2))
        resize(file, width, height, outputFile)   
    else:
        continue

#for files that are video
#create 3 options:
#1. Files horizontal 
#2. Files vertical
#3. Files to rotate
