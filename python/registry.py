#!/usr/bin/python
import os.path
import sys
import logging

ABSOLUTE_PAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR         = 'python'
sys.path.append(ABSOLUTE_PAGE_ROOT + '/../' + MODULE_DIR);
import article
from naga_config import *
import nagaUtils

class Registry:

    def __init__(self, directory_path = REGISTRY_PATH, file_name = 'registry.csv' ):
        self.articles       = []
        self.SEPARATOR      = ';'
        self.directory_path = directory_path
        self.file_name      = self.directory_path + os.sep + file_name
        self.from_file()
        self.logger         = logging.getLogger("Registry")
    
    def from_file(self, file_name = None):
        '''Load registry file'''
        if file_name != None:
            self.file_name = file_name
        self.articles = {}
        file_object  = open(self.file_name, 'r')
        for line in file_object:
            file_content = line.split(self.SEPARATOR)
            if len(file_content) < 3:
                log(LOG_ERROR, "Registry.from_file: " + file_name +
                    " does not seem to have proper registry format in line " + line)
                return
            key, heading, timestamp = line
            article = Article()
            article.set_heading(heading)
            article.set_timestamp(timestamp)
            sef.articles[key] = article
        file_object.close()

    def save(self):
        '''Save registry to registry file'''
        file_object = open(self.file_name, 'w')
        for key in self.articles.keys():
            file_object.write(key)
            file_object.write(self.SEPARATOR)
            file_object.write(article.get_heading())
            file_object.write(self.SEPARATOR)
            file_object.write(article.get_timestamp())
            for category in article.get_categories():
                file_object.write(self.SEPARATOR)
                file_object.write(category)
        file_object.close()

    def get_article_keys(self):
        return self.articles.keys()

    def get(self, key):
        '''Get full article for a given file name'''
        self.logger.debug("get: About to get " + key)
        self.logger.debug(self.articles.keys())
        if key in self.articles.keys():
            return article.article_from_xml(self._load_file(key))
        return None

    def get_xml(self, key):
        '''
        Get xml description of article for a given file name
        '''
        if key in self.articles.keys():
            return self._load_file(key)
        return None
            
    def remove(self, key):
        '''Remove an article from registry and delete the article file'''
        if key in self.articles.keys():
            value = self.articles[key]
            # Delete file
        else:
            value = None
        return value

    def add(self, key, article):
        '''Add new article to registry and save the article to file name'''
        value = None
        self.logger.debug("add: About to add " + key)
        self.logger.debug(self.articles.keys())
        if key in self.articles.keys():
            value = self.articles[key]
        self.articles[key] = article
        self.logger.debug("add: Added " + key)
        self.logger.debug(self.articles.keys())
        self._write_file(key)
        return value

    def find(self, criteria):
        '''Return all file names that match articles satisfying the given criteria'''
        found_articles = self.articles.keys()
        for criterion in criteria:
            found_articles = self._match(found_articles, criterion)
        return found_articles

    def _match(self, articles, criterion):
        found_articles = []
        for key in articles:
            article = self.articles[key]
            if article.matches(article, criterion) == True:
                found_articles.append(key)
        return found_articles

    def _write_file(self, key):
        if not key in self.articles:
            self.logger.debug("Registry._write_file: No article under key " + key)
            return None
        article_object = self.articles[key]
        article_path   = self.directory_path + PATH_SEPARATOR + key
        file_object    = open(article_path, 'w')
        file_object.write(article_object.to_xml())
        file_object.close()
        self.logger.debug("Registry._write_file: Wrote " + article_path)

    def _load_file(self, key):
        article_path = self.directory_path + PATH_SEPARATOR + key
        file_object  = open(article_path, 'r')
        article_data = file_object.read()
        file_object.close()
        self.logger.debug("Registry._load_file: Loaded " + article_path)
        return article_data


if __name__ == '__main__':
    print "Ok"

