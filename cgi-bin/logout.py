#!/usr/bin/python3
import cgi
import cgitb
import io
import os
import sys
import logging
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import security
import page
#------------------------------------------------------------------------------    
__logger = logging.getLogger()
#------------------------------------------------------------------------------    
if __name__ == '__main__':
    cgitb.enable()
    cgi_variables = cgi.FieldStorage()
    html_body_string = '<p>Logged out</p>'
    page_object = page.Page() 
    cookie = security.get_logout_cookie()
    print(cookie.output())
    page_object.set_content(html_body_string)
    print(page_object.get_html())
    __logger.info(html_body_string)

