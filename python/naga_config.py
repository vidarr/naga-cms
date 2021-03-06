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
NAGA_ROOT              = 'https://192.168.10.100'
NAGA_ABS_ROOT          = '/var/www'
PAGE_TITLE             = "Michael J. Beer"
PAGE_DESCRIPTION       = "Michael Beer's personal homepage"
COPYRIGHT              = '&copy;2013 <a href="mailto:michael@ubeer.org">Michael J. Beer</a>'
ENCODING               = "UTF-8"
PAGE_ROOT              = ''
LOG_DIR                = 'log'
CONTENT_DIR            = 'content'
FORMATTING_DIR         = 'formatting'
IMAGE_DIR              = 'images'
FILE_DIR               = 'files'
ETC_DIR                = 'etc'
SCRIPT_DIR             = 'wsgi'
STATIC_DIR             = 'static'
JAVASCRIPT_DIR         = 'javascript'
SCRIPT_PATH               = join(NAGA_ROOT, SCRIPT_DIR)
SCRIPT_SHOW_PATH          = join(SCRIPT_PATH, 'show.py')
LOG_FILE_PATH          = join(PAGE_ROOT, LOG_DIR    , 'naga.log')
RSS_ICON_PATH          = join(NAGA_ROOT, IMAGE_DIR  , 'feed_icon.svg')
RSS_FEED_PATH          = join(PAGE_ROOT, CONTENT_DIR)
RSS_FEED_LINK          = join(NAGA_ROOT, CONTENT_DIR)
RSS_ALL_FEED_NAME      = 'all-news'
RSS_ROLLING_FEED_NAME  = 'news'
RSS_ROLLING_ENTRIES    = 10
CATEGORIES_FILE_PATH   = join(PAGE_ROOT, ETC_DIR       , 'categories')
USERS_FILE_PATH        = join(PAGE_ROOT, ETC_DIR       , 'users')
CSS_PATH               = join(PATH_SEPARATOR, PAGE_ROOT, FORMATTING_DIR, 'general.css')
CSS_ARTICLE_PATH       = join(PATH_SEPARATOR, PAGE_ROOT, FORMATTING_DIR, 'article.css')
CSS_RSS_PATH       = join(PATH_SEPARATOR, PAGE_ROOT, FORMATTING_DIR, 'rss.css')
CSS_POST_PATH          = join(NAGA_ROOT, FORMATTING_DIR, 'post.css')
UPLOAD_PATH            = join(SCRIPT_PATH, 'upload.py')
UPLOAD_FILE_PATH       = join(PAGE_ROOT, SCRIPT_DIR       , 'upload_file.py') 
SHOW_RELATIVE_PATH     = join(SCRIPT_DIR   , 'show.py')
REGISTRY_PATH          = join(PAGE_ROOT , CONTENT_DIR)
CONTENT_PATH           = join(PAGE_ROOT , CONTENT_DIR)
STATIC_PATH            = join(PAGE_ROOT , STATIC_DIR)
STATIC_FILE_PATH       = join(PAGE_ROOT , ETC_DIR, 'static')
AUTHENTICATE_LINK      = join(SCRIPT_PATH  , 'authenticate.py')
CHOOSE_UPLOAD_LINK     = join(SCRIPT_PATH  , 'choose_upload.py')
LOGOUT_LINK            = join(SCRIPT_PATH  , 'logout.py')
ADD_ARTICLE_LINK       = join(SCRIPT_PATH  , 'post.py')
EDIT_ARTICLE_LINK      = ADD_ARTICLE_LINK
JAVASCRIPT_URL         = join(PATH_SEPARATOR, PAGE_ROOT, JAVASCRIPT_DIR)
JAVASCRIPT_DEFAULT_FILE = "general.js"
FAV_ICON_PATH          = join(NAGA_ROOT, IMAGE_DIR  , 'favicon.png')
MENU_IMAGE_PATH        = join(NAGA_ROOT, IMAGE_DIR, 'menu.png') 
#------------------------------------------------------------------------------
# authentication keys
#------------------------------------------------------------------------------
CREDENTIALS_COOKIE      = 'credentials'
CREDENTIALS_USER       = 'user'
CREDENTIALS_PASSPHRASE = 'passphrase'
#------------------------------------------------------------------------------
HTTP_ARG_FILE_NAME     = 'file_name'
XML_FILE_EXTENSION     = 'xml'
RSS_FILE_EXTENSION     = 'rss'
#------------------------------------------------------------------------------
IMAGE_OPTIONS          = 'height="240" width="320"'
IMAGE_OPTIONS          = 'width="320"'
#------------------------------------------------------------------------------
UPDATE_LABEL_START     = '<b>Update:</b> '
#------------------------------------------------------------------------------
STORE_TYPE_FILE        = 'file'
STORE_TYPE_IMAGE       = 'image'
STORE_FILE_PATH        = FILE_DIR
STORE_IMAGE_PATH       = IMAGE_DIR
#------------------------------------------------------------------------------
# Logger configuration
#------------------------------------------------------------------------------
logging.basicConfig(filename=join(NAGA_ABS_ROOT, LOG_FILE_PATH), \
        format='%(asctime)s - %(levelname)s - %(filename)s %(message)s', \
        level=logging.DEBUG)
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
__logger.debug("SCRIPT_DIR=" + SCRIPT_DIR)
__logger.debug("STATIC_DIR=" + STATIC_DIR)
__logger.debug("SCRIPT_PATH=" + SCRIPT_PATH)
__logger.debug("SCRIPT_SHOW_PATH=" + SCRIPT_SHOW_PATH)
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
__logger.debug("CHOOSE_UPLOAD_LINK=" + CHOOSE_UPLOAD_LINK)
__logger.debug("AUTHENTICATE_LINK=" + AUTHENTICATE_LINK)
__logger.debug("LOGOUT_LINK=" + LOGOUT_LINK)
__logger.debug("ADD_ARTICLE_LINK=" + ADD_ARTICLE_LINK)
__logger.debug("EDIT_ARTICLE_LINK=" + EDIT_ARTICLE_LINK)
#------------------------------------------------------------------------------
# Internal Constants
#------------------------------------------------------------------------------
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
