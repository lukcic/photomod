# TODO:
'''
Photomod project:
1. Get files from sourcePath, remove duplicates, copy them to fullSizePath and resizedPath divided by year.
2. Resize pictures in resizedPath.

tych plików i podział na lata. Rename po Exif, potem po ModTime.
4. Resize obrazów:
 - określ czy pion czy poziom
 - jeżeli mniejsze od 1080 to nic nie rob, jezeli wieksze to zmniejsz do 1080
5. Resize filmów:
 - określ czy pion czy poziom
 - jeżlei mniejsze niż 720 to nic nie rob, jeżeli większe to resize
6. Rename całości z zachowaniem ModTime.
7. Policzyć ile źródłowych, porównać z duplikatami i wynikiem końcowym.
8. Póżij funkcja do obracania na podstawie nazwy. 

'''
#Problems:
# -resizing deletes EXIF data
# -resizing rotates some pictures 
# CREATE TESTS!

import os, hashlib, shutil, time, subprocess

packages = ['send2trash', 'Image', 'Pillow']                # creating list of needed packages to install

for package in packages:                                    # installing modules from list
    depInstaller = subprocess.run(['python', '-m', 'pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(depInstaller.stderr)                              # Print erros if occours

from PIL import Image
from PIL import ExifTags
import send2trash

# Paths definitions
sourcePath = '/source_files'
duplPath = str(os.path.join(os.getcwd(), 'duplicates'))
fullSizePath = str(os.path.join(os.getcwd(), 'fullSize'))
resizedPath = str(os.path.join(os.getcwd(), 'resized'))

# Settings
moveSource = False  # If false then copy files
deleteDuplicates = True
picturesEXT = ['jpg','jpeg']
videosEXT = ['mp4','mts','3gp']
jpgRatio = 0.5

# Functions





def resizeJPG(file, ratio):
    image = Image.open(file)                                #creating (opening) image object
    
    try:
        exif = image.info['exif']                                       #save resized object to file
    except Exception:
        fullLog.write(f'Problem with EXIF of file {file}. \n') 

    fileStats = os.stat(file)                               #get file statistics and save it to 'stat_result' object
    modificationTime = fileStats.st_mtime                   #save modification time (in Windows thats picture real creation time) in variable to set it after resizing
    #print('Modification time: ' + time.strftime('%Y%m%d_%H%M%S', time.localtime(modificationTime)))
    
    size = image.size                                       #get image size in pixels (return tuple)
    widthPX = size[0]                                       #save width from tupple to variable
    heightPX = size[1]                                      #save height from tupple to variable
    image = image.resize((int(widthPX / (1/ratio)), int(heightPX / (1/ratio)))) #resize image object with given ratio (widht/2 == width/(1/0.5))
    
    try:
        image.save(file, exif=exif)                                        #save resized object to file
    except Exception:
        fullLog.write(f'Problem with EXIF of file {file}. \n')
    finally:
        image.save(file) 
    
    os.utime(file, (modificationTime, modificationTime))    #update modification time from 'now' to old modification time (real image creation time in Win) from variable, os.utime(file, (acess_time, mod_time))
    
    fullLog.write(os.path.basename(file) + ' resized from: ' + str(widthPX) + ' x ' + str(heightPX) + ' to: ' + str(image.size[0]) + ' x ' + str(image.size[1]) + '\n')

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



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# App will copy/move files from sourcePath to fullSizePath. Removes duplicates (forst moves them to separated directory)

fullLog = open(os.path.join(os.getcwd(), 'fulllog.txt'), 'a', encoding="utf-8")
print('Creating list of files to copy.')

# Creating list of needed files, creating log.
fullFileList = []
for root, dirs, files in os.walk(sourcePath, topdown=True):

    for name in files:
        if name.lower().endswith(tuple(picturesEXT)) or name.lower().endswith(tuple(videosEXT)):
            fullFileList.append(str(os.path.join(root, name)))  # print(os.path.join(root, name))
        else:
            fullLog.write('Different filetype! ' + name)
            continue

fullLog.write('Full list of files to copy: \n')
for element in fullFileList:
    fullLog.write(element + '\n')

if not os.path.exists(duplPath):
    os.makedirs(duplPath)

hashList = []
dupCount = 0

print('Checking for duplicates.')
fullLog.write('\n Checking for duplicates: \n')

for item in fullFileList:
    tempHash = (hashlib.md5(open(item, 'rb').read()).hexdigest())

    if tempHash in hashList:
        fullLog.write('Duplicate detected! ' + item + '\n')
        destFileDup = os.path.join(duplPath, os.path.basename(item))
        destFileDup.lower()
        
        if moveSource == True:
            shutil.move(item, destFileDup)
        else: 
            shutil.copy(item, destFileDup)       
        dupCount = dupCount + 1

    else:
        hashList.append(tempHash)

        fileStats = os.stat(item)
        modificationTime = fileStats.st_mtime
        year = time.strftime('%Y', time.localtime(modificationTime))

        if not os.path.exists(os.path.join(fullSizePath, year)):
            os.makedirs(os.path.join(fullSizePath, year))
        if not os.path.exists(os.path.join(resizedPath, year)):
            os.makedirs(os.path.join(resizedPath, year))

        destFileFull = os.path.join(fullSizePath, year, os.path.basename(item))
        destFileFull = destFileFull.lower()
        destFileRes = os.path.join(resizedPath, year, os.path.basename(item))
        destFileRes = destFileRes.lower()

        if moveSource == True:
            shutil.move(item, destFileFull)
            shutil.move(item, destFileRes)
        else: 
            shutil.copy(item, destFileFull)
            shutil.copy(item, destFileRes)
        os.utime(destFileFull, (modificationTime, modificationTime))
        os.utime(destFileRes, (modificationTime, modificationTime))

        if destFileRes.endswith(tuple(picturesEXT)):
            resizeJPG(destFileRes, jpgRatio)
        else:
            continue

print(f'Duplicates found: {dupCount}')
fullLog.write(f'Duplicates found: {dupCount}')

if deleteDuplicates == True:
    try:
        send2trash.send2trash(duplPath)
    except:
        fullLog.write('No duplicates folder to delete. \n')

print('Finish.')
fullLog.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 