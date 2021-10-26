#Python app that modify name and size of pictures taken by phone camera to fast and clear view on TV using DLNA. 
'''
TODO:
add path as program argument sys.argv
add walking on subfolders
add statiscics (log)
add or autoinstall send2trash and PIllow
add mp4 support regexJPG = re.compile(r'(\S+\.jpg)|(\S+\.mp4)')
add GUI and options
'''

import os, re, time, shutil, hashlib, send2trash
from PIL import Image                               #sudo pip3 install --upgrade Pillow


def resizeJPG(file, ratio):
    image = Image.open(file)                              #creating (opening) image object
    size = image.size                                     #get image size in pixels (return tuple)
    widthPX = size[0]
    heightPX = size[1]
    image = image.resize((int(widthPX / (1/ratio)), int(heightPX / (1/ratio))))
    image.save(file)
    print(os.path.basename(file) + ' resized from: ' + str(widthPX) + ' x ' + str(heightPX) + ' to: ' + str(image.size[0]) + ' x ' + str(image.size[1]))

def removeDuplicates(fileList):
    hashList = []                                           #creating empty list for file hash strings

    for file in fileList:
        if os.path.isdir(file):
            continue
                
        tempHash = (hashlib.md5(open(file, 'rb').read()).hexdigest())   #program is generating md5 checksum from file 
        print(file + ' : '+ str(tempHash))

        if tempHash in hashList:                                        #check if hashlist includes gerenated checksum, if yes, delete file (it's duplicate) 
            send2trash.send2trash(file)
            fileList.remove(file)
            print(str(hashList))
        else:
            hashList.append(tempHash)                                   #if not, add checksum to hashlist and work on file
            print(str(hashList))
    return fileList

def rename(fileList):
    for file in fileList:
        if os.path.isdir(file):
            continue        
        fileSize = str(os.path.getsize(file))                       #getsize() method return filesize in bytes 
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + ".jpg"      #creating new filename using modification time (windows) property and filesize
        #time.localtime() method is used to convert a time expressed in seconds (since the epoch) to a time.struct_time object in local time. 
        #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
        #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.
        destFile = os.path.join(os.getcwd(), newFileName)    #creating new filename full path, that include 'renamed' subdirectory
        print(os.path.basename(file) + ' renamed to: ' + os.path.basename(destFile))
        shutil.move(file, destFile)                                 #copying file with new name
    return fileList

def renameAndCopy(fileList, folder):
    for file in fileList:
        if os.path.isdir(file):
            continue        
        fileSize = str(os.path.getsize(file))                       #getsize() method return filesize in bytes 
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + ".jpg"      #creating new filename using modification time (windows) property and filesize
        #time.localtime() method is used to convert a time expressed in seconds (since the epoch) to a time.struct_time object in local time. 
        #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
        #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.
        destFile = os.path.join(os.getcwd(), folder, newFileName)    #creating new filename full path, that include 'renamed' subdirectory
        print(os.path.basename(file) + ' renamed to: ' + '/' + folder + '/' + os.path.basename(destFile))
        shutil.copy(file, destFile)                                 #copying file with new name
    return fileList

os.chdir(os.getcwd())                               #change work directory to current directowy

if not os.path.exists('renamed'):                   #check if 'renamed' directory exist, if not, create it
    os.makedirs('renamed')

fullFileList = os.listdir()                             #creating a listh that includes all filenames in pwd directory               
regexJPG = re.compile(r'(\S+\.jpg)')                    #creating regular expression object for filter only .jpg files, "if filename.endswith('.jpg'):"  may be used
jpgList = list(filter(regexJPG.match, fullFileList))    #filtering fileList using regex object
print('JPG list: ' + str(jpgList))
clearedJpgList = removeDuplicates(jpgList)                 #removing duplicates only from jpg files

renameAndCopy(clearedJpgList, 'renamed')                             #copying files with changed name

os.chdir('renamed')                         
for file in os.listdir():
    if os.path.isdir(file):
        continue
    else:
        resizeJPG(file, 0.5)                                #resizing copied files 
rename(os.listdir())    

os.chdir('..')
donorList = list(filter(regexJPG.match, os.listdir()))
rename(donorList)