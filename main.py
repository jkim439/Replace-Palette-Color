__author__ = 'Junghwan Kim'
__copyright__ = 'Copyright 2016-2018 Junghwan Kim. All Rights Reserved.'
__version__ = '1.0.0'

import os
import shutil
import numpy
from PIL import Image
import hashlib


def main():

    # Set input path
    path = '/home/jkim/DATA'

    # Output information
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nReplace Color %s' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\nYou set path: %s' % (__version__, path)
    answer = raw_input('Are you sure to start right now (y/n)? ')
    if answer != 'y':
        print '\n[ERROR] Cancelled by user.'
        exit(0)

    # Set variables
    result = 0
    palette = numpy.load('palette.npy')
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # Recur load input directories
    for dir in sorted(dirs):

        # Check folder
        if not dir.isdigit():
            continue

        # Output loaded folder
        print '\n[LOAD]', path + '/' + dir

        # Set path
        path_original = path + '/' + dir + '/labels.ori'
        path_target = path + '/' + dir + '/labels'

        # New folder
        if not os.path.exists(path_original):
            os.makedirs(path_original)
        else:
            print '[ERROR] labels.ori folder is exists.'
            exit(1)

        # Copy label files & Verify process
        for paths, dirs, files in sorted(os.walk(path_target)):
            for name in sorted(files):
                if name.endswith('.png'):
                    shutil.copyfile(path_target + '/' + name, path_original + '/' + name)
                    if md5ChkSum(path_original + '/' + name) != md5ChkSum(path_target + '/' + name):
                        print '[ERROR] Copy is failed because MD5 checksums are different.'
                        exit(1)

        # Replace palette array
        images = 0
        for paths, dirs, files in sorted(os.walk(path_target)):
            for name in sorted(files):
                img = Image.fromarray(numpy.array(Image.open(path_target + '/' + name)), mode='P')

                for x in range(512):
                    for y in range(512):
                        pixel = img.getpixel((x, y))
                        if pixel == 17:
                            img.putpixel((x, y), 7)
                        elif pixel == 16:
                            img.putpixel((x, y), 6)

                img.putpalette(palette)
                img.save(path_target + '/' + name, "PNG")
                images += 1

        # Complete every process
        result += 1
        print '[SUCCESS]', images, 'images are replaced.'

    # Print result
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nResult' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\n', result, 'Folders are processed successfully.'

    return None


def md5ChkSum(_file):  # Calculates MD5 CheckSum
    with open(_file, 'rb') as fp:
        hash_obj = hashlib.md5()

        line = fp.readline()
        while line:
            hash_obj.update(line)
            line = fp.readline()
        return hash_obj.hexdigest()


if __name__ == '__main__':
    main()