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

import pyctags, os, time, sys

## This program can take over six minutes on an AMD Athlon 64 3000+ and 
## consumes over 1GB of RAM.  


srcdir = "../../temp extracts/linux-2.6.27"
if sys.platform.lower()[:len('linux')] == 'linux':
    srcdir = os.path.realpath("/usr/src/linux")

source_files = list()
extensions = ['.c', '.h', '.s']

cl = time.clock()
print ("Walking source tree %s..." % (srcdir))
for (dirpath, dirs, files) in os.walk(srcdir):
    for f in files:
        if f[-2:] in extensions:
            source_files.append(os.path.join(dirpath, f))
            
print ("%.2f seconds elapsed, found %d source files." % (time.clock() - cl, len(source_files)))
print ("This part will take a while.  I've seen it take five to eight minutes on my machine which isn't exactly tuff...")
cl = time.clock()
tf = pyctags.exuberant_ctags().generate_object(files=source_files, generator_options={"--fields" : "-sfk+Kn"})

print ("%d tags parsed in %.2f seconds." % (len(tf.tags), time.clock() - cl))
cl = time.clock()
names = pyctags.harvesters.name_lookup_harvester()
names.process_tag_list(tf.tags)
print ("Name index took %.2f seconds to build." % (time.clock() - cl))

abs_names = names.starts_with('abs_')
print ("%d tags start with the letters abs.  They are:" % (len(abs_names)))

for name in abs_names:
    print ("\t%s" % (name))
print("\n")

print ("%d tags start with the letters abse.  They are:" % (len(names.starts_with("abse"))))

for name in names.starts_with("abse"):
    print ("\t%s" % (name))
print("\n")

print ("%d tags start with a case sensitive match to 'abse'" % (len(names.starts_with("abse", case_sensitive=True))))

for name in names.starts_with("abse", case_sensitive=True):
    print ("\t%s" % (name))
print("\n")
    
print ("Or there's %d tags that start with a case sensitive mach to 'absE':" % (len(names.starts_with("absE", case_sensitive=True))))
for name in names.starts_with("absE", case_sensitive=True):
    print ("\t%s" % (name))

print ("Wait a little more...")
kind_harvest = pyctags.harvesters.kind_harvester()
kind_harvest.process_tag_list(tf.tags)
kind_dict = kind_harvest.get_data()

kinds_by_name = pyctags.harvesters.by_name_harvester()
kinds_by_name.process_tag_list(kind_dict['struct'])
struct_name_dict = kinds_by_name.get_data()

print("\nIf you felt like it, you could find out that the first (and only) struct that's called 'frag' is in file %s on line %d." % (struct_name_dict['frag'][0].file, struct_name_dict['frag'][0].line_number))
