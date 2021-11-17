#add saving hashes and filenames as dictionary, moving duplicate source files with copy of file to separate dir

import os, hashlib, send2trash, shutil, time

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

hashList = []
 
for  item in fullFileList:
    tempHash = (hashlib.md5(open(item, 'rb').read()).hexdigest())
    
    if tempHash in hashList:
        print('Duplicate detected! '+item)
        
        destFileDup = os.path.join('D:\\', 'photomod_source', 'duplicates' , os.path.basename(item))
        destFileDup.lower()
        shutil.copy(item, destFileDup)

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

#add logging to spearate files