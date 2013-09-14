#!/usr/bin/python
import StringIO
import os.path
import sys


PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
from logger import log

categories = None

def get_categories():
    if categories == None:
        categories = Categories(CATEGORIES_FILE_PATH)
        categories.from_file()
    return categories

class Categories:

    def __init__(self, file_name):
        self.file_name  = file_name
        self.categories = []

    def from_file(self, file_name = None):
        if not file_name:
            file_name = self.file_name
        file_object = open(file_name, "r")
        categories_string = file_object.read()
        file_object.close()
        if categories_string:
            self.categories = string.split(categories_string,
                    CFG_LIST_SEPARATOR)
            log(LOG_DEBUG, "Categories.from_file: Read in " +
                    len(self.categories).__str__() + " categories")
        else:
            self.categories = []
            log(LOG_DEBUG, "Categories.from_file: " + file_name + " empty")

    def to_file(self, file_name = None):
        if not file_name:
            file_name = self.file_name
        file_object = open(file_name, "w")
        categories_string = string.join(self.categories, CFG_LIST_SEPARATOR)
        file_object.write(categories_string)
        file_object.close()

    def get_categories(self):
        return self.categories

    def add_category(self, category):
        self.categories.append(category)

    def remove_category(self, category):
        self.categories.remove(category)

