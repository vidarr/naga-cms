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
import logging
from os.path import join, dirname, abspath
import sys
#------------------------------------------------------------------------------
PAGE_ROOT   = join(dirname(abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(join(PAGE_ROOT, '..', MODULE_DIR))
from naga_config import *
import page
import security
import naga_wsgi
from wsgi_hooks import EnsureAuthenticatedHook, ErrorCatchingHook
#------------------------------------------------------------------------------
_logger = logging.getLogger("choose_upload.py")
#------------------------------------------------------------------------------
def choose_upload(request, start_response):
    upload_page = page.Page(request)
    if not security.authenticate_cookie(request):
        upload_page.set_content('<p class="error">Authentication failure</p>')
        print(upload_page.get_html())
        sys.exit(1)
    upload_page.set_title('Michael J. Beer')
    html_body = ''.join([
    '''
    <h1>Choose File to upload</h1>
    <div class="center_item">
    <form action="upload_file.py" method="post" enctype="multipart/form-data" >
        <table>
            <tr>
                <td>
                    <label for="upload">File to upload:</label>
                </td><td class="center_item">
                    <input type="file"
                    id="upload" name="file_to_upload">
                </td>
            </tr><tr>
                <td>
                    File type:
                </td><td class="center_item">
                    <input type="radio" name="type" id="type_file" value="''',
                    STORE_TYPE_FILE, '''">
                    <label for="type_file">File</label>
                    <input type="radio" name="type" id="type_image" value="''',
                    STORE_TYPE_IMAGE, '''">
                    <label for="typeImage">Image</label>
                </td>
            </tr><tr>
                <td class="center_item" colspan="2">
                    <input type="submit" value="Submit"><br/>
                </td>
            </tr>
        </table>
    </form>
    </div>
    '''])
    upload_page.set_content(html_body)
    return naga_wsgi.create_response(start_response, upload_page.get_html())
#------------------------------------------------------------------------------
def application(environ, start_response):
    request = naga_wsgi.Wsgi(environ)
    errorCatchingHook = ErrorCatchingHook(choose_upload)
    ensureAuthenticatedHook = EnsureAuthenticatedHook(errorCatchingHook)
    return  ensureAuthenticatedHook(request, start_response)

