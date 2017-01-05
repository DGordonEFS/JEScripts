import subprocess
from os import listdir, getcwd, rename, remove
from os.path import isfile, join

""" multiedit.py
    allows simultanious renaming of multiple files
    requirements: 
        Python 2.x
        Sublime Text 3 (if on macOS, change sublime_text_path to point to `subl`, something like [/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl])

    usage:
        * `cd` to directory with the files to rename
        * run this script
        * a Sublime window should open, showing a list in the form
             file -> file
        * modify the right-hand-side of the mapping
        * save and close the document
        * the files should be renamed
"""

sublime_text_path = 'C:\Program Files\Sublime Text 3\subl'

temp_file = "multiedit.tmp"
files_in_cwd = [f for f in listdir(getcwd()) if isfile(join(getcwd(), f))]

with open(temp_file, "w+") as f:
    txt = ["{0} -> {0}".format(x) for x in files_in_cwd]
    f.write("\n".join(txt))

proc = subprocess.Popen((sublime_text_path, "-w", temp_file))
proc.wait()

new_lines = file(temp_file).readlines()
remove(temp_file)

for line in new_lines:
    oldname, newname = map(str.strip, line.split("->"))
    print oldname, "->", newname
    oldname, newname = map(lambda x: join(getcwd(), x), (oldname, newname))
    rename(oldname, newname)