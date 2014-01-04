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
def wrap(content, head = "<title>naga</title>"):
    result = ["Content-Type: text/html\n\n",
        '''<!DOCTYPE HTML>
<html>
    <head>
        <meta   charset="utf8">''', head, '</head><body>', 
    content, '</body></html>'] 
    result_string = ''.join(result)
    return result_string
#------------------------------------------------------------------------------
class Page:
    def __init__(self, config = {}):
        self._logger     = logging.getLogger("page.py")
        self.css_links   = [CSS_PATH]
        self.content     = ""
        self.title       = PAGE_TITLE
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
    def set_content(self, content):
        self.content = content
    #--------------------------------------------------------------------------
    def set_title(self, title):
        self.title = title
    #--------------------------------------------------------------------------
    def _create_navbar(self):
        html = ['''
            <ul>
            <li>
            <a href="''', CGI_SHOW_PATH,'''?type=news&content=latest">Home</a></li>
            <li>Articles</li>
            <ul>'''] 
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
        html.append(RSS_FEED_PATH)
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
            html.append(ADD_ARTICLE_PATH)
            html.append('">Add new entry</a> ]</li>')
            html.append('<li>[ <a href="')
            html.append(LOGOUT_PATH)
            html.append('">Log out</a> ]</li>')
            html.append('</ul>')
        html_string = ''.join(html)
        return html_string
    #--------------------------------------------------------------------------
    def get_html(self):
        html_head  = ['<title>', self.title, '</title>']
        for css_link in self.css_links:
            html_head.append('<link   rel="stylesheet" type="text/css" href="') 
            html_head.append(css_link)
            html_head.append('">')
        html_head_string = ''.join(html_head)
        html_body_string = ''.join(['<nav>', self._create_navbar(), '''
            </nav>
            <article>''', 
            self.content, '''
                </article>
                <footer>
                <p class="alignLeft">Powered by 
                <a href="https://code.google.com/p/naga-cms/">naga</a></p>
                <p class="alignRight">''', COPYRIGHT,'</p></footer>'])
        return wrap(html_body_string, html_head_string)
    #--------------------------------------------------------------------------

