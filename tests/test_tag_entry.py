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
from tag_entry import ctags_entry


entry_kwargs_pattern = {"name" : "testName", "file" : "../testFile", "pattern" : "testPattern", "extensions" : {"aa" : "aav", "bb" : "bbv"}}
entry_kwargs_min_line = {"name" : "testName", "file" : "../testFile", "line_number" : 555}
entry_kwargs_min_pattern = {"name" : "testName", "file" : "../testFile", "pattern" : "testPattern"}
entry_kwargs_line = {"name" : "testName", "file" : "../testFile", "line_number" : 555, "extensions" : {"aa" : "aav", "bb" : "bbv"}}
entry_kwargs_both = {"name" : "testName", "file" : "../testFile", "pattern" : "testPattern", "line_number" : 555, "extensions" : {"aa" : "aav", "bb" : "bbv"}}
entry_kwargs_neither = {"name" : "testName", "file" : "../testFile", "extensions" : {"aa" : "aav", "bb" : "bbv"}}
entry_kwargs_windows_path = {"name" : "testName", "file" : "C:\\foo\\bar\\testFile", "pattern" : "testPattern", "line_number" : 555, "extensions" : {"aa" : "aav", "bb" : "bbv"}}

class test_ctags_entry(unittest.TestCase):
    
    def test_pattern_init(self):
        d = entry_kwargs_pattern
        fn = d['file']
        te = ctags_entry(**d)
        self.failUnless(te.name == d['name'])
        self.failUnless(te.file == fn)
        self.failUnless(te.pattern == d['pattern'])
        self.failUnless(te.line_number == None)
        self.failUnless(te.extensions == d['extensions'])
        
    def test_linenum_init(self):
        d = entry_kwargs_line
        fn = d['file']
        te = ctags_entry(**d)
        self.failUnless(te.name == d['name'])
        self.failUnless(te.file == d['file'])
        self.failUnless(te.pattern == None)
        self.failUnless(te.line_number == d['line_number'])
        self.failUnless(te.extensions == d['extensions'])

    def test_both_init(self):
        d = entry_kwargs_both
        fn = d['file']
        te = ctags_entry(**d)
        self.failUnless(te.name == d['name'])
        self.failUnless(te.file == d['file'])
        self.failUnless(te.pattern == d['pattern'])
        self.failUnless(te.line_number == d['line_number'])
        self.failUnless(te.extensions == d['extensions'])

    def test_neither_init(self):
        te = None
        try:
            te = ctags_entry(**entry_kwargs_neither)
        except ValueError:
            pass
        self.failUnlessEqual(te, None)
    
    def test_str(self):
        te = ctags_entry(**entry_kwargs_both)
        short_fn = entry_kwargs_both['file'][entry_kwargs_both['file'].rfind("/") + 1:]
        should_be = "%s:%s:%s" % (te.name, short_fn, te.line_number)
        self.failUnless(str(te) == should_be)

    def test_empty_tag(self):
        te = None
        try:
            te = ctags_entry(**{})
        except ValueError:
            pass
        self.failUnlessEqual(te, None)
        
        try:
            te = ctags_entry({})
        except ValueError:
            pass
        self.failUnlessEqual(te, None)
        
    def test_min_line(self):
        d = entry_kwargs_min_line
        fn = d['file']
        te = ctags_entry(**d)
        self.failUnless(te.name == d['name'])
        self.failUnless(te.file == d['file'])
        self.failUnless(te.pattern == None)
        self.failUnless(te.line_number == d['line_number'])
        self.failUnless(te.extensions == None)
        
    def test_min_pattern(self):
        d = entry_kwargs_min_pattern
        fn = d['file']
        te = ctags_entry(**d)
        self.failUnless(te.name == d['name'])
        self.failUnless(te.file == d['file'])
        self.failUnless(te.pattern == d['pattern'])
        self.failUnless(te.line_number == None)
        self.failUnless(te.extensions == None)
        
    def test_missing_min(self):
        te = None
        try:
            te = ctags_entry({"name" : "testName", "file" : "testFile"})
        except ValueError:
            pass
        self.failIf(te != None)
        
        te = None
        try:
            te = ctags_entry({"name" : "testName", "line_number" : 555})
        except ValueError:
            pass
        self.failIf(te != None)

        te = None
        try:
            te = ctags_entry({"file" : "testFile", "line_number" : 555})
        except ValueError:
            pass
        self.failIf(te != None)

    def test_kwarg_init(self):
        self.failIf(False)
        
    def test_arg0_init(self):
        self.failIf(False)
        
    def test_eq_ne(self):
        te = ctags_entry(entry_kwargs_both)
        self.failUnlessEqual(te, te)
        
        ent = ctags_entry(entry_kwargs_both)
        self.failUnlessEqual(te, ent)
        
        ent = ctags_entry(**entry_kwargs_both)
        self.failUnlessEqual(te, ent)
        
        self.failUnlessEqual(ent, ent)
    
    def test_repr(self):
        te = ctags_entry(**entry_kwargs_both)
        
        ent = ctags_entry(repr(te))
        self.failUnlessEqual(te, ent)
        
        ent = ctags_entry(entry_kwargs_both)
        self.failUnlessEqual(te, ent)
        
        fail = True
        try:
            ent = ctags_entry(repr(te), **entry_kwargs_both)
        except:
            fail = False
            
        self.failIf(fail)
        
        
if __name__ == '__main__':
    unittest.main()
