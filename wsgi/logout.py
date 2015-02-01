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
def call(request, start_response):
    page_object = page.Page(request)
    cookie = security.get_logout_cookie()
    request.set_cookie(cookie)
    html_body_string = '<p>Logged out</p>'
    page_object.set_content(html_body_string)
    __logger.info(html_body_string)
    return naga_wsgi.create_response(start_response, 
            page_object.get_html(), cookie=cookie)
#------------------------------------------------------------------------------
def application(environ, start_response):
    request = naga_wsgi.Wsgi(environ)
    errorCatchingHook = ErrorCatchingHook(call)
    return  errorCatchingHook(request, start_response)

