import os
import sys
import logging
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import page
import naga_wsgi
#------------------------------------------------------------------------------    
__logger = logging.getLogger("login.py")
#------------------------------------------------------------------------------    
def application(environ, start_response):
    __logger.info("Login request")
    html_body = ''.join(['''<h1>Please authenticate</h1>
    <form action=''', AUTHENTICATE_LINK, '''>
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
        <input type="submit" value="Submit"/><br/>
    </form>
    '''])
    page_object = page.Page()
    page_object.set_content(html_body)
    __logger.info(page_object.get_html())
    naga_wsgi.wsgi_start_response(start_response)
    response_body = page_object.get_html()
    return [response_body]

