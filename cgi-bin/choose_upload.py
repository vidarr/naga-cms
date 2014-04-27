#!/usr/bin/python3
import cgi
import cgitb
import logging
from os.path import join, dirname, abspath
import sys
#------------------------------------------------------------------------------    
PAGE_ROOT   = join(dirname(abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(join(PAGE_ROOT, '..', MODULE_DIR))
from naga_config import *
import page
#------------------------------------------------------------------------------    
_logger = logging.getLogger("choose_upload.py")
#------------------------------------------------------------------------------    
if __name__ == '__main__':
    cgitb.enable()
    form = cgi.FieldStorage()
    _logger.debug("UPLOAD_FILE_PATH = " + UPLOAD_FILE_PATH)
    html_head = '<title>Michael J. Beer</title>'
    html_body = ''.join([
    '''<form action="''', 'upload_file.py', '''" method="post">
        <table>
        <tr><td>
        File to upload: 
        <input type="file" enctype="multipart/form-data" name="file_to_upload">
        </td></tr><tr><td>
        <input type="radio" name="type" id="type_file" value="''', STORE_TYPE_FILE, 
        '''"><label for="type_file">File</label>
        </dt><dt> 
        <input type="radio" name="type" id="type_image" value="''', STORE_TYPE_IMAGE,
        '''">
        <label for="typeImage">Image</label>
        </td></tr>
        </table>
        <input type="submit" value="Submit"><br/>
    </form>
    '''])
    print(page.wrap(html_body, html_head))
