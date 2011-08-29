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


import unittest, os, sys
sys.path.append("../pyctags")
from exuberant import exuberant_ctags
from tag_lists import tag_lists
from make_tagfiles import file_lists, extended_tests, tag_program
from tag_file import ctags_file


class test_exuberant_ctags(unittest.TestCase):
    
    def test_init(self):
        ec = exuberant_ctags(tag_program=tag_program, files=file_lists['relpath'])
        ec = exuberant_ctags(files=file_lists['relpath'])
        ec = exuberant_ctags(tag_program=tag_program)
        ec = exuberant_ctags()
    
    def test_executable_set(self):
        ec = exuberant_ctags(tag_program=tag_program)
        ec.generate_tagfile("generated.tags", tag_program=tag_program, files=file_lists['relpath'])
        self.failIf(not os.path.exists("generated.tags"))
        os.remove("generated.tags")
        
        if sys.platform == "win32" and extended_tests:
            ec = exuberant_ctags()
            ec.ctags_executable('/bin/ctags')
            ec.generate_tagfile("generated.tags", tag_program=tag_program, files=file_lists['relpath'])
            self.failIf(not os.path.exists("generated.tags"))
            os.remove("generated.tags")
        
        ec = exuberant_ctags()
        ec.generate_tagfile("generated.tags", tag_program=tag_program, files=file_lists['relpath'])
        self.failIf(not os.path.exists("generated.tags"))
        os.remove("generated.tags")
    
    def test_empty_list(self):
        ec = exuberant_ctags(tag_program=tag_program, files=[])
        tags = ec.generate_tags()
        self.failUnlessEqual(len(tags), 0)
    
    def test_no_ctags_set(self):
        ec = exuberant_ctags(files=file_lists['relpath'])
        try:
            tags = ec.generate_tags()
            self.failUnlessEqual(tags[0], tag_lists['relpath']['body'][0])
        except ValueError:
            # this happens if ctags isn't on the path, but it isn't fatal.
            pass
        
    def test_generate_tags(self):
        ec = exuberant_ctags()
        tags = ec.generate_tags(tag_program=tag_program, files=file_lists['relpath'])
        self.failUnlessEqual(tags[0], tag_lists['relpath']['body'][0])
        self.failUnlessEqual(tags[-1], tag_lists['relpath']['body'][-1])

    def test_generate_from_unc_files(self):
        if extended_tests and sys.platform == "win32":
            ec = exuberant_ctags(tag_program=tag_program, files=file_lists['unc'])
            tags = ec.generate_tags()
            self.failUnlessEqual(tags[0], tag_lists['unc']['body'][0])
    
    def test_generate_from_drive_letter_path(self):
        if extended_tests and sys.platform == "win32":
            ec = exuberant_ctags(tag_program=tag_program, files=file_lists['drive_letter'])
            tags = ec.generate_tags()
            self.failUnlessEqual(tags[0], tag_lists['drive_letter']['body'][0])
        
    def test_generate_to_unc_filename(self):
        if extended_tests and sys.platform == "win32":
            ec = exuberant_ctags(tag_program=tag_program, files=file_lists['relpath'])
            self.failUnless(ec.generate_tagfile('\\\\lazarus\\network write\\tagfile'))
        
    def test_generate_to_drive_letter_path(self):
        if extended_tests and sys.platform == "win32":
            ec = exuberant_ctags(tag_program=tag_program, files=file_lists['relpath'])
            self.failUnless(ec.generate_tagfile('C:\\tagfile'))
        
    def test_generate_tagfile(self):
        ec = exuberant_ctags(tag_program=tag_program, files=file_lists['relpath'])
        ec.generate_tagfile("generated.tags")
        self.failIf(not os.path.exists("generated.tags"))
        os.remove("generated.tags")
        
        ec = exuberant_ctags(tag_program=tag_program)
        ec.generate_tagfile("generated.tags", files=file_lists['relpath'])
        self.failIf(not os.path.exists("generated.tags"))
        os.remove("generated.tags")

        ec = exuberant_ctags()
        ec.generate_tagfile("generated.tags", tag_program=tag_program, files=file_lists['relpath'])
        self.failIf(not os.path.exists("generated.tags"))
        os.remove("generated.tags")

    def test_custom_params(self):
        ec = exuberant_ctags(tag_program=tag_program, files=file_lists['relpath'])
        tags = ec.generate_tags(generator_options={'-e' : None})
        self.failUnless(ec.command_line.find(' -e ') > 0)
        
        # could use a few more tests here
        # test the generated command line as well
        
    def test_custom_input_files(self):
        ec = exuberant_ctags(tag_program=tag_program)
        ec.generate_tagfile("customtags", generator_options={'-L' : "relpath.txt"})
        self.failIf(not os.path.exists("customtags"))
        os.remove("customtags")

    def test_exuberant_kinds(self):
        ec = exuberant_ctags(tag_program=tag_program)
        self.failUnless("python" in ec.language_info)
        self.failUnless("c++" in ec.language_info)

    def test_warnings(self):
        fl = file_lists['relpath'][:]
        fl.append("foobar.py")
        ec = exuberant_ctags(tag_program=tag_program, files=fl)
        ec.generate_tags()
        self.failUnless(len(ec.warnings))
        self.failUnless(ec.warnings[0].find('Warning: cannot open source file "foobar.py" : No such file or directory') > 0)

        ec.generate_tags(files=file_lists['relpath'])
        self.failUnlessEqual(len(ec.warnings), 0)
    
    def test_generate_object(self):
        ec = exuberant_ctags(tag_program=tag_program, files=file_lists['relpath'])
        tf = ec.generate_object()
        tf2 = ctags_file(tag_lists['relpath']['body'])
        
        self.failIfEqual(tf, None)
        self.failUnless(len(tf.tags))
        i = 0
        for tag in tf2.tags:
            self.failUnlessEqual(repr(tag), repr(tf.tags[i]))
            i += 1
    
    def test_language_maps(self):
        ec = exuberant_ctags(tag_program=tag_program)
        self.failUnless('.x68' in ec.all_extensions)
        self.failUnless('.x86' in ec.language_extensions['Asm'])
        self.failUnless('makefile' in ec.all_extensions)
        self.failUnless('.scm' in ec.all_extensions)
        
if __name__ == '__main__':
    unittest.main()
