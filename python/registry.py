#!/usr/bin/python
import os.path
import sys

PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import article
from naga_config import *
import nagaUtils
from logger import log


class Registry:

    def __init__(self, directory_path = REGISTRY_PATH, file_name = 'registry.csv' ):
        self.articles       = []
        self.SEPARATOR      = ';'
        self.directory_path = directory_path
        self.file_name      = self.directory_path + os.sep + file_name
        self.from_file()
    
    def from_file(self, file_name = None):
        '''Load registry file'''
        if file_name != None:
            self.file_name = file_name
        self.articles = []
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

    def get(self, key):
        '''Get full article for a given file name'''
        if key in self.articles:
            article = self._load_file(key)
            return self.articles[key]
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
        if key in self.articles.keys():
            value = self.articles[key]
        self.articles[key] = article
        self.__write_file(key)
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



if __name__ == '__main__':
    print "Ok"
