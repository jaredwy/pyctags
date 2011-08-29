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

import unittest, sys
sys.path.append("../pyctags")
from tag_file import ctags_file
from tag_entry import ctags_entry
from tag_lists import tag_lists

class test_ctags_file(unittest.TestCase):
    
    def test_init_noparams(self):
        tf = ctags_file()
        self.failIf(tf == None)
    
    def test_init_list(self):
        tf = ctags_file(tag_lists['unextended']['body'])
        for line in tag_lists['unextended']['body']:
            e = ctags_entry(line)
            self.failIf(e not in tf.tags)
            
        tf = ctags_file(tag_lists['relpath']['body'])
        for line in tag_lists['relpath']['body']:
            e = ctags_entry(line)
            self.failIf(e not in tf.tags)
        
    def test_parse_list(self):
        tf = ctags_file()
        tf.parse(tag_lists['unextended']['body'])
        
        tf = ctags_file()
        tf.parse(tag_lists['relpath']['body'])

    def test_init_with_filename(self):
        tf = ctags_file("relpath.tags")
        tf2 = ctags_file(tag_lists['relpath']['body'])
        self.failUnlessEqual(len(tf.tags), len(tf2.tags))

        i = 0
        for t in tf.tags:
            self.failUnlessEqual(t, tf2.tags[i])
            i += 1

    def test_parse_with_filename(self):
        tf = ctags_file()
        tf.parse("relpath.tags")
        tf2 = ctags_file(tag_lists['relpath']['body'])
        self.failUnlessEqual(len(tf.tags), len(tf2.tags))

        i = 0
        for t in tf.tags:
            self.failUnlessEqual(t, tf2.tags[i])
            i += 1
    
    def test_extended_kinds(self):
        tf = ctags_file(tag_lists['extended']['body'])
        tf2 = ctags_file(tag_lists['relpath']['body'])
        
        self.failUnlessEqual(tf.tags[0].extensions['kind'], tf2.tags[0].extensions['kind'])
    

if __name__ == '__main__':
    unittest.main()
