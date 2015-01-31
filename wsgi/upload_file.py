#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2015 Michael J. Beer <michael.josef.beer@googlemail.com>
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
import sys
import string
import logging
from os.path import join, dirname, abspath, basename
from cgi import escape
#------------------------------------------------------------------------------
PAGE_ROOT   = join(dirname(abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(join(PAGE_ROOT, '..', MODULE_DIR))
from naga_config import *
import security
import page
import store
from naga_wsgi import wsgi_create_response, wsgi_get_post_variables
from wsgi_hooks import EnsureAuthenticatedHook
#------------------------------------------------------------------------------
_logger        = logging.getLogger("upload_file")
#------------------------------------------------------------------------------
def post_file(upload_type, file_name, content = None):
    store_object = store.get_store(upload_type)
    if store_object == None:
        _logger.error("could not get store for " + upload_type)
        return False
    store_object.put(file_name, content)
    return True
#------------------------------------------------------------------------------
def upload_file(environ, start_response):
    _logger.info("upload_file.py: Upload request received")
    page_object = page.Page(environ)
    (file_to_upload, file_type) = wsgi_get_post_variables(environ, 
            'file_to_upload', 'type')
    _logger.debug("file_type :")
    _logger.debug(str(file_type))
    _logger.debug(str(file_to_upload))
    if file_to_upload is None or file_type is None:
        _logger.error("Error: Called without enough parameters")
        page_object.set_content('''
             <p class="error">Internal error: Called without 
            enough parameters.</p>''')
    else:
        file_type = escape(file_type.value)
        file_name = basename(file_to_upload.filename)
        file_content = file_to_upload.file.read()
        if post_file(file_type, file_name, file_content):
            page_object.set_content('''Upload successful''')
        else:
            page_object.set_content('''Error occured''')
    return wsgi_create_response(start_response, page_object.get_html())
#------------------------------------------------------------------------------
def application(environ, start_response):
    ensureAuthenticatedHook = EnsureAuthenticatedHook(upload_file)
    return  ensureAuthenticatedHook(environ, start_response)
