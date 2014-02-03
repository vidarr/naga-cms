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
def handler1(call, tokens):
    return "h1:" + call + ' ' + tokens
#==============================================================================
class testTransformator(unittest.TestCase):
    '''Test transformator'''
    #--------------------------------------------------------------------------
    def setUp(self):
        self.transformator = transformator.Transformator()
        self.transformator.register_callback("heading", handler1)
        self.transformator.register_callback("b", handler1)
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
    def test_transform_beginning(self):
        test_string = "[heading ijk]lmnopqrstuvwxyz1234567890"
        res_string = "h1:heading ijklmnopqrstuvwxyz1234567890"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_end(self):
        test_string = "abcdefg[heading ijk]"
        res_string = "abcdefgh1:heading ijk"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_escapes(self):
        test_string = "[[ab]]cdefg[heading ijk]12345]]]]67890[["
        res_string = "[ab]cdefgh1:heading ijk12345]]67890["
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_transform_nested_escapes(self):
        test_string = "[[ab]]cdefg[heading i[[j]]k]12345]]]]67890"
        res_string = "[ab]cdefgh1:heading i[j]k12345]]67890"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_unknown_call(self):
        test_string = "[[ab]]cdefg[footer i[[j]]k]12345]]]]67890"
        res_string = "[ab]cdefgfooter i[j]k12345]]67890"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_nested_simple(self):
        test_string = "a[heading [b tata] ] a"
        res_string  = "ah1:heading h1:b tata  a"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_nested_begin(self):
        test_string = "[heading [b tata] ] a"
        res_string  = "h1:heading h1:b tata  a"
        self.assertEqual(res_string, self.transformator.transform(test_string))
    #--------------------------------------------------------------------------
    def test_nested_end(self):
        test_string = "a[heading [b tata] ]"
        res_string  = "ah1:heading h1:b tata "
        self.assertEqual(res_string, self.transformator.transform(test_string))
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    logging.basicConfig(filename='test_transformator.log',level=logging.DEBUG)
    unittest.main()
#     trans = transformator.Transformator()
#     print (trans.transform('''[heading Once upon a time] 
# [ilink tepahara]
# [link linking the link]
# [link tik]
# [kink ink]
# There has been some sort of list, it was 
# [olist * one *two *three]
# or 
# [link http://google.com [b google] ]
# [ulist *an item *and another]
# No one knew what it was about
# Others [link https://google.com linked] to the good old [link http://google.com]'''))
#  
