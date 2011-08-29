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


# this program will only map out first-generation subclasses and doesn't handle multiple inheritance

import pyctags, os
srcdir = "../pyctags/"

class class_def:
    def __init__(self, entry=None):
        self.members = list()
        self.name = None
        self.location = None
        self.inherits_from = None
        if isinstance(entry, pyctags.ctags_entry):
            self.name = entry.name
            self.location = entry.line_number
            if 'inherits' in entry.extensions and len(entry.extensions['inherits']):
                self.inherits_from = entry.extensions['inherits']
        elif entry:
            self.name = entry

    def longest_name(self):
        longest = len(self.name)
        if self.inherits_from and len(self.inherits_from) > longest:
            longest = len(self.inherits_from)
        for member in self.members:
            if len(member[0]) > longest:
                longest = len(member[0])
        return longest
        
    def classbox(self):
        box = list()
        longest = self.longest_name()
        sep = (longest + 4) * "-"
        box.append(sep)
        box.append("| " + self.name + ((longest - len(self.name)) * " ") + " |")
        box.append(sep)
        for member in self.members:
            box.append("| " + member[0] + ((longest - len(member[0])) * " ") + " |")
        box.append(sep)
        return (box)
        
    def __str__(self):
        return self.name
        
class python_class_harvester(pyctags.harvesters.base_harvester):
    def __init__(self):
        self.class_data = dict()
        self.class_data['Exception'] = class_def('Exception')
        self.base_classes = dict()
        self.base_classes['Exception'] = list()

    def feed(self, entry):
        if 'kind' in entry.extensions:
            if entry.extensions['kind'] == 'c':
                if entry.name in self.class_data:
                    if self.class_data[entry.name].location is not None:
                        raise ValueError("Class name collision.")
                    else:
                        self.class_data[entry.name].location = entry.line_number
                        if 'inherits' in entry.extensions:
                            if len(entry.extensions['inherits']):
                                self.class_data[entry.name].inherits_from = entry.extensions['inherits']
                else:
                    self.class_data[entry.name] = class_def(entry)
                
            elif entry.extensions['kind'] == 'm':
                if 'class' not in entry.extensions:
                    raise ValueError("'class' tag not found in tag_entry that has a kind of 'm'(member)")
                classname = entry.extensions['class']
                if classname not in self.class_data:
                    self.class_data[classname] = class_def(classname)
                self.class_data[classname].members.append((entry.name, entry.file, entry.line_number))

    def do_after(self):
        # build the class hierarchy
        derived_classes = list()
        for cl_def in self.class_data.values():
            if not cl_def.inherits_from:
                self.base_classes[cl_def.name] = list()
            else:
                derived_classes.append(cl_def)
        
        for cl in derived_classes:
            self.base_classes[cl.inherits_from].append(cl.name)
    
    def pretty_print(self):
        for classname, children in self.base_classes.items():
            cl = self.class_data[classname]
            for line in cl.classbox():
                print (line)
            if len(children):
                print ("  ^")
                print ("  |")
                lastclass = len(children)
                thisclass = 1
                for child in children:
                    sc = self.class_data[child]
                    num = 0
                    for line in sc.classbox():
                        num += 1
                        if num == 1:
                            print ("  | " + line)
                        elif num == 2:
                            print ("  |-" + line)
                        elif thisclass == lastclass:
                            print ("    " + line)
                        else:
                            print ("  | " + line)
                    if thisclass < lastclass:
                        print ("  |")
                    thisclass += 1
            print("")

source_files = list()
for (dirpath, dirs, files) in os.walk(srcdir):
    for f in files:
        if f[-3:] == '.py':
            source_files.append(os.path.join(dirpath, f))

harvester = python_class_harvester()
ec = pyctags.exuberant_ctags()
   
tf = ec.generate_object(generator_options={"--fields" : "+in"}, files=source_files, harvesters=[harvester])

harvester.pretty_print()
