# add saving hashes and filenames as dictionary, moving duplicate source files with copy of file to separate dir
import os, hashlib, send2trash, shutil, time

from PIL import Image
from PIL import ExifTags


def renameJPG(jpgFileFullPath):
    fileSize = str(os.path.getsize(jpgFileFullPath))
    newFileNameFromTime = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(jpgFileFullPath))))) + '_' + fileSize.zfill(10) + '.' + jpgFileFullPath[-3:]

    jpgObject = Image.open(jpgFileFullPath)
    jpg_exif = jpgObject._getexif()

    if jpg_exif is None:
        fullLog.write(f'Picture {os.path.basename(jpgFileFullPath)} don`t have EXIF data! \n')  # exif changed to time
        newFileNameFromExif = newFileNameFromTime
    elif 36868 not in jpg_exif.keys():
        fullLog.write(f'Picture {os.path.basename(jpgFileFullPath)} don`t have DateTime EXIF value! \n')  # exif changed to time
        newFileNameFromExif = newFileNameFromTime
    else:
        newFileNameFromExif = ((jpg_exif[
            36868]).replace(':', '').replace(' ', '_') + '_' + fileSize.zfill(10) + '.' + jpgFileFullPath[-3:])  # have exif

    jpgObject.close()

    destFileName = os.path.join(os.path.dirname(jpgFileFullPath), newFileNameFromExif)
    shutil.move(jpgFileFullPath, destFileName)
    fullLog.write(os.path.basename(jpgFileFullPath) + ' renamed to: ' + newFileNameFromExif + '\n')


fullLog = open(os.path.join(os.getcwd(), 'fulllog.txt'), 'a', encoding="utf-8")

print('Creating list of files to copy.')

fullFileList = []
for root, dirs, files in os.walk("\\\qnap\home\Foto Full Res\Różne", topdown=True):

    for name in files:
        if name.lower().endswith('jpg') or name.lower().endswith('mp4') or name.lower().endswith('mts') or name.lower().endswith('3gp'):
            fullFileList.append(str(os.path.join(root, name)))  # print(os.path.join(root, name))
        else:
            fullLog.write('Not a .jpg or .mp4! ' + name)
            continue

fullLog.write(' Full list of files to copy: \n')

for element in fullFileList:
    fullLog.write(element + '\n')

if not os.path.exists('D:\\photomod_source\\duplicates'):
    os.makedirs('D:\\photomod_source\\duplicates')
else:
    print('Duplicates directory exists! Exiting.')
    fullLog.write('Duplicates directory exists! Exiting.')
    exit

hashList = []
dupCount = 0

print('Checking for duplicates.')
fullLog.write('\n Checking for duplicates: \n')

for item in fullFileList:
    tempHash = (hashlib.md5(open(item, 'rb').read()).hexdigest())

    if tempHash in hashList:
        fullLog.write('Duplicate detected! ' + item + '\n')

        destFileDup = os.path.join('D:\\', 'photomod_source', 'duplicates', os.path.basename(item))
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

        destFile = os.path.join('D:\\', 'photomod_source', year, os.path.basename(item))
        destFile = destFile.lower()
        shutil.copy(item, destFile)
        os.utime(destFile, (modificationTime, modificationTime))

print(f'Duplicates found: {dupCount}')
fullLog.write(f'Duplicates found: {dupCount}')

try:
    send2trash.send2trash("D:\\photomod_source\\duplicates")
except:
    fullLog.write('No duplicates folder to delete. \n')

from photomod2 import makeFileList

photoSource = makeFileList('D:\\photomod_source')

print('Renaming files.')
fullLog.write(' \n Renaming files. \n')

for file in photoSource:
    if file.endswith('jpg'):
        renameJPG(file)
    else:
        continue

print('Finish.')
fullLog.close()
