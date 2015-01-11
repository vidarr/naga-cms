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
import string
import logging
#-------------------------------------------------------------------------------
ABS_PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(ABS_PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
#-------------------------------------------------------------------------------
global_categories = None
#-------------------------------------------------------------------------------
def get_categories():
    global global_categories
    if global_categories == None:
        global_categories = Categories(NAGA_ABS_ROOT + PATH_SEPARATOR + \
                CATEGORIES_FILE_PATH)
        global_categories.from_file()
    return global_categories
#-------------------------------------------------------------------------------
class Categories:

    def __init__(self, file_name):
        self.file_name  = file_name
        self.categories = []
        self.logger     = logging.getLogger("Categories")

    def from_file(self, file_name = None):
        if not file_name:
            file_name = self.file_name
        file_object = open(file_name, "r")
        categories_string = file_object.read()
        file_object.close()
        if categories_string:
            self.categories = categories_string.rstrip().split(CFG_LIST_SEPARATOR)
            self.logger.debug("Categories.from_file: Read in " +
                    len(self.categories).__str__() + " categories")
        else:
            self.categories = []
            self.logger.debug("Categories.from_file: " + file_name + " empty")

    def to_file(self, file_name = None):
        if not file_name:
            file_name = self.file_name
        file_object = open(file_name, "wb")
        categories_string = string.join(self.categories, CFG_LIST_SEPARATOR)
        file_object.write(categories_string)
        file_object.close()

    def get_categories(self):
        return self.categories

    def add_category(self, category):
        self.categories.append(category)

    def remove_category(self, category):
        self.categories.remove(category)

