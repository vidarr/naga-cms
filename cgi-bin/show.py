#!/usr/bin/python3
import os.path
import sys
import logging
import cgi
import cgitb
import urllib.request
#------------------------------------------------------------------------------
ABSOLUTE_PAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ABSOLUTE_PAGE_ROOT = ABSOLUTE_PAGE_ROOT + '/..'
MODULE_DIR         = 'python'
sys.path.append(ABSOLUTE_PAGE_ROOT + '/' + MODULE_DIR)
from naga_config import *
from security    import sanitize_string
from page        import Page
from rss         import Rss
import registry
import statics
#------------------------------------------------------------------------------
_logger            = logging.getLogger('show.py')
_page              = Page()
#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------
def finish_page():
    print(_page.get_html())
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
    sys.exit(1)
#------------------------------------------------------------------------------
def show_news(content):
    _logger.info("show_rss: Requested " + content)
    if content == 'all':
        file_name = NAGA_ABS_ROOT + PATH_SEPARATOR +RSS_ROLLING_FEED_PATH
    elif content == 'latest':
        file_name = NAGA_ABS_ROOT + PATH_SEPARATOR + RSS_FEED_PATH
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
    article_registry = registry.Registry()
    if not content in article_registry.get_article_keys():
        show_error(content + " not found")
    article_object = article_registry.get(content)
    _page.set_content(article_object.to_html())
    finish_page()
#------------------------------------------------------------------------------
def show_category(content):
    if not content:
        show_error("No category to show given")
    _logger.info('show_category: Requested ' + content)
    criteria = [['category', content]]
    article_registry = registry.Registry()
    articles = article_registry.find(criteria)
    if len(articles) < 1:
        _page.set_content("<p>No articles found</p>")
    else:
        html = []
        for article_key in articles:
            article = article_registry.get(article_key)
            html.append('<a href="') 
            html.append(NAGA_ROOT + PATH_SEPARATOR + SHOW_RELATIVE_PATH)
            html.append('?type=article&content=') 
            html.append(article_key)
            html.append('">') 
            html.append(article.to_html_short())
            html.append('</a>')
        html_string = u''.join(html)
        _page.set_content(html_string)
    finish_page()
#------------------------------------------------------------------------------
def show_url(content):
    if not content:
        show_error("No content given")
    remote_file = urllib.request.urlopen(content)
    if not remote_file:
        show_error("Got None for url " + content)
    remote_data = remote_file.readlines()
    remote_file.close()
    _page.set_content(u''.join(map(
        lambda item: item.decode(ENCODING),
        remote_data)))
    finish_page()
#------------------------------------------------------------------------------
def show_static(content):
    if not content:
        show_error("show_static: No static key given")
    static_object = statics.Statics()
    url           = static_object.get(content)
    show_url(url)
#------------------------------------------------------------------------------
_content_types = {
        'error'    : show_error,
        'news'     : show_news,
        'article'  : show_article,
        'category' : show_category,
        'static'   : show_static,
        'url'      : show_url
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
    #    content = sanitize_string(content)
    content_handler(content)

