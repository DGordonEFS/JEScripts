import os
import sys

""" usage
        copyxml.py path_to_images path_to_print
"""

def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)


path_to_images = sys.argv[1]
path_to_print = sys.argv[2]

files = filter(lambda x: os.path.basename(__file__) not in x, os.listdir(path_to_images))
files = filter(lambda x : x[0] is not '.', files)
files = filter(os.path.isfile, map(lambda x : os.path.join(path_to_images, x), files))
files = map(lambda x : os.path.join(path_to_print, os.path.basename(x)), files)
files = [(os.path.splitext(os.path.basename(x))[0], '/'.join(x.split(os.sep))) for x in files]

xml = ['<asset id="{id}" path="{path}" type="BITMAP" streaming="true"/>'.format(path=p, id=i) for i, p in files]

print('\n'.join(xml))
addToClipBoard('\n'.join(xml))