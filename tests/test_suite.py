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
sys.path.append('../')
import test_tag_entry
import test_tag_file
import test_writetags
import test_harvesting

from kwargs_validator import ParameterError, the_validator as validator
from exuberant import exuberant_ctags
from tag_file import ctags_file
from tag_entry import ctags_entry
from tag_lists import tag_lists

tag_program = test_writetags.tag_program

class kwargs_validator(unittest.TestCase):
    def test_validator(self):
        fail = True
        try:
            validator.validate(['abc', 'ghi'], ['abc', 'def', 'ghi'])
            try:
                validator.validate(['abc', 'def', 'jkl'], ['abc', 'def', 'ghi'])
            except ParameterError:
                fail = False
        except:
            pass
        self.failIf(fail)
        
class end_to_end(unittest.TestCase):
    def test_end_to_end(self):
        ec = exuberant_ctags()
        tags = ec.generate_tags(tag_program=tag_program, files=test_writetags.file_lists['relpath'])
        tf = ctags_file(tags)
        tf2 = ctags_file(tag_lists['relpath']['head'] + tag_lists['relpath']['body'])
        i = 0
        for t in tf.tags:
            self.failUnless(t in tf2.tags)
            i += 1

l = unittest.TestLoader()
entry_tests = l.loadTestsFromModule(test_tag_entry)
tag_file_tests = l.loadTestsFromModule(test_tag_file)

write_tests = l.loadTestsFromModule(test_writetags)
harvest_tests = l.loadTestsFromModule(test_harvesting)

validator_tests = l.loadTestsFromTestCase(kwargs_validator)
ends = l.loadTestsFromTestCase(end_to_end)

alltests = unittest.TestSuite([write_tests, entry_tests, tag_file_tests, harvest_tests, validator_tests, ends])

r = unittest.TestResult()
unittest.TextTestRunner().run(alltests)
