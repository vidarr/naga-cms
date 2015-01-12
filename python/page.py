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
import os
import sys
#------------------------------------------------------------------------------
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
from security import authenticate_cookie
import categories
import statics
#------------------------------------------------------------------------------
def wrap(content, head = "<title>naga</title>", onload_body_function = None):
    result = ["Content-Type: text/html\n\n",
        '''<!DOCTYPE HTML>
<html>
    <head>
        <meta   charset="utf8">''', head, '''
    </head>
    <body''']
    if onload_body_function != None:
        result.extend([''' onload="''', onload_body_function, '"'])
    result.extend(['''>''', 
    content, '''
    </body>
</html>''']) 
    result_string = ''.join(result)
    return result_string
#------------------------------------------------------------------------------
class Page:
    def __init__(self, config = {}):
        self._logger     = logging.getLogger("page.py")
        self.css_links   = [CSS_PATH]
        self.content     = ""
        self.title       = PAGE_TITLE
        self.javascript_files = []
        self.onload_body = None
        if 'Page.TITLE' in config:
            self.title = config['Page.TITLE']
        if 'Page.CSS_LINK' in config:
            self.css_link = config['Page.CSS_LINK']
        if 'Page.CONTENT' in config:
            self.content = config['Page.CONTENT']
        self._categories = categories.get_categories().get_categories()
        self._logger.debug(self._categories)
    #--------------------------------------------------------------------------
    def set_css_links(self, css_links):
        self.css_links = css_links
    #--------------------------------------------------------------------------
    def add_css_link(self, css_link):
        self.css_links.append(css_link)
    #--------------------------------------------------------------------------
    def add_javascript_file(self, script_name):
        self.javascript_files.append(script_name)
    #--------------------------------------------------------------------------
    def set_onload_body(self, onload_function):
        self.onload_body = onload_function
    #--------------------------------------------------------------------------
    def set_content(self, content):
        self.content = content
    #--------------------------------------------------------------------------
    def set_title(self, title):
        self.title = title
    #--------------------------------------------------------------------------
    def _create_navbar(self):
        self._logger.debug('CGI_SHOW_PATH = ' + CGI_SHOW_PATH)
        html = [self._get_logo_entry()]
        html.extend(['''<ul>
            <li>
            <a href="''', CGI_SHOW_PATH,'''?type=news&content=latest">Home</a></li>
            <li>Articles</li>
            <ul>''']) 
        for category in self._categories:
            html.append('<li><a href="') 
            html.append(CGI_SHOW_PATH)
            html.append('?type=category&content=')
            html.append(category)
            html.append('">')
            html.append(category)
            html.append('</a></li>')
        html.append('</ul>')
        statics_object = statics.Statics()
        for static_entry in statics_object.get_statics():
            html.append(''.join(['<li><a href="', CGI_SHOW_PATH,
                               '?type=static&content=',
                               static_entry, '">',
                               static_entry, '</a></li>']))
        html.append('<li><a href="')
        html.append(RSS_FEED_LINK + PATH_SEPARATOR + RSS_ROLLING_FEED_NAME + '.'
                + RSS_FILE_EXTENSION)
        html.append('''">
                <img src="''')
        html.append(RSS_ICON_PATH)
        html.append('''"  height="18" width="18"/>Subscribe</a>
            </li>
            </ul>
            ''')
        if authenticate_cookie():
            self._logger.debug("Authenticated via cookie")
            html.append('<ul>')
            html.append('<li>[ <a href="')
            html.append(ADD_ARTICLE_LINK)
            html.append('">Add new entry</a> ]</li>')
            html.append('<li>[ <a href="')
            html.append(CHOOSE_UPLOAD_LINK)
            html.append('">Upload file</a> ]</li>')
            html.append('<li>[ <a href="')
            html.append(LOGOUT_LINK)
            html.append('">Log out</a> ]</li>')
            html.append('</ul>')
        html_string = ''.join(html)
        return html_string
    #--------------------------------------------------------------------------
    def _get_logo_entry(self):
        logo_entry = ''
        if FAV_ICON_PATH != '':
            logo_entry = ''.join(['<img src="', FAV_ICON_PATH, 
                '" id="logo_image" alt="Logo">'])
        return logo_entry
    #--------------------------------------------------------------------------
    def _get_favicon_entry(self):
        favicon_link = ''
        if FAV_ICON_PATH != '':
            favicon_link = ''.join(['<link rel="shortcut icon" ',
           'type="image/x-icon" href="', FAV_ICON_PATH, '">' ])
        return favicon_link
    #--------------------------------------------------------------------------
    def get_html(self):
        html_head  = ['<title>', self.title, '</title>']
        html_head.append(self._get_favicon_entry())
        for css_link in self.css_links:
            html_head.append('<link   rel="stylesheet" type="text/css" href="') 
            html_head.append(css_link)
            html_head.append('"/>')
        for javascript_file in self.javascript_files:
            html_head.append('<script src="')
            html_head.append(JAVASCRIPT_URL) 
            html_head.append('/') 
            html_head.append(javascript_file) 
            html_head.append('" type="text/javascript"></script>')
        html_head_string = ''.join(html_head)
        html_body_string = ''.join([
        '''
        <nav>
        ''', self._create_navbar(), '''
        </nav>
        <article>''', 
        self.content, '''
        </article>
        <footer>
            <div class="alignLeft">Powered by 
            <a href="https://code.google.com/p/naga-cms/">naga</a></div>
            <div class="alignRight">''', COPYRIGHT,'''
            </div>
        </footer>'''])
        return wrap(html_body_string, html_head_string, self.onload_body)
    #--------------------------------------------------------------------------

