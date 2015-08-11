# -*- coding: UTF-8 -*-
#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2013, 2014, 2015 
#                  Michael J. Beer <michael.josef.beer@googlemail.com>
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
import urllib.request
from cgi import parse_qs, escape
#------------------------------------------------------------------------------
ABSOLUTE_PAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ABSOLUTE_PAGE_ROOT = ABSOLUTE_PAGE_ROOT + '/..'
MODULE_DIR         = 'python'
sys.path.append(ABSOLUTE_PAGE_ROOT + '/' + MODULE_DIR)
from naga_config import *
from security    import sanitize_string, authenticate_cookie
from page        import Page
from rss         import Rss
from article     import get_edit_links_html
import nagaUtils
import registry
import statics
import naga_wsgi
from wsgi_hooks import ErrorCatchingHook
#------------------------------------------------------------------------------
_logger            = logging.getLogger('show.py')
_page              = None
_sortkey           = SORT_KEY_TIMESTAMP
#------------------------------------------------------------------------------
# Content Handlers
#------------------------------------------------------------------------------
def show_error(request, message):
    _logger.error(message)
    _page.set_content('''
<h1>Error occured</h1>
<p>
''' + message + '''
</p>''')
    return _page.get_html()
#------------------------------------------------------------------------------
def show_news(request, content):
    _logger.info("show_rss: Requested " + content)
    html = ['<h1>', PAGE_TITLE, '</h1>\r\n', PAGE_DESCRIPTION]
    if content == 'all':
        file_name = join(NAGA_ABS_ROOT, RSS_FEED_PATH, 
            ''.join([RSS_ROLLING_FEED_NAME, '.', RSS_FILE_EXTENSION]))
    elif content == 'latest':
        file_name = join(NAGA_ABS_ROOT, RSS_FEED_PATH, 
            ''.join([RSS_ALL_FEED_NAME, '.', RSS_FILE_EXTENSION]))
    else:
        show_error("Wrong rss info requested")
    rss = Rss(file_name)
    _logger.info(rss)
    _logger.info(_page)
    html.append(rss.to_html())
    html_string = ''.join(html)
    _page.set_content(html_string)
    return _page.get_html()
#------------------------------------------------------------------------------
def show_article(request, file_name):
    _logger.info('show_article: Requested ' + file_name)
    article_registry = registry.Registry()
    if not file_name in article_registry.get_article_keys():
        show_error(file_name + " not found")
    article_object = article_registry.get(file_name)
    edit_links = ''
    if authenticate_cookie(request):
        edit_links = get_edit_links_html(file_name)
    _page.add_css_link(CSS_ARTICLE_PATH)
    _page.set_content(edit_links + article_object.to_html())
    return _page.get_html()
#------------------------------------------------------------------------------
def sort_articles(articles, sort_key = SORT_KEY_HEADING):
    if sort_key == SORT_KEY_HEADING:
        sort_function = lambda x: x.get_heading()
    elif sort_key == SORT_KEY_TIMESTAMP:
        sort_function = lambda x: nagaUtils.to_posix_timestamp(x.get_timestamp())
    else:
        _logger.error("Invalid sort key given: " + sort_key)
        return None
    return sorted(articles, key = sort_function)
#------------------------------------------------------------------------------
def show_category(request, content):
    if not content:
        show_error("No category to show given")
    _logger.info('show_category: Requested ' + content)
    criteria = [['category', content]]
    article_registry = registry.Registry()
    articles = article_registry.find(criteria)
    if len(articles) < 1:
        _page.set_content("<p>No articles found</p>")
    else:
        html = ['<h1>', content, '</h1><p>All articles in category ', content, 
                '. <a href="', 
                RSS_FEED_LINK, PATH_SEPARATOR, 
                content, '.', RSS_FILE_EXTENSION, 
                '"><img src="', RSS_ICON_PATH, 
                '" height="18" width="18"/>Subscribe to ', content, 
                '</a></p>\r\n<table class="listing">']
        article_objects = []
        for article_key in articles:
            article = article_registry.get(article_key)
            if not article:
                _logger.error(article_key + ' not found')
            else:
                article_objects.append(article)
        articles_sorted = sort_articles(article_objects, _sortkey)
        for article in articles_sorted:
            html.extend([ 
                '<tr><td><div class="heading">', 
                '<a href="', NAGA_ROOT, PATH_SEPARATOR, SHOW_RELATIVE_PATH, 
                '?type=article&content=', article.get_key(), '">', 
                article.get_heading(), '</a>', '</div><div class="timestamp">', 
                article.get_timestamp(),
                '</div><div class="description"></div></td></tr>\r\n'])
        html.append("</table>\r\n")
        html_string = ''.join(html)
        _page.set_content(html_string)
    return _page.get_html()
#------------------------------------------------------------------------------
def show_url(request, content):
    if not content:
        show_error("No content given")
    remote_file = urllib.request.urlopen(content)
    if not remote_file:
        show_error("Got None for url " + content)
    remote_data = remote_file.readlines()
    remote_file.close()
    _page.set_content(''.join(map(
        lambda item: item.decode(ENCODING),
        remote_data)))
    return _page.get_html()
#------------------------------------------------------------------------------
def show_static(request, content):
    if not content:
        show_error("show_static: No static key given")
    static_object = statics.Statics()
    url           = static_object.get(content)
    return show_url(request, url)
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
def show( request, start_response):
    _logger.info("Python " + str(sys.version_info))
    _logger.info("Called show.py")
    global _page 
    _page = Page(request)
    (content_type, content, sortkey) = request.get_get_variables('type', 
            'content', 'sortkey')
    if sortkey:
        _sortkey = sortkey
        _logger.info("using sortkey " + _sortkey)
    if not content_type:
        response_body = show_error('Invalid argument given to show.py')
    else:
        _logger.info(content_type)
        if not content_type in _content_types:
            response_body = show_error("Invalid content type requested")
        content_handler = _content_types[content_type]
        if not content:
            show_error('Invalid argument given to show.py')
        else:
            _logger.info(content)
    response_body = content_handler(request, content)
    return naga_wsgi.create_response(start_response, response_body)
#------------------------------------------------------------------------------
def application(environ, start_response):
    request = naga_wsgi.Wsgi(environ)
    errorCatchingHook = ErrorCatchingHook(show)
    return  errorCatchingHook(request, start_response)
