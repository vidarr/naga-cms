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
import logging
#------------------------------------------------------------------------------
# General constants
#------------------------------------------------------------------------------
LINEBREAK              = "\n"
PATH_SEPARATOR         = os.sep
CFG_LIST_SEPARATOR     = ','
#------------------------------------------------------------------------------
# Actual configuration
#------------------------------------------------------------------------------
NAGA_ROOT              = 'https://localhost/naga'
NAGA_ABS_ROOT          = '/var/www'
PAGE_TITLE             = "Michael J. Beer"
COPYRIGHT              = '&copy;2013 <a href="mailto:michael@ubeer.org">Michael J. Beer</a>'
ENCODING               = "UTF-8"
PAGE_ROOT              = PATH_SEPARATOR + 'naga'
LOG_DIR                = 'log'
CONTENT_DIR            = 'content'
FORMATTING_DIR         = 'formatting'
IMAGE_DIR              = 'images'
ETC_DIR                = 'etc'
CGI_DIR                = 'cgi-bin'
STATIC_DIR             = 'static'
CGI_PATH               = PAGE_ROOT + PATH_SEPARATOR + CGI_DIR
CGI_SHOW_PATH          = CGI_PATH  + PATH_SEPARATOR + 'show.py'
LOG_FILE_PATH          = PAGE_ROOT + PATH_SEPARATOR + LOG_DIR        + PATH_SEPARATOR + 'naga.log'
RSS_ICON_PATH          = PAGE_ROOT + PATH_SEPARATOR + IMAGE_DIR      + PATH_SEPARATOR + 'feed_icon.svg'
RSS_FEED_PATH          = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR    + PATH_SEPARATOR
RSS_ALL_FEED_NAME      = 'all-news'
RSS_ROLLING_FEED_NAME  = 'news'
RSS_ROLLING_ENTRIES    = 10
CATEGORIES_FILE_PATH   = PAGE_ROOT + PATH_SEPARATOR + ETC_DIR        + PATH_SEPARATOR + 'categories'
USERS_FILE_PATH        = PAGE_ROOT + PATH_SEPARATOR + ETC_DIR        + PATH_SEPARATOR + 'users'
CSS_PATH               = PAGE_ROOT + PATH_SEPARATOR + FORMATTING_DIR + PATH_SEPARATOR + 'general.css'
CSS_POST_PATH          = PAGE_ROOT + PATH_SEPARATOR + FORMATTING_DIR + PATH_SEPARATOR + 'post.css'
UPLOAD_PATH            = PAGE_ROOT + PATH_SEPARATOR + CGI_DIR        + PATH_SEPARATOR + 'upload.py'
SHOW_RELATIVE_PATH     = CGI_DIR   + PATH_SEPARATOR + 'show.py'
REGISTRY_PATH          = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR
CONTENT_PATH           = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR
STATIC_PATH            = PAGE_ROOT + PATH_SEPARATOR + STATIC_DIR
STATIC_FILE_PATH       = PAGE_ROOT + PATH_SEPARATOR + ETC_DIR        + PATH_SEPARATOR + 'static'
AUTHENTICATE_LINK      = CGI_PATH  + PATH_SEPARATOR + 'authenticate.py'
LOGOUT_PATH            = CGI_PATH  + PATH_SEPARATOR + 'logout.py'
ADD_ARTICLE_PATH       = CGI_PATH  + PATH_SEPARATOR + 'post.py'
EDIT_ARTICLE_PATH      = ADD_ARTICLE_PATH
IMAGE_DIRECTORY        = 'images'
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
# Logger configuration
#------------------------------------------------------------------------------
logging.basicConfig(filename=NAGA_ABS_ROOT + PATH_SEPARATOR +
                 LOG_FILE_PATH,level=logging.DEBUG)
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
