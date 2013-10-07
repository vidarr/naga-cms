#!/usr/bin/python
import os.path
import sys
import logging
import cgi
import cgitb
#------------------------------------------------------------------------------
ABSOLUTE_PAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR         = 'python'
sys.path.append(ABSOLUTE_PAGE_ROOT + '/../' + MODULE_DIR)
from naga_config import *
import categories
#------------------------------------------------------------------------------
_logger         = logging.getLogger('get.py')
ITEM_TAG        = 'item'
_item_open_tag  = '<'  + ITEM_TAG + '>'
_item_close_tag = '</' + ITEM_TAG + '>'
#------------------------------------------------------------------------------
def wrap_items(items):
    if not type(items) == type([]):
        _logger.error('wrap_items: Wrong argument' + str(items))
        return None
    _logger.debug(''.join(items))
    if len(items) > 0:
        wrapped_items = _item_open_tag + \
                (_item_close_tag + _item_open_tag).join(items) + \
                _item_close_tag
    else:
        wrapped_items = ''
    return wrapped_items
#------------------------------------------------------------------------------
def get_categories():
    return wrap_items(categories.get_categories().get_categories())
#------------------------------------------------------------------------------
def get_file_content(file_name):
    _logger.debug("Trying to open " + file_name)
    file_object = open(file_name)
    content     = file_object.read()
    file_object.close()
    return content
#------------------------------------------------------------------------------
def get_recent_news():
    return get_file_content(ABSOLUTE_PAGE_ROOT + PATH_SEPARATOR + '..' + \
            PATH_SEPARATOR + '..' + RSS_ROLLING_FEED_PATH)
#------------------------------------------------------------------------------
def get_news():
    return get_file_content(ABSOLUTE_PAGE_ROOT + PATH_SEPARATOR + '..' + \
            PATH_SEPARATOR + '..' + RSS_FEED_PATH)
#------------------------------------------------------------------------------
item_getter = {
        'categories'   : get_categories   ,
        'recent_news' : get_recent_news  ,
        'all_news'     : get_news
        }
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    cgitb.enable()
    form = cgi.FieldStorage()
    if not 'value' in form:
        content = 'Invalid argument'
    else:
        if not form['value'].value in item_getter:
            content = 'invalid argument'
        else:
            getter_func = item_getter[form['value'].value]
            content     = getter_func()
    print "Content-Type: text/xml\n\n"
    print content


