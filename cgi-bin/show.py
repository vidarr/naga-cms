#!/usr/bin/python
import os.path
import sys
import logging
import cgi
import cgitb
#------------------------------------------------------------------------------
ABSOLUTE_PAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ABSOLUTE_PAGE_ROOT = ABSOLUTE_PAGE_ROOT + '/..'
MODULE_DIR         = 'python'
sys.path.append(ABSOLUTE_PAGE_ROOT + '/' + MODULE_DIR)
from naga_config import *
from security    import sanitize_string
from page        import Page
from rss         import Rss
#------------------------------------------------------------------------------
_logger            = logging.getLogger('show.py')
_page              = Page()
#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------
def finish_page():
    print "Content-Type: text/html\n\n"
    print _page.get_html()
    sys.exit(0)
#------------------------------------------------------------------------------
# Content Handlers
#------------------------------------------------------------------------------
def show_error(message):
    _logger.error(message)
    _page.set_content('''
<h1>Error occured</h1>
<p>
''' + message + '''
</p>''')
    finish_page()
#------------------------------------------------------------------------------
def show_news(content):
    _logger.info("show_rss: Requested " + content)
    if content == 'all':
        file_name = ABSOLUTE_PAGE_ROOT + PATH_SEPARATOR + '..' + PATH_SEPARATOR +RSS_ROLLING_FEED_PATH
    elif content == 'latest':
        file_name = ABSOLUTE_PAGE_ROOT + PATH_SEPARATOR + '..' + PATH_SEPARATOR + RSS_FEED_PATH
    else:
        show_error("Wrong rss info requested")
    rss = Rss(file_name)
    _logger.info(rss)
    _logger.info(_page)
    _page.set_content(rss.to_html())
    finish_page()
#------------------------------------------------------------------------------
def show_article(content):
    _logger.info('show_article: Requested ' + content)
#------------------------------------------------------------------------------
_content_types = {
        'error' : show_error,
        'news'   : show_news
        }
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    cgitb.enable()
    form = cgi.FieldStorage()
    if not 'type' in form:
        show_error('Invalid argument given to show.py')
    content_type = form['type'].value
    if not content_type in _content_types:
        show_error("Invalid content type requested")
    content_handler = _content_types[content_type]
    if not 'content' in form:
        show_error('Invalid argument given to show.py')
    content = form['content'].value
    content = sanitize_string(content)
    content_handler(content)

