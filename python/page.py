import StringIO
import os
import sys
#------------------------------------------------------------------------------
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import categories
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
            <a href="http://localhost/naga/cgi-bin/show.py?type=news&content=latest">Home</a></li>
            <li>Projekte</li>
            <li>Blog</li>
            <ul>''')
        for category in self._categories:
            html.write('<li><a href="')
            html.write(CGI_SHOW_PATH)
            html.write('?type=category&content=')
            html.write(category)
            html.write('">')
            html.write(category)
            html.write('</a></li>')
        html.write('''</ul>
        <li>Kontakt</li>
        <li><a href="''')
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
        html = StringIO.StringIO()
        html.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta   charset="utf8"></meta>
            <title>""" )
        html.write(self.title)
        html.write('''</title>
            <link   rel="stylesheet" type="text/css" href="''')
        html.write(self.css_link)
        html.write('''"></link>
        </head>
        <body>
            <nav>''')
        html.write(self._create_navbar())
        html.write('''
            </nav>
            <article>''')
        html.write(self.content)
        html.write('''
                </article>
                <footer>
                <p class="alignLeft">Powered by 
                <a href="https://ubeer.org">naga</a></p>
                <p class="alignRight">''')
        html.write(COPYRIGHT)
        html.write('''</p> 
            </footer>
            </body>
            </html>''')
        html_string = html.getvalue()
        html.close()
        return html_string
    #--------------------------------------------------------------------------
