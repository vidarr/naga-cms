#!/usr/bin/python3
import cgi
import cgitb
import sys
import string
import logging
from os.path import join, dirname, abspath
#------------------------------------------------------------------------------
PAGE_ROOT   = join(dirname(abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(join(PAGE_ROOT, '..', MODULE_DIR))
from naga_config import *
import security
import page
import store
#------------------------------------------------------------------------------
_logger        = logging.getLogger("upload_file")
#------------------------------------------------------------------------------
def upload_file(upload_type, file_name, content = None):
    store_object = store.get_store(upload_type)
    if store_object == None:
        _logger.error("could not get store for " + upload_type)
        return False
    store_object.put(file_name, content)
    return True
#------------------------------------------------------------------------------
if __name__ == '__main__':
    cgitb.enable()
    _logger.info("upload_file.py: Upload request received")
    form = cgi.FieldStorage()
#     if not security.authenticate_cookie():
#         _logger.warn("Authentication failure")
#         print(page.wrap('<p class="error">Authentication failure</p>'))
#         sys.exit(1)
    if 'file_name' not in form or 'type' not in form:
        _logger.error("Error: Called without enough parameters")
        print(page.wrap('''
             <p class="error">Internal error: Called without
            enough parameters</p>'''))
        sys.exit(1)
    file_name = form['file_name'].value
    upload_type = form['type'].value
    if upload_file(upload_type, file_name, 'success'):
        print(page.wrap('''Upload successful'''))
    else:
        print(page.wrap('''Error occured'''))

