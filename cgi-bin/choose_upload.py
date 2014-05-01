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
    upload_page = page.Page()
    upload_page.set_title('Michael J. Beer')
    html_body = ''.join([
    '''
    <form action="''', 'upload_file.py', '''" method="post" enctype="multipart/form-data" >
        <table>
            <tr>
                <td class="center_item" colspan="2">
                    <label for="upload">File to upload:</label>
                    <input type="file" 
                    id="upload" name="file_to_upload">
                </td>
            </tr><tr>
                <td class="center_item">
                    <input type="radio" name="type" id="type_file" value="''', STORE_TYPE_FILE, 
                    '''"><label for="type_file">File</label>
                </td><td class="center_item"> 
                    <input type="radio" name="type" id="type_image" value="''', STORE_TYPE_IMAGE,
                    '''">
                    <label for="typeImage">Image</label>
                </td>
            </tr><tr>
                <td class="center_item" colspan="2">
                    <input type="submit" value="Submit"><br/>
                </td>
            </tr>
        </table>
    </form>
    '''])
    #  '''
    #  <form action="''', 'upload_file.py', '''" method="post" enctype="multipart/form-data" >
    #      File to upload: <input type="file" id="upload" name="file_to_upload"''',
    #      ''' onchange="uploadOnChange()">
    #      <input type="radio" name="type" id="type_file" value="''', STORE_TYPE_FILE, 
    #                  '''"><label for="type_file">File</label>
    #      <input type="radio" name="type" id="type_image" value="''', STORE_TYPE_IMAGE, '''">
    #                  <label for="typeImage">Image</label>
    #      <input type="submit" value="Submit"><br/>
    #      <input type="hidden" id="file_name" name="file_name">
    #  </form>
    #  <div id="show_file_name"></div>
    #  '''])
    upload_page.set_content(html_body)
    print(upload_page.get_html())
