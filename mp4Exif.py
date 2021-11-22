import os, subprocess, json

exifToolBin = 'd:\\photomod\\exiftool(-k).exe'

file = 'd:\\video\\20130608_185224_167018496.MTS'

exifConsole = subprocess.run([exifToolBin, '-json', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
exifOut = json.loads(exifConsole.stdout)

exifDict = json.loads((str(exifOut).replace('[','').replace(']','').replace('\'','\"')))
print(exifDict)
print(type(exifDict))

print(exifDict['DateTimeOriginal'])