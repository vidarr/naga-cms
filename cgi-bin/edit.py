#!/usr/bin/python
import cgi
import cgitb
import logging
import os
import sys
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import page
#------------------------------------------------------------------------------    
_logger = logging.getLogger("edit.py")
#------------------------------------------------------------------------------    
if __name__ == '__main__':
    cgitb.enable()
    _logger.info("Request")
    form = cgi.FieldStorage()
    if not 'forward' in form:
        _logger.error("Nowhere to forward")
        sys.exit(1)
    forward_link = form['forward'].value
    html_head = '<title>Michael J. Beer</title>'
    html_body = ''.join(['''<h1>Please authenticate</h1>
    <form action=''', forward_link, '''>
        <table>
        <tr><td>
        User: 
        </td><td>
        <input type="text"     id="input_user"  name="''', CREDENTIALS_USER, 
        '''" formmethod="post"/> 
        </td></tr><tr><td>
        Passphrase: 
        </td><td>
        <input type="password"     id="input_passphrase" name="''', 
        CREDENTIALS_PASSPHRASE, '''" formmethod="post"/> 
        </td></tr>
        </table>
        <input type="submit" value="Submit"><br/>
    </form>
    '''])
    print page.wrap(html_body, html_head)
