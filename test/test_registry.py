#!/usr/bin/python
import StringIO
import os.path
import sys
import tempfile
import shutil
import unittest
import random
import string
import logging

PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import registry
from article import Article
#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
NUMBER_OF_CATEGORIES       = 10
MAX_NO_ARTICLES            = 10
NO_NEGATIVE_ARTICLE_CHECKS = 10
#-------------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------------
_registry     = None
temp_dir_name = None
_logger       = logging.getLogger("test_registry")
#-------------------------------------------------------------------------------
# Helpers
#-------------------------------------------------------------------------------
def init_registry():
    '''Create a new empt_registry'''
    temp_dir_name  = tempfile.mkdtemp()
    temp_file_name = 'temp.csv'
    temp_file      = open(temp_dir_name + os.sep + temp_file_name, 'w')
    temp_file.close()
    _logger.debug("Created " + temp_dir_name + os.sep + temp_file_name)
    global _registry
    _registry      = registry.Registry(temp_dir_name, temp_file_name)

def dispose_registry():
    '''
    Clean up.
    Remove any trace within the file system of this test.
    '''
    _registry = None
    shutil.rmtree(temp_dir_name)
    temp_dir_name = None
    _logger.debug("Removed " + temp_dir_name)

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

def random_name():
    return random_string(random.randint(1, 60))

def random_heading():
    return random_string(random.randint(0, 100))

def random_timestamp():
    return random_string(random.randint(0, 60))

def random_categories(categories):
    return [random.choice(categories) for i in 
            range(random.randint(2, len(categories)))]

def test_false_article_name(articles_data):
    '''
    Generate article name that should not be contained within the registry,
    then check that there is no such article within the registry
    article_data is of the form as storeAndRetrieve.article_data
    '''
    get_another_name = True
    while get_another_name:
        article_name = random_name()
        get_another_name = False
        for article in articles_data:
            print "Checking " 
            print article
            if article[0] == article_name:
                get_another_name = True
                break
    if _registry.get(article_name) != None:
        print 'Found ' + article_name + ' in registry'
        return False
    return True

def test_all_article_names(articles_data):
    '''
    Test whether ALL articles described in article_data are contained within 
    the registry
    article_data is of the form as storeAndRetrieve.article_data
    '''
    for article in articles_data:
        if _registry.get(article[0]) == None:
            print 'Did not find ' + article[0]
            return False
    return true

def test_article_name(article_data):
    '''
    Test whether the article described within article_data is contained within
    the registry
    '''
    if _registry.get(article_data[0]) == None:
        print 'Did not find ' + article_data[0]
        return False
    return True

def insert_article(article_data):
    '''
    Insert an article into the registry.
    The article is described by a list containing 
    [file_name, heading, timestamp, [category1, category2, ...]]
    '''
    print article_data
    if type(article_data) != type([]):
        print "insert_article: Called with a parameter that is not a list"
        _logger.error("insert_article: Called with a parameter that is not a list")
        return False
    article_object = Article()
    article_object.set_heading(article_data[1])
    article_object.set_timestamp(article_data[2])
    article_object.set_categories(article_data[3])
    _registry.add(article_data[0], article_object)
    return True

class storeAndRetrieve(unittest.TestCase):
    '''Test simple storage of some articles within_registry as well as their recovery from th_registry'''

    def setUp(self):
        init_registry()
        self.article_data   = []
        random.seed()
        self.categories     = [random_string(random.randint(0, 40)) for i in range(NUMBER_OF_CATEGORIES)]
        _logger.debug('Created categories: ' + '   '.join(self.categories))
        no_articles         = random.randint(0, MAX_NO_ARTICLES)
        _logger.debug('Creating ' + str(no_articles) + ' articles')
        self.article_data   = [[random_name(), random_heading(),
            random_timestamp(), 
            random_categories(self.categories)] 
            for i in range(no_articles)]

    def test_insert(self):
        _logger.debug(self.article_data)
        for i in range(NO_NEGATIVE_ARTICLE_CHECKS):
            self.assertTrue(test_false_article_name(self.article_data))
        _logger.debug("Registry seems to be empty")
        for article_info in self.article_data:
            self.assertTrue(insert_article(article_info))
            self.assertTrue(test_false_article_name(self.article_data))
            self.assertTrue(test_article_name(article_info))


if __name__ == '__main__':
    unittest.main()
    dispose_registry()

