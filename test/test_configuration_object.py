import os.path
import sys
import logging
import random
import unittest
import string
import copy
import operator
#------------------------------------------------------------------------------
PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from configuration import ConfigurationObject
#------------------------------------------------------------------------------
_logger   = logging.getLogger("test_configuration_object")
FILE_NAME = './test_configuration_object_data_file'
#------------------------------------------------------------------------------
def fill_conf_object(conf_object, ref_hash):
    for key in ref_hash:
        conf_object.set(key, ref_hash[key])
#------------------------------------------------------------------------------
def get_random_string(length = 7):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) 
            for x in range(length))
#------------------------------------------------------------------------------
def get_ref_hash(number_of_keys = 11, number_of_values = 13):
    new_hash = {}
    keys = [get_random_string(11) for x in range(number_of_keys)]
    for key in keys:
        values = [get_random_string() for x in range(number_of_values)]
        new_hash[key] = values
    return new_hash
#==============================================================================
class ConfigurationObjectTest(unittest.TestCase):
    '''
    Test the configuration object
    '''
    #--------------------------------------------------------------------------
    def check_configuration_object(self, conf_object, conf_hash):
        for key in conf_object.get_keys():
            self.assertTrue(key in conf_hash)
            value = conf_object.get(key)
            self.assertTrue(value)
            print 'conf_object: ' + key + ' : ' + '.'.join(value) 
            print 'conf_hash  : ' + key + ' : ' + '.'.join(conf_hash[key])
            self.assertTrue(all(map(operator.eq, value, conf_hash[key])))
            del conf_hash[key]
        self.assertTrue(not conf_hash.keys())
    #--------------------------------------------------------------------------
    def setUp(self):
        pass
    #--------------------------------------------------------------------------
    def test_empty_config_object(self):
        self.check_configuration_object(ConfigurationObject(FILE_NAME), {})
    #--------------------------------------------------------------------------
    def test_without_file(self):
        ref_hash = get_ref_hash()
        conf_object = ConfigurationObject(FILE_NAME)
        fill_conf_object(conf_object, ref_hash)
        self.check_configuration_object(conf_object, ref_hash)
    #--------------------------------------------------------------------------
    def test_with_file(self):
        ref_hash = get_ref_hash()
        ref_hash_copy = copy.deepcopy(ref_hash)
        conf_object = ConfigurationObject(FILE_NAME)
        fill_conf_object(conf_object, ref_hash)
        conf_object.to_file(FILE_NAME)
        conf_object_2 = ConfigurationObject(FILE_NAME)
        os.remove(FILE_NAME)
        self.check_configuration_object(conf_object_2, ref_hash_copy)
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    logging.basicConfig(filename='test_configuration_object.log',level=logging.DEBUG)
    unittest.main()
    dispose_registry()

