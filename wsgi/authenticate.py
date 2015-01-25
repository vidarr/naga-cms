#!/usr/bin/python3
import io
import os
import sys
import logging
from cgi import parse_qs
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
    form = parse_qs(environ['QUERY_STRING'])
    page_object = page.Page() 
    user = security.get_user(form)
    passphrase = security.get_passphrase(form)
    if not security.authenticate(user, passphrase):
        page_object.set_content('<p class="error">Authentication failure</p>')
        print(page_object.get_html())
        sys.exit(1)
    html_body_string = '<p>Authenticated</p>'
    if not user or not passphrase:
        html_body_string = "Error occured during authentication"
        __logger.error(
                "Could not extract user or passphrase from cgi variables")
        naga_wsgi.wsgi_start_response(start_response)
    else:
        cookie = security.get_credential_cookies(user, passphrase)
        naga_wsgi.wsgi_start_response(start_response, cookie=cookie)
        # 'Set' cookie for this run already ...
        security.set_cookie_for_current_request(environ, cookie)
        page_object.set_environment(environ)
    __logger.info(html_body_string)
    page_object.set_content(html_body_string)
    response_body = page_object.get_html()
    return [response_body]

