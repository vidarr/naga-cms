import os.path
import sys

# Log-Levels
LOG_ERROR              = 0
LOG_WARNING            = 1
LOG_INFO               = 2
LOG_DEBUG              = 3

LINEBREAK              = "\n"
PATH_SEPARATOR         = '/'
CFG_LIST_SEPARATOR     = ','

# Actual configuration
PAGE_ROOT              = '/seite'
LOG_LEVEL              = LOG_DEBUG
LOG_DIR                = 'log'
LOG_FILE_PATH          = PAGE_ROOT + PATH_SEPARATOR + LOG_DIR + PATH_SEPARATOR + 'naga.log'
CONTENT_DIR            = 'content'
FORMATTING_DIR         = 'formatting'
IMAGE_DIR              = 'images'
ETC_DIR                = 'etc'
RSS_ICON_PATH          = PAGE_ROOT + PATH_SEPARATOR + IMAGE_DIR   + PATH_SEPARATOR + 'feed_icon.svg'
RSS_FEED_PATH          = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR + PATH_SEPARATOR + 'all-news.xml'
RSS_ROLLING_FEED_PATH  = PAGE_ROOT + PATH_SEPARATOR + CONTENT_DIR + PATH_SEPARATOR + 'news.xml'
RSS_ROLLING_ENTRIES    = 10
CATEGORIES_FILE_PATH   = PAGE_ROOT + PATH_SEPARATOR + ETC_DIR     + PATH_SEPARATOR + 'categories'


