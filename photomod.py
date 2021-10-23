#Python app that modify name and size of pictures taken by phone camera to fast and clear view on TV using DLNA. 
'''
TODO:
add path as program argument sys.argv
resize files to given format ptyhon image library
add walking on subfolders
add statiscics (log)
add or autoinstall send2trash
add mp4 support regexJPG = re.compile(r'(\S+\.jpg)|(\S+\.mp4)')
add GUI and options
'''

import os, re, time, shutil, hashlib, send2trash
from PIL import Image                               #sudo pip3 install --upgrade Pillow

os.chdir(os.getcwd())                               #change work directory to current directowy

if not os.path.exists('renamed'):                   #check if 'renamed' directory exist, if not, create it
    os.makedirs('renamed')

fileList = os.listdir()                             #creating a listh that includes filenames
print('Full file list: ' + str(fileList))

regexJPG = re.compile(r'(\S+\.jpg)')                #creating regular expression object, "if filename.endswith('.jpg'):"  may be used

fileList = list(filter(regexJPG.match, fileList))   #filtering fileList using regex object
hashList = []                                       #creating empty list for file hash strings

for file in fileList:
    tempHash = (hashlib.md5(open(file, 'rb').read()).hexdigest())   #program is generating md5 checksum from file
    
    if tempHash in hashList:                                        #check if hashlist includes gerenated checksum, if yes, delete file (it's duplicate) 
        send2trash.send2trash(file)
    else:
        hashList.append(tempHash)                                   #if not, add checksum to hashlist and work on file

        fileSize = str(os.path.getsize(file))                       #getsize() method return filesize in bytes 
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getctime(file))))) + '_' + fileSize.zfill(10) + ".jpg"      #creating new filename using modification time (windows) property and filesize
        #time.localtime() method is used to convert a time expressed in seconds (since the epoch) to a time.struct_time object in local time. 
        #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
        #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.
        destFile = os.path.join(os.getcwd(), 'renamed', newFileName)    #creating new filename full path, that include 'renamed' subdirectory
        print(destFile)
        shutil.copy(file, destFile)                                 #copying file with new name                         

        image = Image.open(destFile)                                    #creating (opening) image object
        size = image.size                                     #get image size in pixels (return tuple)
        widthPX = size[0]
        heightPX = size[1]
        print(widthPX, heightPX)

        image = image.resize((int(widthPX / 2), int(heightPX / 2)))
        image.save(destFile)

print(hashList)

