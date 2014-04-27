#!/usr/bin/python
#
# Part of the CMS naga, See <https://ubeer.org>
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
        self._file_name = file_name
        try:
            self.from_file(file_name)
        except IOError as io_exception:
            self._logger.warning("Could not read file " + file_name)
    #--------------------------------------------------------------------------    
    def from_file(self, file_name):
        file_object = open(file_name, 'r')
        for line in file_object:
            line = line.rstrip()
            entry = line.split(CFG_LIST_SEPARATOR)
            if len(entry) < 2:
                self._logger.error("Malformed line in " + str(file_name) + 
                " : " + str(line))
                break
            self._configuration[entry[0]] = entry[1:]
            self._logger.info('Found ' + entry[0])
    #--------------------------------------------------------------------------    
    def to_file(self, file_name = None):
        if not file_name:
            file_name = self._file_name
        file_object = open(file_name, 'wb')
        for key in self._configuration:
            value = self.get(key)
            file_object.write(bytes(key +
                    CFG_LIST_SEPARATOR + CFG_LIST_SEPARATOR.join(value) + '\n',
                    ENCODING))
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

