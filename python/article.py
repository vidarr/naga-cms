#!/usr/bin/python3
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
import datetime
import os.path
import sys
import xml.etree.ElementTree as ET
import logging
import re
#------------------------------------------------------------------------------
PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import nagaUtils
import transformator
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
def heading_2_file_name(heading):
    file_name = re.sub('[^a-zA-Z0-9]', '', heading)
    return file_name.lower()
#------------------------------------------------------------------------------
def get_edit_links_html(file_name):
    '''Return HTML links to edit / delete pages '''
    return ''.join(['[ <a href="', EDIT_ARTICLE_LINK, '?file_name=',
        file_name, '">edit</a> ]'])
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
    #---------------------------------------------------------------------------
    def __init__(self, html_transformator =
            transformator.make_default_transformator()):
        self.timestamp  = nagaUtils.get_timestamp_now()
        self.heading    = ''
        self.summary    = ''
        self.content    = ''
        self.article_key = ''
        self.categories = []
        self.logger     = logging.getLogger('Article')
        self.html_transformator = html_transformator
    #---------------------------------------------------------------------------
    def get_timestamp(self):
        return self.timestamp
    #---------------------------------------------------------------------------
    def set_timestamp(self, timestamp):
        old_timestamp = self.timestamp
        self.timestamp = timestamp
        return old_timestamp
    #---------------------------------------------------------------------------
    def get_heading(self):
        return self.heading
    #---------------------------------------------------------------------------
    def set_heading(self, heading):
        old_heading = self.heading
        self.heading = heading
        return old_heading
    #---------------------------------------------------------------------------
    def get_summary(self):
        return self.summary
    #---------------------------------------------------------------------------
    def get_html_summary(self):
        return self.html_transformator.transform(self.summary)
    #---------------------------------------------------------------------------
    def set_summary(self, summary):
        old_summary = self.summary
        self.summary = summary
        return old_summary
    #---------------------------------------------------------------------------
    def get_content(self):
        return self.content
    #---------------------------------------------------------------------------
    def get_html_content(self):
        return self.html_transformator.transform(self.content)
    #---------------------------------------------------------------------------
    def set_content(self, content):
        old_content = self.content
        self.content = content
        return old_content
    #---------------------------------------------------------------------------
    def get_categories(self):
        return self.categories
    #---------------------------------------------------------------------------
    def set_categories(self, categories):
        old_categories = self.categories
        self.categories = categories
        return old_categories
    #---------------------------------------------------------------------------
    def set_key(self, key):
        self.logger.error("set_key: setting " + key)
        self.article_key = key
    #---------------------------------------------------------------------------
    def get_key(self):
        self.logger.error("get_key: " + self.article_key)
        return self.article_key
    #---------------------------------------------------------------------------
    def _to_xml_tree_short(self):
        '''
        Generate short article description as xml tree
        '''
        xml_tree           = ET.Element(TAG_ARTICLE_ROOT)
        xml_timestamp      = ET.SubElement(xml_tree, TAG_TIMESTAMP)
        xml_timestamp.text = self.timestamp
        xml_heading        = ET.SubElement(xml_tree, TAG_HEADING)
        xml_heading.text   = self.heading
        xml_summary        = ET.SubElement(xml_tree, TAG_SUMMARY)
        xml_summary.text   = self.summary
        return xml_tree
    #---------------------------------------------------------------------------
    def to_xml(self):
        '''
        Generate long article description as xml (including actual content and
        categories)
        '''
        xml_tree           = self._to_xml_tree_short()
        xml_content        = ET.SubElement(xml_tree, TAG_CONTENT)
        xml_content.text   = self.content
        xml_categories     = ET.SubElement(xml_tree, TAG_CATEGORIES)
        for category in self.categories:
            xml_category   = ET.SubElement(xml_categories, TAG_CATEGORY)
            xml_category.text = category
        return ET.tostring(xml_tree, encoding = ENCODING)
    #---------------------------------------------------------------------------
    def to_xml_short(self):
        '''
        Return short article description as xml (excluding actual content and
        categories)
        '''
        return ET.tostring(self._to_xml_tree_short(), encoding = ENCODING)
    #---------------------------------------------------------------------------
    def to_html(self):
        '''
        Return article description as html
        '''
        html = ['<p class="article_heading">',
                self.get_heading(),
                '</p><p class="article_timestamp">',
                self.get_timestamp(),
                '</p><p class="article_summary">',
                self.get_html_summary(),
                '</p><p class="article_content">',
                self.get_html_content(),'</p>']
        html_string = ''.join(html)
        return html_string
    #---------------------------------------------------------------------------
    def to_html_short(self):
        '''
        Return article short description as html
        '''
        html = ['<p class="article_short_heading">', 
                self.get_heading() ,
                '</p><p class="article_short_timestamp">', 
                self.get_timestamp(), '</p>'] 
        html_string = ''.join(html)
        return html_string
    #---------------------------------------------------------------------------
    def matches(self, criterion):
        point     = criterion[0]
        ref_value = criterion[1]
        self.logger.debug("matches: point = " + point + " ref_value = " +
                ref_value)
        if point ==  'heading':
            return self.get_heading() == ref_value
        if point == 'timestamp':
            return self.get_timestamp() == ref_value
        if point == 'category':
            self.logger.debug("matches: " + ref_value + " in " +
                    str(self.get_categories()))
            return ref_value in self.get_categories()
        return False

