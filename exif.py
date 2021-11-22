from PIL import Image
from PIL import ExifTags

img = Image.open('20090320_183722_1052490.jpg')
img_exif = img._getexif()
#print(img_exif.items())

if (img_exif is None):
    print('Picture don`t have exif data!')
elif 36868 not in img_exif.keys():
    print('No value for DateTime')
else:
    for key, val in img_exif.items():
        if key in ExifTags.TAGS:
            print(f'{ExifTags.TAGS[key]}:{val}')

#print(img_exif.keys())

print(img_exif[36868])

#print((img_exif[36868]).replace(':','').replace(' ','_'))
