import StringIO
import os
import sys

PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import naga_config

class Page:

    def __init__(self, config = {}):
        self.css_link = ""
        self.content  = ""
        self.title    = ""
        if 'Page.TITLE' in config:
            self.title = config['Page.TITLE']
        if 'Page.CSS_LINK' in config:
            self.css_link = config['Page.CSS_LINK']
        if 'Page.CONTENT' in config:
            self.content = config['Page.CONTENT']


    def set_css_link(self, css_link):
        self.css_link = css_link


    def set_content(self, content):
        self.content = content


    def set_title(self, title):
        self.title = title


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
            <nav>
                <ul>
                    <li>Home</li>
                    <li>Projekte</li>
                    <li>Blog</li>
                    <li>Kontakt</li>
                    <li><a href="''')
        html.write(naga_config.RSS_FEED_PATH)
        html.write('''">
                <img src="''')
        html.write(naga_config.RSS_ICON_PATH)
        html.write('''"  height="18" width="18"/>Subscribe</a>
                    </li>
                </ul>
                </nav>
                <article>''')
        html.write(self.content)
        html.write('''
                </article>
            </body>
            </html>''')
        html_string = html.getvalue()
        html.close()
        return html_string

