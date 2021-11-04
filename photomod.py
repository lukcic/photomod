#Python app that modify name and size of pictures taken by phone camera to fast and clear view on TV using DLNA. 
'''
TODO:
add path as program argument sys.argv
add walking on subfolders
add statiscics (log)
add GUI and options
'''

import os, re, time, shutil, hashlib, subprocess, sys       #import standard python packages used in program

def install_package(package):                               #function that install packages not included to standard python libraries 
    import importlib                                        
    try:                                                    #try import package
        importlib.import_module(package)
    except ImportError:                                     #if failed, import pip and use it to install given package
        import pip
        pip.main(['install', package])


install_package('Pillow')
install_package('send2trash')
from PIL import Image  

def resizeJPG(file, ratio):
    image = Image.open(file)                                #creating (opening) image object
    
    fileStats = os.stat(file)                               #get file statistics and save it to 'stat_result' object
    modificationTime = fileStats.st_mtime                   #save modification time (in Windows thats picture real creation time) in variable to set it after resizing
    #print('Modification time: ' + time.strftime('%Y%m%d_%H%M%S', time.localtime(modificationTime)))

    size = image.size                                       #get image size in pixels (return tuple)
    widthPX = size[0]                                       #save width from tupple to variable
    heightPX = size[1]                                      #save height from tupple to variable
    image = image.resize((int(widthPX / (1/ratio)), int(heightPX / (1/ratio)))) #resize image object with given ratio (widht/2 == width/(1/0.5))
    image.save(file)                                        #save resized object to file
    os.utime(file, (modificationTime, modificationTime))    #update modification time from 'now' to old modification time (real image creation time in Win) from variable, os.utime(file, (acess_time, mod_time))
    print(os.path.basename(file) + ' resized from: ' + str(widthPX) + ' x ' + str(heightPX) + ' to: ' + str(image.size[0]) + ' x ' + str(image.size[1]))


def removeDuplicates(fileList):
    hashList = []                                           #creating empty list for file hash strings
    import send2trash  
    
    for file in fileList:
        if os.path.isdir(file):
            continue
                
        tempHash = (hashlib.md5(open(file, 'rb').read()).hexdigest())   #program is generating md5 checksum from file 
        print(file + ' : '+ str(tempHash))

        if tempHash in hashList:                #check if hashlist includes gerenated checksum, if yes, delete file (it's duplicate) 
            send2trash.send2trash(file)
            fileList.remove(file)
            print(str(hashList))
        else:
            hashList.append(tempHash)                                   #if not, add checksum to hashlist and work on file
            print(str(hashList))
    return fileList

def rename(fileList):
    for file in fileList:
        if os.path.isdir(file):                                                                                                                 #exclude directories from renaming (just files)
            continue                                                                                                                            #if statement = True, then leave this iteration and start next with new file
        fileSize = str(os.path.getsize(file))                                                                                                   #getsize() method return filesize in bytes 
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + ".jpg"      #creating new filename using modification time (windows) property and filesize
        #time.localtime() method is used to convert a time expressed in seconds (since the epoch) to a time.struct_time object in local time. 
        #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
        #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.
        destFile = os.path.join(os.getcwd(), newFileName)                                                                                       #creating new filename full path from cwd and filename
        print(os.path.basename(file) + ' renamed to: ' + os.path.basename(destFile))
        shutil.move(file, destFile)                                                                                                             #renaming file with new name
 
def renameAndCopy(fileList, folder):                                                                                                            #firsth argument is filelist and second is subfolder name where files will be copied with new names
    for file in fileList:
        if os.path.isdir(file):
            continue
        
        fileStats = os.stat(file)
        modificationTime = fileStats.st_mtime
        #print(time.strftime('%Y%m%d_%H%M%S', time.localtime(modificationTime)))

        fileSize = str(os.path.getsize(file))                                                                                                   
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + ".jpg"      
        destFile = os.path.join(os.getcwd(), folder, newFileName)       #creating new filename full path, that include subdirectory given as second argument
        print(os.path.basename(file) + ' renamed to: ' + '/' + folder + '/' + os.path.basename(destFile))
        shutil.copy(file, destFile)                                     #copying file with new name 
        os.utime(destFile, (modificationTime, modificationTime))        

os.chdir(os.getcwd())                                   #change work directory to current directowy

if not os.path.exists('renamed'):                       #check if 'renamed' directory exist, if not, create it
    os.makedirs('renamed')

fullFileList = os.listdir()                             #creating a listh that includes all filenames in cwd directory               
regexJPG = re.compile(r'(\S+\.jpg)')                    #creating regular expression object for filter only .jpg files, "if filename.endswith('.jpg'):"  may be used
jpgList = list(filter(regexJPG.match, fullFileList))    #filtering fileList using regex object, creating list of jpg files only
print('JPG list: ' + str(jpgList))
clearedJpgList = removeDuplicates(jpgList)              #removing duplicates only from jpg files

renameAndCopy(clearedJpgList, 'renamed')                #copying files with changed name, to 'rename' subfolder

os.chdir('renamed')                         
for file in os.listdir():                               #iterate subfolder and exclude directories (work only on files)
    if os.path.isdir(file):
        continue
    else:
        resizeJPG(file, 0.5)                            #resizing copied files
rename(os.listdir())                                    #rename files after changing its size

os.chdir('..')
donorList = list(filter(regexJPG.match, os.listdir()))  #create list of jpg files that were copied
rename(donorList)                                       #rename source files with pattern