"""
Python app that modify name and size of pictures taken by phone camera to fast and clear view on TV using DLNA. 
"""

import os
import time

os.chdir('/home/debian/LearningProjects/Python/exercises')
#os.chdir('D:\\photo')

fileList = os.listdir()     #creating a listh that includes filenames

for file in fileList:
    fileSize = str(os.path.getsize(file))   #getsize() method return filesize in bytes 
    print(file + str(time.strftime(' %Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10))
    #time.localtime() method of Time module is used to convert a time expressed in seconds since the epoch to a time.struct_time object in local time. 
    #strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
    #zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.