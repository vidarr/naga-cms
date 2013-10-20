#!/usr/bin/python
import os.path
import sys
import logging
import re
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
#------------------------------------------------------------------------------    
class ConfigurationObject:
    
    def __init__(self, file_name):
        self._logger = logging.getLogger("ConfigurationObject")
        self._configuration = {}
        try:
            self.from_file(file_name)
        except IOError as io_exception:
            self._logger.warning("Could not read file " + file_name)
    #--------------------------------------------------------------------------    
    def from_file(self, file_name):
        file_object = open(file_name, 'r')
        for line in file_object:
            line = line.rstrip()
            print "line = " + line + "|"
            entry = line.split(CFG_LIST_SEPARATOR)
            if len(entry) < 2:
                self._logger.error("Malformed line in " + str(file_name) + 
                " : " + str(line))
                break
            self._configuration[entry[0]] = entry[1:]
            self._logger.info('Found ' + entry[0])
    #--------------------------------------------------------------------------    
    def to_file(self, file_name):
        file_object = open(file_name, 'w')
        for key in self._configuration:
            value = self.get(key)
            file_object.write(key +
                    CFG_LIST_SEPARATOR + CFG_LIST_SEPARATOR.join(value) + '\n')
        file_object.close()
    #--------------------------------------------------------------------------    
    def get_keys(self):
        return self._configuration.keys()
    #--------------------------------------------------------------------------    
    def get(self, key):
        if not key in self._configuration:
            self._logger.warning(key + " not found in configuration")
            return None
        return self._configuration[key]
    #--------------------------------------------------------------------------    
    def set(self, key, value):
        if not type(value) == type([]):
            self._logger.error("Called set with non-list value")
            return None
        self._configuration[key] = value
        return True

