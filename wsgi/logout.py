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
import naga_wsgi
#------------------------------------------------------------------------------    
__logger = logging.getLogger()
#------------------------------------------------------------------------------    
def application(environ, start_response):
    page_object = page.Page() 
    cookie = security.get_logout_cookie()
    security.set_cookie_for_current_request(environ, cookie)
    page_object.set_environment(environ)
    html_body_string = '<p>Logged out</p>'
    page_object.set_content(html_body_string)
    __logger.info(html_body_string)
    naga_wsgi.wsgi_start_response(start_response, cookie=cookie)
    return [page_object.get_html()]


