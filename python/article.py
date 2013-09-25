import datetime
import StringIO
import os.path
import sys
import xml.etree.ElementTree as ET
import logging

PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import nagaUtils
#------------------------------------------------------------------------------
TAG_ARTICLE_ROOT = 'michael.josef.beer.article'
TAG_HEADING      = 'heading'
TAG_SUMMARY      = 'summary'
TAG_CONTENT      = 'content'
TAG_CATEGORIES   = 'categories'
TAG_CATEGORY     = 'category'
TAG_TIMESTAMP    = 'timestamp'
#------------------------------------------------------------------------------
_logger = logging.getLogger('article')
#------------------------------------------------------------------------------
def article_from_xml(article_xml):
    '''
    Create article from XML description
    '''

    def parse_categories(categories_node):
        _logger.debug("parse_categories: Got node "  + categories_node.tag)
        new_categories = []
        for node in categories_node:
            _logger.debug("parse_categories: Got node "  + node.tag)
            if node.tag == TAG_CATEGORY:
                new_categories.append(node.text)
        return new_categories

    def parse_article_root(root_node):
        _logger.debug("parse_article_root: Got node "  + root_node.tag)
        new_article = Article()
        for node in root_node:
            _logger.debug("parse_article_root: Got node "  + node.tag)
            if node.tag == TAG_HEADING:
                new_article.set_heading(node.text)
            if node.tag == TAG_SUMMARY:
                new_article.set_summary(node.text)
            if node.tag == TAG_CONTENT:
                new_article.set_content(node.text)
            if node.tag == TAG_TIMESTAMP:
                new_article.set_timestamp(node.text)
            if node.tag == TAG_CATEGORIES:
                new_categories = parse_categories(node)
                new_article.set_categories(new_categories)
        _logger.debug("Loaded ")
        _logger.debug(new_article.to_xml())
        return new_article
    
    _logger.debug("article_from_xml: Got " + article_xml)
    xml_tree = ET.fromstring(article_xml)
    return parse_article_root(xml_tree)
#------------------------------------------------------------------------------    
class Article:

    def __init__(self):
        self.timestamp  = nagaUtils.get_timestamp_now()
        self.heading    = ''
        self.summary    = ''
        self.content    = ''
        self.categories = []

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        old_timestamp = self.timestamp
        self.timestamp = timestamp
        return old_timestamp

    def get_heading(self):
        return self.heading

    def set_heading(self, heading):
        old_heading = self.heading
        self.heading = heading
        return old_heading

    def get_summary(self):
        return self.summary

    def set_summary(self, summary):
        old_summary = self.summary
        self.summary = summary
        return old_summary

    
    def get_content(self):
        return self.content

    def set_content(self, content):
        old_content = self.content
        self.content = content
        return old_content

    def get_categories(self):
        return self.categories

    def set_categories(self, categories):
        old_categories = self.categories
        self.categories = categories
        return old_categories

    def to_xml(self):
        xml_tree           = ET.Element(TAG_ARTICLE_ROOT)
        xml_timestamp      = ET.SubElement(xml_tree, TAG_TIMESTAMP)
        xml_timestamp.text = self.timestamp
        xml_heading        = ET.SubElement(xml_tree, TAG_HEADING)
        xml_heading.text   = self.heading
        xml_summary        = ET.SubElement(xml_tree, TAG_SUMMARY)
        xml_summary.text   = self.summary
        xml_content        = ET.SubElement(xml_tree, TAG_CONTENT)
        xml_content.text   = self.content
        xml_categories     = ET.SubElement(xml_tree, TAG_CATEGORIES)
        for category in self.categories:
            xml_category   = ET.SubElement(xml_categories, TAG_CATEGORY)
            xml_category.text = category
        return ET.tostring(xml_tree)

    def matches(self, criterion):
        point     = criterion[0]
        ref_value = criterion[1]
        if point ==  'heading':
            return self.get_heading() == ref_value
        if point == 'timestamp':
            return self.get_timestamp() == ref_value
        if point == 'category':
            return ref_value in self.get_categories()
        return False

