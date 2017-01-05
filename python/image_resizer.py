import os
import sys
from os import path
from PIL import Image

""" image_resizer.py
    resizes all images in a directory from a given size to a given size
    works recursively

    requirements:
        python 3.x
        PIL

    usage:
        * set size_mapping. Images matching the key-size are resized to the value-size.
        * call this script with the path to the directory containing images to be resized
        as the first argument
        * images should be resized in-place

"""

size_mapping = {
    "2048x1536": "1024x768"
}

excludes = []

def find_in_directory(dir, extensions, callback):
    for dir_name, subdirs, files in os.walk(dir):
        for filename in files:
            for extension in extensions:
                if extension in filename.lower()[-5:] and filename not in excludes:
                    callback(path.join(dir_name, filename))


def resize_if_matched(image_path):
    img = Image.open(image_path)
    size_str = '{}x{}'.format(img.size[0], img.size[1])

    if size_str in size_mapping:
        target_size = list(map(int, size_mapping[size_str].split('x')))
        result = img.resize(target_size, Image.ANTIALIAS)
        print("resized {} from {} to {}".format(path.basename(image_path), size_str, size_mapping[size_str]))
        result.save(image_path, img.format)


if __name__ == "__main__":
    find_in_directory(sys.argv[1], [".jpeg", ".jpg", ".png" ], resize_if_matched)
