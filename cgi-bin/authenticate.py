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
    page_object = page.Page() 
    if not security.authenticate_cgi(cgi_variables):
        page_object.set_content('<p class="error">Authentication failure</p>')
        print(page_object.get_html())
        sys.exit(1)
    html_body_string = '<p>Authenticated</p>'
    user = security.get_user(cgi_variables)
    passphrase = security.get_passphrase(cgi_variables)
    if not user or not passphrase:
        html_body_string = "Error occured during authentication"
        __logger.error(
                "Could not extract user or passphrase from cgi variables")
    else:
        cookie = security.get_credential_cookie(user, passphrase)
        print(cookie.output())
    __logger.info(html_body_string)
    page_object.set_content(html_body_string)
    print(page_object.get_html())

