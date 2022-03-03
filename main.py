# This application copy pictures and movies created using digital camera or smartphone into 2 directories.
# Firsth directory includes full sizes copies renamed for create historical timeline archive (duplicates are removed).
# Second copy includes resized pics and movies (converted to mp4) for fast viewing on TV etc. using DLNA.
# Timeline is divided by each year folder.


import os, hashlib, shutil, time, subprocess

packages = ['send2trash', 'Image', 'Pillow']                # creating list of needed packages to install

for package in packages:                                    # installing modules from list
    depInstaller = subprocess.run(['python', '-m', 'pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(depInstaller.stderr)                              # Print erros if occours

from PIL import Image
from PIL import ExifTags
import send2trash

ffmpegBin = 'C:\\Users\\lukcic\\Desktop\\ffmpeg-2021-11-03-git-08a501946f-full_build\\bin\\ffmpeg.exe'
ffprobeBin = 'C:\\Users\\lukcic\\Desktop\\ffmpeg-2021-11-03-git-08a501946f-full_build\\bin\\ffprobe.exe'
crfValue = '18'


# - - - - - - - - - - - - - - Function definition - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def makeFileList(path):  # Function will save all full-path filenames from given path as a list
    fileList = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            fileList.append(str(os.path.join(root, name)))  # print(os.path.join(root, name))
    return fileList


def renameJPG(jpgFileFullPath):
    fileSize = str(os.path.getsize(jpgFileFullPath))  # getting size of JPG
    newFileNameFromTime = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(jpgFileFullPath))))) + '_' + fileSize.zfill(10) + '.' + jpgFileFullPath[-3:]
    # creating new filename using modification time, get file modification time, convert it to date format and format as needed string, add size in bytes and extension

    jpgObject = Image.open(jpgFileFullPath)  # open JPG and store it in variable
    jpg_exif = jpgObject._getexif()  # get JPGs exif data and store it as variable

    if jpg_exif is None:
        fullLog.write(f'Picture {os.path.basename(jpgFileFullPath)} don`t have EXIF data! \n')  # write info to log file
        newFileNameFromExif = newFileNameFromTime  # exif filename changed to time, because file don`t have exif data
    elif 36868 not in jpg_exif.keys():  # if exif`s DateTime value is not present, use time filemane
        fullLog.write(f'Picture {os.path.basename(jpgFileFullPath)} don`t have DateTime EXIF value! \n')
        newFileNameFromExif = newFileNameFromTime
    else:
        newFileNameFromExif = ((jpg_exif[
            36868]).replace(':', '').replace(' ', '_') + '_' + fileSize.zfill(10) + '.' + jpgFileFullPath[-3:])  # have exif, create filename from exif`s DateTime value

    jpgObject.close()  # close JPG object

    destFileName = os.path.join(os.path.dirname(jpgFileFullPath), newFileNameFromExif)  # create full filename (with path)
    shutil.move(jpgFileFullPath, destFileName)  # rename file
    fullLog.write(os.path.basename(jpgFileFullPath) + ' renamed to: ' + newFileNameFromExif + '\n')  # write log entry


def renameAndCopy(fileList, folder):  # firsth argument is filelist and second is subfolder name where files will be copied with new names
    for file in fileList:
        fileStats = os.stat(file)
        modificationTime = fileStats.st_mtime

        fileSize = str(os.path.getsize(file))
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + '.' + file[-3:]

        year = time.strftime('%Y', time.localtime(modificationTime))

        if not os.path.exists(os.path.join('D:\\', 'photomod_dest', year)):
            os.makedirs(os.path.join('D:\\', 'photomod_dest', year))

        destFile = os.path.join('d:\\', folder, year, newFileName)  # creating new filename full path, that include subdirectory given as second argument
        fullLog.write(os.path.basename(file) + ' renamed to: ' + '/' + folder + '/' + os.path.basename(destFile) + '\n')
        shutil.copy(file, destFile)  # copying file with new name
        os.utime(destFile, (modificationTime, modificationTime))


def rename(fileList, destPath):
    for file in fileList:  # if statement = True, then leave this iteration and start next with new file
        fileSize = str(os.path.getsize(file))  # getsize() method return filesize in bytes
        newFileName = str(time.strftime('%Y%m%d_%H%M%S', time.localtime(int(os.path.getmtime(file))))) + '_' + fileSize.zfill(10) + '.' + file[-3:]  # creating new filename using modification time (windows) property and filesize
        fileStats = os.stat(file)
        modificationTime = fileStats.st_mtime
        year = time.strftime('%Y', time.localtime(modificationTime))
        # time.localtime() method is used to convert a time expressed in seconds (since the epoch) to a time.struct_time object in local time.
        # strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.
        # zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length.

        if not os.path.exists(os.path.join(destPath, year)):
            os.makedirs(os.path.join(destPath, year))

        destFile = os.path.join(destPath, year, newFileName)  # creating new filename full path from cwd and filename
        fullLog.write(os.path.basename(file) + ' renamed to: ' + os.path.basename(destFile) + '\n')
        shutil.move(file, destFile)


def resizeJPG(file, ratio):
    image = Image.open(file)  # creating (opening) image object

    fileStats = os.stat(file)  # get file statistics and save it to 'stat_result' object
    modificationTime = fileStats.st_mtime  # save modification time (in Windows thats picture real creation time) in variable to set it after resizing
    # print('Modification time: ' + time.strftime('%Y%m%d_%H%M%S', time.localtime(modificationTime)))

    size = image.size  # get image size in pixels (return tuple)
    widthPX = size[0]  # save width from tupple to variable
    heightPX = size[1]  # save height from tupple to variable
    image = image.resize((int(widthPX / (1 / ratio)), int(heightPX / (1 / ratio))))  # resize image object with given ratio (widht/2 == width/(1/0.5))
    image.save(file)  # save resized object to file
    os.utime(file, (modificationTime, modificationTime))  # update modification time from 'now' to old modification time (real image creation time in Win) from variable, os.utime(file, (acess_time, mod_time))
    fullLog.write(os.path.basename(file) + ' resized from: ' + str(widthPX) + ' x ' + str(heightPX) + ' to: ' + str(image.size[0]) + ' x ' + str(image.size[1]) + '\n')


def getInputScale(file):
    subObj1 = subprocess.run([ffprobeBin, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width','-of', 'default=nw=1:nk=1', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subObj2 = subprocess.run([ffprobeBin, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=height','-of', 'default=nw=1:nk=1', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    width = int(str(subObj1.stdout).partition('\n')[0])  # partition command cuts string into separate lines using '\n'
    height = int(str(subObj2.stdout).partition('\n')[0])  # needed for mts files which have multiple streams

    return (width, height)


def resizeVID(inputFile, width, height, outputFile):
    fileStats = os.stat(inputFile)
    modificationTime = fileStats.st_mtime
    
    tempFile = os.path.join(os.getcwd(),os.path.basename(outputFile))
    scale = str('scale=' + width + 'x' + height)
    consoleOut = subprocess.run([ffmpegBin, '-i', inputFile, '-vf', scale, '-preset', 'slow', '-crf', crfValue, tempFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #fullLog.write(consoleOut.stderr)
    send2trash.send2trash(inputFile)
    shutil.move(tempFile, outputFile)
    os.utime(outputFile, (modificationTime, modificationTime))
  

def setNewScale(width: int, height: int):
    if width > height:
        #horizontal file
        if height >= 1080:
            newWidth = 1280
            newHeight = 720
        else:
            newWidth = width
            newHeight = height
    else:
        #vertical file
        if width >= 1080:
            newWidth = 720
            newHeight = 1280
        else:
            newWidth = width
            newHeight = height

    return(newWidth, newHeight)


# - - - - - - - - - - - - - - Copying source - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":

    if os.path.exists(os.path.join(os.getcwd(), 'fulllog.txt')):  # delete old logfile
        send2trash.send2trash('fulllog.txt')

    fullLog = open(os.path.join(os.getcwd(), 'fulllog.txt'), 'a', encoding="utf-8")  # create logfile

    print('Creating list of files to copy.')

    fullFileList = []
    for root, dirs, files in os.walk("\\\qnap\\home\\-=TEMP=-\\Pieseł", topdown=True):

        for name in files:
            name.lower()
            if name.endswith('jpg') or name.endswith('mp4') or name.endswith('mts') or name.endswith('3gp') or name.endswith('jpeg'):
                fullFileList.append(str(os.path.join(root, name)))
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

    photoSource = makeFileList('D:\\photomod_source')

    print('Renaming source files.')
    fullLog.write(' \n Renaming source files. \n')

    videoList = []
    
    for file in photoSource:
        file.lower()
        if file.endswith('jpg'):
            renameJPG(file)
        elif file.endswith('jpeg'):
            newJPEGName = file.replace('jpeg','jpg')
            shutil.move(name, newJPEGName)
            renameJPG(newJPEGName)
        else:
            videoList.append(file)

    rename(videoList, 'D:\\photomod_source')

    # - - - - - - - - - - - - - - Photomod - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    fullSourceList = makeFileList("d:\\photomod_source")

    if not os.path.exists('D:\\photomod_dest'):
        os.makedirs('D:\\photomod_dest')

    print('Copy renamed files to destination directory.')
    fullLog.write(' \n Copy renamed files to destination directory. \n')
    renameAndCopy(fullSourceList, 'photomod_dest')

    print('Resizing destination files')
    fullLog.write(' \n Resizing destination files \n')
    fullDestList = makeFileList('D:\\photomod_dest')

    for file in fullDestList:  # resizing copied files
        file.lower()

        if str(file).endswith('jpg'):
            resizeJPG(file, 0.5)

        else:
            if str(file).endswith('.mts'):
                outputFile = file.replace('mts', 'mp4')

            elif str(file).endswith('.mp4'):
                outputFile = file

            elif str(file).endswith('.mov'):
                outputFile = file.replace('mov', 'mp4')

            elif str(file).endswith('.3gp'):
                outputFile = file.replace('3gp', 'mp4')

            else:
                continue


            if getInputScale(file)[0] < 720 and getInputScale(file)[1] < 720:
                continue
            elif getInputScale(file)[0] == 720 and getInputScale(file)[1] == 1280:
                continue
            elif getInputScale(file)[0] == 1280 and getInputScale(file)[1] == 720:
                continue
            else:
                newScale = setNewScale(int(getInputScale(file)[0]), int(getInputScale(file)[1]))
                fullLog.write(f'Resize {file} from {getInputScale(file)[0]}x{getInputScale(file)[1]} to {newScale[0]}x{newScale[1]}. \n')
                resizeVID(file, str(newScale[0]), str(newScale[1]), outputFile)

    fullDestList = makeFileList('D:\\photomod_dest')
    rename(fullDestList, 'D:\\photomod_dest')

    print('Finish.')
    fullLog.close()
