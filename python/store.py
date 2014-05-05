#!/usr/bin/python3
#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2014 Michael J. Beer <michael.josef.beer@googlemail.com>
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
import logging
import sys
from os import listdir, remove
from os.path import isfile, join, dirname, abspath
#---------------------------------------------------------------------------    
PAGE_ROOT   = join(dirname(abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR)
from naga_config import *
from configuration import ConfigurationObject
from security import sanitize_string
#------------------------------------------------------------------------------
_logger = logging.getLogger("store")
#------------------------------------------------------------------------------
def get_store(store_type):
    if store_type == STORE_TYPE_FILE:
        _logger.debug("Going to return " + NAGA_ABS_ROOT + " " + \
                PAGE_ROOT + " " + STORE_FILE_PATH)
        _logger.debug("Going to return " + join(NAGA_ABS_ROOT, PAGE_ROOT,
            STORE_FILE_PATH))
        return FileStore(join(NAGA_ABS_ROOT, PAGE_ROOT, STORE_FILE_PATH), 
                join(NAGA_ROOT, STORE_FILE_PATH),
                mode='b')
    if store_type == STORE_TYPE_IMAGE:
        return FileStore(join(NAGA_ABS_ROOT, PAGE_ROOT, STORE_IMAGE_PATH),
                join(NAGA_ROOT, IMAGE_DIR),
                mode='b')
    return None
#------------------------------------------------------------------------------
class FileStore(object):
    '''
    Persistently store key/value pairs using one file per value
    '''
    def __init__(self, base_dir, uri_prefix, **options):
        '''
        Create key/value store
        '''
        self.__base_dir = base_dir
        self.__uri_prefix = uri_prefix
        self.__logger = logging.getLogger()
        self.__mode = ""
        if 'mode' in options:
            self.__mode = options['mode']
    #--------------------------------------------------------------------------
    def get_keys(self):
        '''
        Get all keys currently within this store
        '''
        return [file_name for file_name in listdir(self.__base_dir) if
                isfile(join(self.__base_dir, file_name))]
    #--------------------------------------------------------------------------
    def put(self, key, content):
        '''
        Add a new key/value pair. If key exists, its value will be overwritten
        '''
        key = sanitize_string(key, keep_dot=True)
        file_name = join(self.__base_dir, key)
        mode = 'w' + self.__mode
        file_object = open(file_name, mode)
        file_object.write(content)
        file_object.close()
    #--------------------------------------------------------------------------
    def remove(self, key):
        '''
        Remove key/value pair from store
        '''
        key = sanitize_string(key, keep_dot=True)
        file_name = join(self.__base_dir, key)
        if os.path.isfile(file_name):
            remove(file_name)
    #--------------------------------------------------------------------------
    def get(self, key):
        '''
        get value of a key if available, else None is returned
        '''
        key = sanitize_string(key, keep_dot=True)
        file_name = self.__get_file_name(key)
        if not isfile(file_name):
            return None
        mode = 'r' + self.__mode
        file_object = open(file_name, mode)
        content = file_object.read()
        file_object.close()
        return content
    #--------------------------------------------------------------------------
    def get_uri(self, key):
        '''
        Get URI that can be used to retrieve the content
        '''
        key = sanitize_string(key, keep_dot=True)
        if isfile(self.__get_file_name(key)):
            return join(self.__uri_prefix, key) # self.__base_dir, key)
        return None
    #--------------------------------------------------------------------------
    def __get_file_name(self, key):
        return join(self.__base_dir, key)
