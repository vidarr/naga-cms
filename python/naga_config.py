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
RSS_FEED_PATH          = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR    + PATH_SEPARATOR + 'all-news.xml'
RSS_ROLLING_FEED_PATH  = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR    + PATH_SEPARATOR + 'news.xml'
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
#------------------------------------------------------------------------------
# CGI authentication names
#------------------------------------------------------------------------------
CREDENTIALS_USER       = 'user'
CREDENTIALS_PASSPHRASE = 'passphrase'
#------------------------------------------------------------------------------
HTTP_ARG_FILE_NAME     = 'file_name'
#------------------------------------------------------------------------------
UPDATE_LABEL           = '<b>Update:</b> '
#------------------------------------------------------------------------------
# Logger configuration
#------------------------------------------------------------------------------
logging.basicConfig(filename= NAGA_ABS_ROOT + PATH_SEPARATOR +
                    LOG_FILE_PATH,level=logging.DEBUG)
#------------------------------------------------------------------------------
# Internal Constants
#------------------------------------------------------------------------------
# ARTICLE_HTML_SHORT_HEADING   = 'article_short_heading'
ARTICLE_HTML_SHORT_TIMESTAMP = 'article_short_timestamp' 
