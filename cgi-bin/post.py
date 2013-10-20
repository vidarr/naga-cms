#!/usr/bin/python
import cgi
import cgitb
import StringIO
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
import categories
#------------------------------------------------------------------------------    
_logger = logging.getLogger()
#------------------------------------------------------------------------------    
if __name__ == '__main__':
    cgitb.enable()
    cgi_variables = cgi.FieldStorage()
    if not security.authenticate_cgi(cgi_variables):
        print "Content-Type: text/html\n\n"
        print '<html><body><p class="error">Authentication failure</p></body></html>'
        sys.exit(1)
    print "Content-Type: text/html\n\n"
    print '''<!DOCTYPE HTML>
<html>
    <head>
        <title>Michael J. Beer</title>
        <link rel="stylesheet" href="'''
    print CSS_POST_PATH
    print '''"/> 
    </head>
<body>

    <h1>Make your post!</h1>

    <form action="'''
    print  UPLOAD_PATH
    print '''">
        Heading: 
        <input type="text"     id=input_heading"  name="heading"
        formmethod="post"/> <br/>
        Summary: <br/>
        <input type="text"     id="input_summary" name="summary" formmethod="post"/> <br/>
        <input type="checkbox" name="contentexists" value="yes" formmethod="post"/>Content</input> <br/>
        Content: <br/>
        <input type="text"     id="input_content" name="content" formmethod="post"/> <br/>
        <h2>Categories</h2>
        '''
    for cat in categories.get_categories().get_categories():
        print  '<input type="checkbox" name="category.' + cat + '" value="yes" formmethod="post"/>' + \
                cat + '</input> <br/>'
    print ''.join(['<input type="hidden" name="', CREDENTIALS_USER, '" value="',
        security.get_user(cgi_variables), '">'])
    print ''.join(['<input type="hidden" name="', CREDENTIALS_PASSPHRASE, '" value="',
        security.get_passphrase(cgi_variables), '">'])
    print '''<input type="submit" value="Submit"><br/>
    </form>
</body>
    '''

