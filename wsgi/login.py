#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2013, 2014, 2015 
#                  Michael J. Beer <michael.josef.beer@googlemail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
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
    page_object = page.Page(environ)
    page_object.set_content(html_body)
    __logger.info(page_object.get_html())
    response_body = page_object.get_html()
    return naga_wsgi.create_response(start_response, response_body)


