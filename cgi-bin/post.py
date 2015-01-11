#!/usr/bin/python3
import cgi
import cgitb
import os
import sys
#-------------------------------------------------------------------------------
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import post_page
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    cgitb.enable()
    cgi_variables = cgi.FieldStorage()
    if HTTP_ARG_FILE_NAME in cgi_variables.keys():
        file_name = cgi_variables[HTTP_ARG_FILE_NAME]
        post = post_page.PostPage(FILENAME=file_name.value)
    else:
        post = post_page.PostPage()
    html_string = post.get_html()
    print(html_string)

