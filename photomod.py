"""
Python app that modify name and size of pictures taken by phone camera to fast and clear view on TV using DLNA. 
"""
#work only on files (not dirs, not .py): break, continue
#add path as program argument sys.argv
#resize files to given format ptyhon image library
#check for duplicates and delete them: md5
#error handling (duplicate files)?
#use regex to work only on .jpg files

import os
import re
import time
import shutil


#os.chdir('/home/debian/LearningProjects/Python/exercises')
os.chdir(os.getcwd())

if not os.path.exists('renamed'):
    os.makedirs('renamed')

fileList = os.listdir()                     #creating a listh that includes filenames

#regexJPG = re.compile(r'(\S+\.(jpg))')      #\S+ - matches any character without whites, one or more times, \.(jpg matches) '.jpg'  
                                            #creating regex object
#print(regexJPG.findall(str(fileList)))      #will search filenames list for regex of .jpg and returns tupples list of mathings (because regex use groups "()")

print('Full file list: ' + str(fileList))
regexJPG = re.compile(r'(\S+\.jpg)')
#fileList = list(regexJPG.findall(str(fileList)))     #findall() will return list of strings, because regex don't use groups "()" 
fileList = list(filter(regexJPG.match, fileList))

for file in fileList:
    fileSize = str(os.path.getsize(file))   #getsize() method return filesize in bytes 
    #print(file + str(time.strftime(' %Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10))
    newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + ".jpg"
    #time.localtime() method of Time module is used to convert a time expressed in seconds since the epoch to a time.struct_time object in local time. 
    #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
    #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.
    destFile = os.path.join(os.getcwd(), 'renamed', newFileName)
    print(destFile)
    shutil.copy(file, destFile)