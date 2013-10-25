#!/usr/bin/python3
import cgi
import cgitb
from io import StringIO
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
import page
#------------------------------------------------------------------------------    
_logger = logging.getLogger()
#------------------------------------------------------------------------------    
if __name__ == '__main__':
    cgitb.enable()
    cgi_variables = cgi.FieldStorage()
    if not security.authenticate_cgi(cgi_variables):
        print(page.wrap('<p) class="error">Authentication failure</p></body></html>'))
        sys.exit(1)
    head_string = ''.join(['''<title>Michael J. Beer</title>
    <link rel="stylesheet" href="''', CSS_POST_PATH, '"/>']) 
    html_body = StringIO()
    html_body.write('''<h1>Make your post!</h1>
    <form action="''')
    html_body.write(UPLOAD_PATH)
    html_body.write('''" method="post">
        Heading: 
        <input type="text"     id=input_heading"  name="heading"/> <br/>
        Summary: <br/>
        <textarea              id="input_summary" name="summary"></textarea> <br/>
        <input type="checkbox" name="contentexists" value="yes"/>Content</input> <br/>
        Content: <br/>
        <textarea              id="input_content" name="content"></textarea> <br/>
        <h2>Categories</h2>
        ''')
    for cat in categories.get_categories().get_categories():
        html_body.write(''.join(['<input type="checkbox" name="category.', cat, 
            '" value="yes" formmethod="post"/>', cat, '</input> <br/>']))
    html_body.write(''.join(['<input type="hidden" name="', CREDENTIALS_USER, '" value="',
        security.get_user(cgi_variables), '">']))
    html_body.write(''.join(['<input type="hidden" name="', CREDENTIALS_PASSPHRASE, '" value="',
        security.get_passphrase(cgi_variables)])) 
    html_body.write('''"><input type="submit" value="Submit"><br/>
    </form>
    ''')
    html_body_string = html_body.getvalue()
    html_body.close()
    html = page.wrap(html_body_string, head_string)
    _logger.info(html)
    print(html)

