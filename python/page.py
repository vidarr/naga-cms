import StringIO
import os
import sys
#------------------------------------------------------------------------------
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import categories
import statics
#------------------------------------------------------------------------------
def wrap(content, head = "<title>naga</title>"):
    result = StringIO.StringIO()
    result.write("Content-Type: text/html\n\n")
    result.write('''<!DOCTYPE HTML>
<html>
    <head>
        <meta   charset="utf8">''')
    result.write(head)
    result.write('</head><body>')
    result.write(content)
    result.write('</body></html>')
    result_string = result.getvalue()
    result.close()
    return result_string
#------------------------------------------------------------------------------
class Page:
    def __init__(self, config = {}):
        self._logger     = logging.getLogger("page.py")
        self.css_link = CSS_PATH
        self.content  = ""
        self.title    = PAGE_TITLE
        if 'Page.TITLE' in config:
            self.title = config['Page.TITLE']
        if 'Page.CSS_LINK' in config:
            self.css_link = config['Page.CSS_LINK']
        if 'Page.CONTENT' in config:
            self.content = config['Page.CONTENT']
        self._categories = categories.get_categories().get_categories()
        self._logger.debug(self._categories)
    #--------------------------------------------------------------------------
    def set_css_link(self, css_link):
        self.css_link = css_link
    #--------------------------------------------------------------------------
    def set_content(self, content):
        self.content = content
    #--------------------------------------------------------------------------
    def set_title(self, title):
        self.title = title
    #--------------------------------------------------------------------------
    def _create_navbar(self):
        html = StringIO.StringIO()
        html.write('''
            <ul>
            <li>
            <a href="''')
        html.write(CGI_SHOW_PATH)
        html.write('''?type=news&content=latest">Home</a></li>
            <li>Articles</li>
            <ul>''')
        for category in self._categories:
            html.write('<li><a href="')
            html.write(CGI_SHOW_PATH)
            html.write('?type=category&content=')
            html.write(category)
            html.write('">')
            html.write(category)
            html.write('</a></li>')
        html.write('''</ul>''')
        statics_object = statics.Statics()
        for static_entry in statics_object.get_statics():
            html.write(''.join(['<li><a href="', CGI_SHOW_PATH,
                               '?type=static&content=',
                               static_entry, '">',
                               static_entry, '</a></li>']))
        html.write('<li><a href="')
        html.write(RSS_FEED_PATH)
        html.write('''">
                <img src="''')
        html.write(RSS_ICON_PATH)
        html.write('''"  height="18" width="18"/>Subscribe</a>
            </li>
            </ul>''')
        html_string = html.getvalue()
        html.close()
        return html_string
    #--------------------------------------------------------------------------
    def get_html(self):
        html_head = StringIO.StringIO()
        html_head.write('<title>')
        html_head.write(self.title)
        html_head.write('''</title>
            <link   rel="stylesheet" type="text/css" href="''')
        html_head.write(self.css_link)
        html_head.write('''"></link>''')
        html_head_string = html_head.getvalue()
        html_head.close()
        html_body = StringIO.StringIO()
        html_body.write('''
            <nav>''')
        html_body.write(self._create_navbar())
        html_body.write('''
            </nav>
            <article>''')
        html_body.write(self.content)
        html_body.write('''
                </article>
                <footer>
                <p class="alignLeft">Powered by 
                <a href="https://code.google.com/p/naga-cms/">naga</a></p>
                <p class="alignRight">''')
        html_body.write(COPYRIGHT)
        html_body.write('''</p> 
            </footer>
            </body>
            </html>''')
        html_body_string = html_body.getvalue()
        html_body.close()
        return wrap(html_body_string, html_head_string)
    #--------------------------------------------------------------------------

