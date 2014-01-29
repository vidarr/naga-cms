#!/usr/bin/python
import os.path
import sys
import unittest
import logging
#------------------------------------------------------------------------------
PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import transformator
#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------------
_logger       = logging.getLogger("test_registry")
#-------------------------------------------------------------------------------
# Helpers
#-------------------------------------------------------------------------------
def handler1(tokens):
    return "h1:" + tokens
#==============================================================================
class textTransformator(unittest.TestCase):
    '''Test transformator'''
    #--------------------------------------------------------------------------
    def setUp(self):
        self.transformator = transformator.Transformator()
        self.transformator.register_callback("heading", handler1)
    #--------------------------------------------------------------------------
    def test_no_transform(self):
        test_string = "abcdefghijklmnopqrstuvwxyz1234567890"
        self.assertEqual(test_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_escape(self):
        test_string = "abcdefg[[hijk]]lmnopqrst[[u]]vwxyz1234567890"
        res_string = "abcdefg[hijk]lmnopqrst[u]vwxyz1234567890"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_escape_2(self):
        test_string = "]]abcdefg[[hijk]]lmnopqrst[[u]]vwxyz1234567890"
        res_string = "]abcdefg[hijk]lmnopqrst[u]vwxyz1234567890"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_escape_3(self):
        test_string = "abcdefg[[hijk]]lmnopqrst[[u]]vwxyz1234567890[["
        res_string = "abcdefg[hijk]lmnopqrst[u]vwxyz1234567890["
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_1(self):
        test_string = "abcdefg[heading ijk]lmnopqrstuvwxyz1234567890"
        res_string = "abcdefgh1:heading ijklmnopqrstuvwxyz1234567890"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    # def test_link(self):
    #     pass
        # return test_transform('''Hagbard [link
        # https://de.wikipedia.org/wiki/Hagbard Germanische Sagengestalt]
        # Celine''', '''Hagbard <a
        # href="https://de.wikipedia.org/wiki/Hagbard">Germanische
        # Sagengestalt</a>''')
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    logging.basicConfig(filename='test_transformator.log',level=logging.DEBUG)
    unittest.main()
