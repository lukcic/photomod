#Python app that modify name and size of pictures taken by phone camera to fast and clear view on TV using DLNA. 
'''
TODO:
add paths as program argument sys.argv
add logs
add GUI and options
do not resize very small jpgs
'''

import os, hashlib, send2trash, shutil, time

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

def makeFileList(path):
    fileList = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            fileList.append(str(os.path.join(root, name)))
            print(os.path.join(root, name))
    return fileList

def renameAndCopy(fileList, folder):                                                                                                            #firsth argument is filelist and second is subfolder name where files will be copied with new names
    for file in fileList:       
        fileStats = os.stat(file)
        modificationTime = fileStats.st_mtime

        fileSize = str(os.path.getsize(file))                                                                                                   
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + '.' + file[-3:]  

        year = time.strftime('%Y', time.localtime(modificationTime))

        if not os.path.exists(os.path.join('D:\\', 'photomod_dest', year)):
            os.makedirs(os.path.join('D:\\', 'photomod_dest', year))

        destFile = os.path.join('d:\\', folder, year ,newFileName)       #creating new filename full path, that include subdirectory given as second argument
        print(os.path.basename(file) + ' renamed to: ' + '/' + folder + '/' + os.path.basename(destFile))
        shutil.copy(file, destFile)                                     #copying file with new name 
        os.utime(destFile, (modificationTime, modificationTime)) 

def rename(fileList, destPath):
    for file in fileList:                                                                                                                         #if statement = True, then leave this iteration and start next with new file
        fileSize = str(os.path.getsize(file))                                                                                                   #getsize() method return filesize in bytes 
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + '.' + file[-3:]      #creating new filename using modification time (windows) property and filesize
        fileStats = os.stat(file)
        modificationTime = fileStats.st_mtime
        year = time.strftime('%Y', time.localtime(modificationTime))
        #time.localtime() method is used to convert a time expressed in seconds (since the epoch) to a time.struct_time object in local time. 
        #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
        #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.
        destFile = os.path.join(destPath, year, newFileName)                                                                                       #creating new filename full path from cwd and filename
        print(os.path.basename(file) + ' renamed to: ' + os.path.basename(destFile))
        shutil.move(file, destFile)          

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

import copying_source

try:
    send2trash.send2trash("D:\\photomod_source\\duplicates")
except:
    print('No duplicates folder.')

fullSourceList = makeFileList("d:\\photomod_source")

if not os.path.exists('D:\\photomod_dest'):
    os.makedirs('D:\\photomod_dest')
renameAndCopy(fullSourceList, 'photomod_dest')

fullDestList = makeFileList('D:\\photomod_dest')
for file in fullDestList:                               #iterate subfolder and exclude directories (work only on files)
    if file.endswith('jpg'):
        resizeJPG(file, 0.5)                            #resizing copied files
    else:
        continue

rename(fullDestList, 'D:\\photomod_dest')
rename(fullSourceList, 'D:\\photomod_source')
