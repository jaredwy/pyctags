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

import os
from make_tagfiles import file_lists, extended_tests, make_tagfiles

tag_lists = dict()

files = list(file_lists.keys())
files.append('extended')
files.append('unextended')
files.append('hyper_extended')
files.append('no_kinds')

for k in files:
    filename = "%s.tags" % k
    if not os.path.exists(filename):
        make_tagfiles()
    f = open(filename).readlines()
    lines = list()
    
    for l in f:
        lines.append(l.strip())
        
    tag_lists[k] = {'head' : lines[0:6], 'body' : lines[6:]}
