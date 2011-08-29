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

from unittest import TestCase, main as unittest_main
import sys
sys.path.append("../pyctags")
from tag_file import ctags_file
from harvesters import kind_harvester, name_lookup_harvester, by_name_harvester
from tag_lists import tag_lists
from exuberant import exuberant_ctags 
from make_tagfiles import tag_program

class TestHarvesting(TestCase):
    def do_kind_harvest(self, taglist):
        kh = kind_harvester()
        tf = ctags_file(taglist, harvesters=[kh])
        return (tf, kh.get_data())
    
    def check_kind_keys(self, kinds, keys):
        for k in keys:
            self.failUnless(k in kinds)
            self.failUnless(type(kinds[k]), list)
            self.failUnless(len(kinds[k]))

    def test_kind_harvester(self):

        ec = exuberant_ctags(tag_program=tag_program)

        (tf, kinds) = self.do_kind_harvest(tag_lists['unextended']['body'])
        self.failUnlessEqual(len(kinds), 0)
        
        (tf, kinds) = self.do_kind_harvest(tag_lists['no_kinds']['body'])
        self.failUnlessEqual(len(kinds), 0)

        (tf, kinds) = self.do_kind_harvest(tag_lists['relpath']['body'])
        if ec.version == "5.7":
            self.failUnlessEqual(len(kinds), 2)
            self.check_kind_keys(kinds, ['c', 'm'])
        elif ec.version == "5.6b1":
            self.failUnlessEqual(len(kinds), 3)
            self.check_kind_keys(kinds, ['c', 'm', 'v'])
        
        for tag in tf.tags:
            if 'kind' in tag.extensions:
                self.failUnless(tag in kinds[tag.extensions['kind']])

        (tf, kinds) = self.do_kind_harvest(tag_lists['hyper_extended']['body'])
        if ec.version == "5.7":
            self.failUnlessEqual(len(kinds), 2)
            self.check_kind_keys(kinds, ['class', 'member'])
        elif ec.version == "5.6b1":
            self.failUnlessEqual(len(kinds), 3)
            self.check_kind_keys(kinds, ['class', 'member', 'variable'])
        
        for tag in tf.tags:
            if 'kind' in tag.extensions:
                self.failUnless(tag in kinds[tag.extensions['kind']])

    def test_by_name_harvester(self):
        by_name_h = by_name_harvester()
        tf = ctags_file(tag_lists['extended']['body'], harvesters=[by_name_h])
        name_dict = by_name_h.get_data()
        self.failUnless('ctags_entry' in name_dict)
        self.failUnless(name_dict['ctags_entry'][0].name == 'ctags_entry')
        self.failUnless(name_dict['ctags_entry'][0].extensions['kind'] == 'c')


    def test_name_lookup_harvester(self):
        lookup_harvest = name_lookup_harvester()
        tf = ctags_file(tag_lists['extended']['body'], harvesters=[lookup_harvest])
        ec = exuberant_ctags(tag_program=tag_program)
        
        # exuberant ctags 5.8 picks up 5 matches, because of copy.copy
        tags = lookup_harvest.starts_with('c', case_sensitive=True)
        if ec.version in ['5.7', '5.6b1']:
            self.failUnlessEqual(len(tags), 4)
        if ec.version in ['5.8']:
            self.failUnlessEqual(len(tags), 5)

        tags = lookup_harvest.starts_with('C', case_sensitive=True)
        self.failUnlessEqual(len(tags), 0)
        
        atags = lookup_harvest.starts_with('a')
        self.failUnlessEqual(len(atags), 0)

        tags = lookup_harvest.starts_with('c')
        if ec.version in ['5.7', '5.6b1']:
            self.failUnlessEqual(len(tags), 4)
        if ec.version in ['5.8']:
            self.failUnlessEqual(len(tags), 5)
        
        tag_tags = lookup_harvest.starts_with('ctags_')
        self.failUnlessEqual(len(tag_tags), 4)

        tags = lookup_harvest.starts_with('c', num_results=2)
        self.failUnlessEqual(len(tags), 2)

        tags = lookup_harvest.starts_with('C', num_results=2)
        self.failUnlessEqual(len(tags), 2)
    
        tags = lookup_harvest.starts_with('c', num_results=5)
        self.failUnless(len(tags) <= 5)

        tags = lookup_harvest.starts_with('c', num_results=3, case_sensitive=True)
        self.failUnlessEqual(len(tags), 3)

        tags = lookup_harvest.starts_with('C', num_results=2, case_sensitive=True)
        self.failUnlessEqual(len(tags), 0)
    
        tags = lookup_harvest.starts_with('c', num_results=2, case_sensitive=False)
        self.failUnlessEqual(len(tags), 2)

        tags = lookup_harvest.starts_with('C', num_results=2, case_sensitive=False)
        self.failUnlessEqual(len(tags), 2)


if __name__ == '__main__':
    unittest_main()
