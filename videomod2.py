import subprocess, os

def makeFileList(path):
    fileList = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            fileList.append(str(os.path.join(root, name)))
            print(os.path.join(root, name))
    return fileList

files = makeFileList(os.getcwd())

#MTS Support

ffmpegBin = 'C:\\Users\\lukcic\\Desktop\\ffmpeg-2021-11-03-git-08a501946f-full_build\\bin\\ffmpeg.exe'
scale = 'scale=1280x720'
crfValue = '18'

for file in files:
    if str(file).endswith('.MTS'):
        outputFile = 'decoded_' + os.path.basename(file.replace('MTS','mp4')) 
        consoleOut = subprocess.run([ffmpegBin, '-i', file, '-vf', scale, '-preset', 'slow','-crf', crfValue, outputFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(consoleOut.stdout, consoleOut.stderr)
    else:
        continue

