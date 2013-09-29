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
PAGE_ROOT              = PATH_SEPARATOR + 'naga'
LOG_DIR                = 'log'
CONTENT_DIR            = 'content'
FORMATTING_DIR         = 'formatting'
IMAGE_DIR              = 'images'
ETC_DIR                = 'etc'
CGI_DIR                = 'cgi-bin'
LOG_FILE_PATH          = PAGE_ROOT + PATH_SEPARATOR + LOG_DIR        + PATH_SEPARATOR + 'naga.log'
RSS_ICON_PATH          = PAGE_ROOT + PATH_SEPARATOR + IMAGE_DIR      + PATH_SEPARATOR + 'feed_icon.svg'
RSS_FEED_PATH          = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR    + PATH_SEPARATOR + 'all-news.xml'
RSS_ROLLING_FEED_PATH  = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR    + PATH_SEPARATOR + 'news.xml'
RSS_ROLLING_ENTRIES    = 10
CATEGORIES_FILE_PATH   = PAGE_ROOT + PATH_SEPARATOR + ETC_DIR        + PATH_SEPARATOR + 'categories'
CSS_POST_PATH          = PAGE_ROOT + PATH_SEPARATOR + FORMATTING_DIR + PATH_SEPARATOR + 'post.css'
UPLOAD_PATH            = PAGE_ROOT + PATH_SEPARATOR + CGI_DIR        + PATH_SEPARATOR + 'upload.py'
REGISTRY_PATH          = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR 
CONTENT_PATH           = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR 
#------------------------------------------------------------------------------
# Logger configuration
#------------------------------------------------------------------------------
logging.basicConfig(filename='..' + PATH_SEPARATOR + '..' + PATH_SEPARATOR +
                    LOG_FILE_PATH,level=logging.DEBUG)

