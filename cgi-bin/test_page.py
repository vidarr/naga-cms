#!/usr/bin/python
import os.path
import sys

PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import naga_config
import page

def test():
    config = { 'Page.TITLE'    : 'My Test Page', 'Page.CSS_LINK' :
            '../test.css', 'Page.CONTENT'  :  'This is THE test page' }
    html_page = page.Page(config)
    return html_page.get_html()

print "Content-type: text/html\n\n"
print test()





