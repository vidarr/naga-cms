#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2013, 2014 Michael J. Beer <michael.josef.beer@googlemail.com>
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
from wsgi_hooks import ErrorCatchingHook
#------------------------------------------------------------------------------
__logger = logging.getLogger()
#------------------------------------------------------------------------------
def authenticate(request, start_response):
    cookie = None
    page_object = page.Page(request)
    user = security.get_user(request)
    passphrase = security.get_passphrase(request)
    if not user or not passphrase:
        html_body_string = "Error occured during authentication"
        __logger.error(
                "Could not extract user or passphrase from cgi variables")
    elif not security.authenticate(user, passphrase):
        html_body_string = '<p class="error">Authentication failure</p>'
    else:
        html_body_string = '<p>Authenticated</p>'
        cookie = security.get_credential_cookies(user, passphrase)
        request.set_cookie(cookie)
    __logger.info(html_body_string)
    page_object.set_content(html_body_string)
    response_body = page_object.get_html()
    return naga_wsgi.create_response(start_response, response_body, 
            cookie=cookie)
#------------------------------------------------------------------------------
def application(environ, start_response):
    request = naga_wsgi.Wsgi(environ)
    errorCatchingHook = ErrorCatchingHook(authenticate)
    return  errorCatchingHook(request, start_response)
