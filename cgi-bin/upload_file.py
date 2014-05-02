#!/usr/bin/python3
import cgi
import cgitb
import sys
import string
import logging
from os.path import join, dirname, abspath, basename
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
    if 'file_to_upload' not in form or 'type' not in form:
        _logger.error("Error: Called without enough parameters")
        print(page.wrap('''
             <p class="error">Internal error: Called without 
            enough parameters.</p>'''))
        sys.exit(1)
    file_item = form['file_to_upload']
    file_type = form['type'].value
    file_name = basename(file_item.filename)
    file_content = file_item.file.read()
    page_object = page.Page()
    if upload_file(file_type, file_name, file_content):
        page_object.set_content('''Upload successful''')
    else:
        page_object.set_content('''Error occured''')
    print(page_object.get_html())
    sys.exit(0)

