import os, subprocess, json

exifToolBin = 'd:\\photomod\\exiftool(-k).exe'

from photomod2 import makeFileList

fileList = makeFileList('D:\\video')

for file in fileList:
    if str(file).endswith('.mp4') or str(file).endswith('.mts') or str(file).endswith('.mov'):

        print(exifToolBin +  ' -json ' + file)
        exifConsole = subprocess.run([exifToolBin, '-json', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(json.loads(exifConsole.stdout))
        exifOut = json.loads(exifConsole.stdout)

        exifDict = json.loads((str(exifOut).replace('[','').replace(']','').replace('\'','\"')))
        print(exifDict)

        print(file + ':' + exifDict['DateTimeOriginal'])
    else:
        continue
