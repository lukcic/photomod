#add saving hashes and filenames as dictionary, moving duplicate source files with copy of file to separate dir
import os, hashlib, send2trash, shutil, time

from PIL import Image
from PIL import ExifTags

def renameJPG(jpgFileFullPath):

    fileSize = str(os.path.getsize(jpgFileFullPath)) 
    newFileNameFromTime = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(jpgFileFullPath))))) + '_' + fileSize.zfill(10) + '.' + jpgFileFullPath[-3:]
    
    
    jpgObject = Image.open(jpgFileFullPath)
    jpg_exif = jpgObject._getexif()

    if jpg_exif is None:
        print(f'Picture {os.path.basename(jpgFileFullPath)} don`t have EXIF data!')  #exif changed to time
        newFileNameFromExif = newFileNameFromTime            
    elif 36868 not in jpg_exif.keys(): 
        print(f'Picture {os.path.basename(jpgFileFullPath)} don`t have DateTime EXIF value!')  #exif changed to time     
        newFileNameFromExif = newFileNameFromTime
    else:
        newFileNameFromExif = ((jpg_exif[36868]).replace(':','').replace(' ','_') + '_' + fileSize.zfill(10) + '.' + jpgFileFullPath[-3:])  #have exif

    jpgObject.close()

    destFileName = os.path.join(os.path.dirname(jpgFileFullPath) , newFileNameFromExif)
    shutil.move(jpgFileFullPath, destFileName)
    print(os.path.basename(jpgFileFullPath) + ' renamed to: ' + newFileNameFromExif)
       

fullFileList = []
for root, dirs, files in os.walk("\\\qnap\home\Foto Full Res\Różne", topdown=True):

    for name in files:
        if name.lower().endswith('jpg') or \
        name.lower().endswith('mp4') or \
        name.lower().endswith('mts') or \
        name.lower().endswith('3gp'):
            fullFileList.append(str(os.path.join(root, name)))
            print(os.path.join(root, name))
        else:
            print('Not a .jpg or .mp4! ' + name)
            continue
print(fullFileList)

if not os.path.exists('D:\\photomod_source\\duplicates'):
    os.makedirs('D:\\photomod_source\\duplicates')
else:
    print('Destination directory exists! Exiting.')
    exit

hashList = []
dupCount = 0
 
for  item in fullFileList:
    tempHash = (hashlib.md5(open(item, 'rb').read()).hexdigest())
    
    if tempHash in hashList:
        print('Duplicate detected! '+item)
        
        destFileDup = os.path.join('D:\\', 'photomod_source', 'duplicates' , os.path.basename(item))
        destFileDup.lower()
        shutil.copy(item, destFileDup)
        dupCount = dupCount + 1

    else:
        hashList.append(tempHash)

        fileStats = os.stat(item)
        modificationTime = fileStats.st_mtime
        year = time.strftime('%Y', time.localtime(modificationTime))

        if not os.path.exists(os.path.join('D:\\', 'photomod_source', year)):
            os.makedirs(os.path.join('D:\\', 'photomod_source', year))

        destFile = os.path.join('D:\\', 'photomod_source', year , os.path.basename(item))
        destFile = destFile.lower()
        shutil.copy(item, destFile)
        os.utime(destFile, (modificationTime, modificationTime))

try:
    send2trash.send2trash("D:\\photomod_source\\duplicates")
except:
    print('No duplicates folder.')

from photomod2 import makeFileList

photoSource = makeFileList('D:\\photomod_source')

for file in photoSource:
    if file.endswith('jpg'):
        renameJPG(file)
    else:
        continue

print(f'Duplicates found: {dupCount}')
