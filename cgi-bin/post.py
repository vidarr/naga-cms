#!/usr/bin/python3
import cgi
import cgitb
from io import StringIO
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
import categories
import page
#------------------------------------------------------------------------------    
_logger     = logging.getLogger()
_file_name  = None
_content    = ''
_summary    = ''
_heading    = ''
_categories = []
#------------------------------------------------------------------------------    
def initialize_data_vars(file_name):
    if file_name:
        registry_object = registry.Registry()
        if not file_name in registry_object.get_article_keys():
            _logger.error(file_name + " does not exist")
            return False
        article_object = registry_object.get(file_name)
        _heading  = article_object.get_heading()
        _summary  = article_object.get_summary()
        _content  = article_object.get_content()
        _categories = article_object.get_categories()
    return True
#------------------------------------------------------------------------------    
if __name__ == '__main__':
    cgitb.enable()
    cgi_variables = cgi.FieldStorage()
    page_object = page.Page()
    if not security.authenticate_cookie():
        page_object.set_page('<p class="error">Authentication failure</p>')
        print(page_object.get_html())
        sys.exit(1)
    if HTTP_ARG_FILE_NAME in cgi_variables.keys():
        file_name = cgi_variables[HTTP_ARG_FILE_NAME]
        if not initialize_data_vars(file_name):
            page.set_content('<p class="error">' + file_name + 
                ' does not exist</p>')
            print(page.get_html())
            sys.exit(1)
    page_object.add_css_link(CSS_POST_PATH)
    html_body = StringIO()
    html_body.write('''<h1>Make your post!</h1>
    <form action="''')
    html_body.write(UPLOAD_PATH)
    html_body.write('''" method="post">
        Heading: 
        <input type="text"     id=input_heading"  name="heading" value="''' + 
        _heading + '''"/> <br/>
        Summary: <br/>
        <textarea              id="input_summary" name="summary" value="''' + 
        _summary + '''"></textarea> <br/>
        <input type="checkbox" name="contentexists" value="yes"/>Content</input> <br/>
        Content: <br/>
        <textarea              id="input_content" name="content" value="''' +
        _content +
        '''"></textarea> <br/>
        <h2>Categories</h2>
        ''')
    for cat in categories.get_categories().get_categories():
        html_body.write(''.join(['<input type="checkbox" name="category.', cat, 
            '" value="yes" formmethod="post"/>', cat, '</input> <br/>']))
    html_body.write('''<input type="submit" value="Submit"><br/>
    </form>
    ''')
    html_body_string = html_body.getvalue()
    html_body.close()
    page_object.set_content(html_body_string)
    print(page_object.get_html())

