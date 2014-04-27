#!/usr/bin/python
#
# Part of the CMS naga, See <https://ubeer.org
#
#    Copyright (C) 2013, 2014 Michael J. Beer <michael.josef.beer@googlemail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#------------------------------------------------------------------------------
import os.path
import sys
import shutil
#------------------------------------------------------------------------------
PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import store
import unittest
import logging
import tempfile
#==============================================================================
def get_store_directory():
    '''
    Sets up a directory for FileStore to be used
    '''
    dir_path = tempfile.mkdtemp()
    return dir_path
#------------------------------------------------------------------------------
def clean_store(test_store_directory):
    '''
    Removes any remnants of the test file store from disk
    '''
    shutil.rmtree(test_store_directory)
#------------------------------------------------------------------------------
class StoreObjectTest(unittest.TestCase):
    '''
    Test a store object
    '''
    def setUp(self):
        pass
    #--------------------------------------------------------------------------
    def test_empty_store(self):
        '''
        Test an empty store
        '''
        test_store_directory = get_store_directory()
        test_store = store.FileStore(test_store_directory, 'test://')
        self.assertEqual(test_store.get_keys(), [])
        test_store.remove('taba')
        self.assertEqual(test_store.get('luga'), None)
        self.assertEqual(test_store.get_uri('tv'), None)
        clean_store(test_store_directory)
    #--------------------------------------------------------------------------
    def test_filling_store(self):
        '''
        Test an empty store being filled
        '''
        test_store_directory = get_store_directory()
        test_store = store.FileStore(test_store_directory, 'test://')
        test_store.put('ogg', 'vorbis')
        test_store.put('rincewind', 'twoflower')
        self.assertEqual(test_store.get('magrat'), None)
        self.assertEqual(test_store.get('ogg'), 'vorbis')
        self.assertEqual(test_store.get('garlick'), None)
        self.assertEqual(test_store.get('rincewind'), 'twoflower')
        clean_store(test_store_directory)
    #--------------------------------------------------------------------------
    def test_persistent_store(self):
        '''
        Test an empty store being filled that stores persistently on disk,
        then use another store object to retrieve the stored data
        '''
        test_store_directory = get_store_directory()
        test_store = store.FileStore(test_store_directory, 'test://')
        test_store.put('ogg', 'vorbis')
        test_store.put('rincewind', 'twoflower')
        self.assertEqual(test_store.get('magrat'), None)
        self.assertEqual(test_store.get('ogg'), 'vorbis')
        self.assertEqual(test_store.get('garlick'), None)
        self.assertEqual(test_store.get('rincewind'), 'twoflower')
        test_store = store.FileStore(test_store_directory, 'test://')
        self.assertEqual(test_store.get('magrat'), None)
        self.assertEqual(test_store.get('ogg'), 'vorbis')
        self.assertEqual(test_store.get('garlick'), None)
        self.assertEqual(test_store.get('rincewind'), 'twoflower')
        clean_store(test_store_directory)
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    logging.basicConfig(filename='test_store.log', level=logging.DEBUG)
    unittest.main()
