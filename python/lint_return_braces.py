import os
from os import path
import sys
import xml.etree.ElementTree
import re
import json
""" Recursively scans all xml files in the supplied directory 
searching for script tags containing return statements
prints out the filepath and code snippet if it detects a mismatch in braces

usage: python3 line_return_braces.py /path/to/directory/containing/xml/files
"""


def lint_project(root):
    print("searching \"{root}\" for mismatched braces".format(root=root))
    xml_files = []
    
    errors = {
        'braces': {}
    }

    files_scanned = 0
    for dir_name, subdirs, files in os.walk(root):
        for filename in files:
            if filename[-4:] == ".xml":
                files_scanned = files_scanned + 1
                filepath = path.join(dir_name, filename)
                brace_mismatches = check_braces_for_file(filepath)
                if len(brace_mismatches) > 0:
                    if not filepath in errors['braces']: 
                        errors['braces'][filepath] = []
                    errors['braces'][filepath].append(brace_mismatches)

    print(json.dumps(errors, sort_keys=True, indent=4, separators=(',', ': ')))


def check_braces_for_file(filepath):
    ret = []
    with open(filepath, 'r') as f:
        data = f.read()
        for m in re.finditer('return', data):
            return_start_index = m.start()

            # scan backwards to find the beginning of the tag
            tag_start_offset = 0
            c = ''
            while '<!' not in c:
                tag_start_offset = tag_start_offset + 1
                c = data[return_start_index - tag_start_offset:
                         return_start_index - tag_start_offset + 2]
            # then forwards to the end
            tag_end_offset = 0
            c = ''
            while '</' not in c:
                tag_end_offset = tag_end_offset + 1
                c = data[return_start_index + tag_end_offset:
                         return_start_index + tag_end_offset + 2]

            # see if the number of opening braces matches the number of closing
            # braces
            script_string = data[
                return_start_index - tag_start_offset:return_start_index + tag_end_offset]
            n_open = script_string.count('[')
            n_close = script_string.count(']')
            line_number = data[0:return_start_index-tag_start_offset].count('\n') + 1
            if n_open is not n_close:
                ret.append("(line:{line})    {script}".format(line=line_number, script=script_string))
    return ret

if __name__ == '__main__':
    lint_project(sys.argv[1])
