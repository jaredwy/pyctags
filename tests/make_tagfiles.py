#!/usr/bin/env python
## Copyright (C) 2008 Ben Smith <benjamin.coder.smith@gmail.com>

##    This file is part of pyctags.

##    pyctags is free software: you can redistribute it and/or modify
##    it under the terms of the GNU Lesser General Public License as published
##    by the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.

##    pyctags is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU Lesser General Public License
##    and the GNU Lesser General Public Licens along with pyctags.  If not, 
##    see <http://www.gnu.org/licenses/>.

import subprocess, sys

tag_program = 'ctags'

# set this to true to test system-specific absolute paths.
# anyone testing this that isn't on my computer will need to adjust the paths to test this area
extended_tests = False

default_flags = '--excmd=pattern --langmap=python:+.pyw -L -'
extended_flags = '--fields=+afiklmnsStz --excmd=pattern --langmap=python:+.pyw -L -'
hyper_extended_flags = '--fields=+afiKlmnsStz --excmd=pattern -L -'
unextended_flags = '--format=1 --langmap=python:+.pyw -L -'
no_kinds_flags = '--fields=-k+afilmnsStz --excmd=pattern --langmap=python:+.pyw -L -'
source_files = ['tag_file.py', 'tag_entry.py', 'exuberant.py', 'tag_base.py', 'kwargs_validator.py', 'harvesters.py']

relpath_prefix = '../pyctags/'
absolute_windows_prefixes = {'unc' : '\\\\lazarus\\pyctags\\pyctags\\', 
                             'drive_letter' : 'C:\\Documents and Settings\\Ben\\Desktop\\pyctags\\pyctags\\'
                             }

file_lists = dict()

file_lists['relpath'] = list()
for sf in source_files:
    file_lists['relpath'].append(relpath_prefix + sf)

if extended_tests:
    if sys.platform == 'win32':
        for abs_prefix in absolute_windows_prefixes.keys():
            file_lists[abs_prefix] = list()
            for sf in source_files:
                file_lists[abs_prefix].append(absolute_windows_prefixes[abs_prefix] + sf)


def make_tagfiles():
    
    generation_options = []
    for group in file_lists.keys():
        output_file = "%s.tags" % group
        generation_options.append([file_lists[group], output_file, default_flags])
    
    generation_options += [[file_lists['relpath'], "extended.tags", extended_flags], 
                           [file_lists['relpath'], "hyper_extended.tags", hyper_extended_flags],
                           [file_lists['relpath'], "no_kinds.tags", no_kinds_flags],
                           [file_lists['relpath'], "unextended.tags", unextended_flags]
                           ]

    for opt in generation_options:
        shell_cmd = "%s %s -f %s" % (tag_program, opt[2], opt[1])
        
        inp_line = ''
        for o in opt[0]:
            inp_line += "%s\n" % o
        p = subprocess.Popen(shell_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        
        p.communicate(input=inp_line.encode())
        if p.returncode != 0:
            raise Exception

if __name__ == '__main__':
    make_tagfiles()
    
    
