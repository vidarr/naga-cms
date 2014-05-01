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
from os.path import join
import sys
import logging
#------------------------------------------------------------------------------
__logger = logging.getLogger('naga_config')
#------------------------------------------------------------------------------
# General constants
#------------------------------------------------------------------------------
LINEBREAK              = "\n"
CFG_LIST_SEPARATOR     = ','
PATH_SEPARATOR         = '/'
#------------------------------------------------------------------------------
# Actual configuration
#------------------------------------------------------------------------------
NAGA_ROOT              = 'https://localhost/naga'
NAGA_ABS_ROOT          = '/var/www'
PAGE_TITLE             = "Michael J. Beer"
COPYRIGHT              = '&copy;2013 <a href="mailto:michael@ubeer.org">Michael J. Beer</a>'
ENCODING               = "UTF-8"
PAGE_ROOT              = 'naga'
LOG_DIR                = 'log'
CONTENT_DIR            = 'content'
FORMATTING_DIR         = 'formatting'
IMAGE_DIR              = 'images'
FILE_DIR               = 'files'
ETC_DIR                = 'etc'
CGI_DIR                = 'cgi-bin'
STATIC_DIR             = 'static'
JAVASCRIPT_DIR         = 'javascript'
CGI_PATH               = join(NAGA_ROOT, CGI_DIR)
CGI_SHOW_PATH          = join(CGI_PATH, 'show.py')
LOG_FILE_PATH          = join(PAGE_ROOT, LOG_DIR    , 'naga.log')
RSS_ICON_PATH          = join(NAGA_ROOT, IMAGE_DIR  , 'feed_icon.svg')
RSS_FEED_PATH          = join(PAGE_ROOT, CONTENT_DIR)
RSS_ALL_FEED_NAME      = 'all-news'
RSS_ROLLING_FEED_NAME  = 'news'
RSS_ROLLING_ENTRIES    = 10
CATEGORIES_FILE_PATH   = join(PAGE_ROOT, ETC_DIR       , 'categories')
USERS_FILE_PATH        = join(PAGE_ROOT, ETC_DIR       , 'users')
CSS_PATH               = join(PATH_SEPARATOR, PAGE_ROOT, FORMATTING_DIR, 'general.css')
CSS_POST_PATH          = join(PAGE_ROOT, FORMATTING_DIR, 'post.css')
UPLOAD_PATH            = join(PAGE_ROOT, CGI_DIR       , 'upload.py')
UPLOAD_FILE_PATH       = join(PAGE_ROOT, CGI_DIR       , 'upload_file.py') 
SHOW_RELATIVE_PATH     = join(CGI_DIR   , 'show.py')
REGISTRY_PATH          = join(PAGE_ROOT , CONTENT_DIR)
CONTENT_PATH           = join(PAGE_ROOT , CONTENT_DIR)
STATIC_PATH            = join(PAGE_ROOT , STATIC_DIR)
STATIC_FILE_PATH       = join(PAGE_ROOT , ETC_DIR, 'static')
AUTHENTICATE_LINK      = join(CGI_PATH  , 'authenticate.py')
LOGOUT_PATH            = join(CGI_PATH  , 'logout.py')
ADD_ARTICLE_PATH       = join(CGI_PATH  , 'post.py')
EDIT_ARTICLE_PATH      = ADD_ARTICLE_PATH
JAVASCRIPT_URL         = join(PATH_SEPARATOR, PAGE_ROOT, JAVASCRIPT_DIR)
#------------------------------------------------------------------------------
# CGI authentication names
#------------------------------------------------------------------------------
CREDENTIALS_USER       = 'user'
CREDENTIALS_PASSPHRASE = 'passphrase'
#------------------------------------------------------------------------------
HTTP_ARG_FILE_NAME     = 'file_name'
XML_FILE_EXTENSION     = 'xml'
RSS_FILE_EXTENSION     = 'rss'
#------------------------------------------------------------------------------
IMAGE_OPTIONS          = 'height="240" width="320"'
#------------------------------------------------------------------------------
UPDATE_LABEL           = '<b>Update:</b> '
#------------------------------------------------------------------------------
STORE_TYPE_FILE        = 'file'
STORE_TYPE_IMAGE       = 'image'
STORE_FILE_PATH        = FILE_DIR
STORE_IMAGE_PATH       = IMAGE_DIR
#------------------------------------------------------------------------------
# Logger configuration
#------------------------------------------------------------------------------
logging.basicConfig(filename=join(NAGA_ABS_ROOT, LOG_FILE_PATH),level=logging.DEBUG)
#------------------------------------------------------------------------------
__logger.debug("NAGA_ROOT=" + NAGA_ROOT)
__logger.debug("NAGA_ABS_ROOT=" + NAGA_ABS_ROOT)
__logger.debug("PAGE_TITLE=" + PAGE_TITLE)
__logger.debug("COPYRIGHT=" + COPYRIGHT)
__logger.debug("ENCODING=" + ENCODING)
__logger.debug("PAGE_ROOT=" + PAGE_ROOT)
__logger.debug("LOG_DIR=" + LOG_DIR)
__logger.debug("CONTENT_DIR=" + CONTENT_DIR)
__logger.debug("FORMATTING_DIR=" + FORMATTING_DIR)
__logger.debug("IMAGE_DIR=" + IMAGE_DIR)
__logger.debug("FILE_DIR=" + FILE_DIR)
__logger.debug("ETC_DIR=" + ETC_DIR)
__logger.debug("CGI_DIR=" + CGI_DIR)
__logger.debug("STATIC_DIR=" + STATIC_DIR)
__logger.debug("CGI_PATH=" + CGI_PATH)
__logger.debug("CGI_SHOW_PATH=" + CGI_SHOW_PATH)
__logger.debug("LOG_FILE_PATH=" + LOG_FILE_PATH)
__logger.debug("RSS_ICON_PATH=" + RSS_ICON_PATH)
__logger.debug("RSS_FEED_PATH=" + RSS_FEED_PATH)
__logger.debug("RSS_ALL_FEED_NAME=" + RSS_ALL_FEED_NAME)
__logger.debug("RSS_ROLLING_FEED_NAME=" + RSS_ROLLING_FEED_NAME)
__logger.debug("RSS_ROLLING_ENTRIES=" + str(RSS_ROLLING_ENTRIES))
__logger.debug("CATEGORIES_FILE_PATH=" + CATEGORIES_FILE_PATH)
__logger.debug("USERS_FILE_PATH=" + USERS_FILE_PATH)
__logger.debug("CSS_PATH=" + CSS_PATH)
__logger.debug("CSS_POST_PATH=" + CSS_POST_PATH)
__logger.debug("UPLOAD_PATH=" + UPLOAD_PATH)
__logger.debug("UPLOAD_FILE_PATH=" + UPLOAD_FILE_PATH)
__logger.debug("SHOW_RELATIVE_PATH=" + SHOW_RELATIVE_PATH)
__logger.debug("REGISTRY_PATH=" + REGISTRY_PATH)
__logger.debug("CONTENT_PATH=" + CONTENT_PATH)
__logger.debug("STATIC_PATH=" + STATIC_PATH)
__logger.debug("STATIC_FILE_PATH=" + STATIC_FILE_PATH)
__logger.debug("AUTHENTICATE_LINK=" + AUTHENTICATE_LINK)
__logger.debug("LOGOUT_PATH=" + LOGOUT_PATH)
__logger.debug("ADD_ARTICLE_PATH=" + ADD_ARTICLE_PATH)
__logger.debug("EDIT_ARTICLE_PATH=" + EDIT_ARTICLE_PATH)
#------------------------------------------------------------------------------
# Internal Constants
#------------------------------------------------------------------------------
# ARTICLE_HTML_SHORT_HEADING   = 'article_short_heading'
ARTICLE_HTML_SHORT_TIMESTAMP   = 'article_short_timestamp'
ARTICLE_HTML_SHORT_DESCRIPTION = 'article_short_description'
SORT_KEY_HEADING               = 'heading'
SORT_KEY_TIMESTAMP             = 'timestamp'
#------------------------------------------------------------------------------
# Markup constants
#------------------------------------------------------------------------------
MARKUP_LINK_SEPARATOR = ' '
#------------------------------------------------------------------------------
HTML_HEADER = '''
<!DOCTYPE HTML>
<html>
'''
HTML_FOOTER = '''
</html>
'''
