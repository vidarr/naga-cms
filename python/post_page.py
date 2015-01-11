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
import registry
FILENAME = 'FILENAME'
CONTENT  = 'CONTENT'
HEADING  = 'HEADING'
CATEGORIES = 'CATEGORIES'
#------------------------------------------------------------------------------ 
class PostPage:
    '''
    Provides page to post/edit an entry
    '''
    #-------------------------------------------------------------------------- 
    def __init__(self, **arguments):
        self.__logger     = logging.getLogger()
        self.__file_name  = None
        self.__content    = ''
        self.__heading    = ''
        self.__categories = []
        if FILENAME in arguments:
            self.__file_name = arguments['FILENAME']
            self.__initialize_data_vars()
        else:
            if CONTENT in arguments and HEADING in arguments and \
                    CATEGORIES in arguments:
                self.__content    = arguments['CONTENT'] 
                self.__heading    = arguments['HEADING']
                self.__categories = arguments['CATEGORIES']
            elif  CONTENT in arguments or  HEADING in arguments or \
                    CATEGORIES in arguments:
                        raise Exception("Expected either a file name" +
                                "or content, heading and arguments")
    #-------------------------------------------------------------------------- 
    def __initialize_data_vars(self):
        registry_object = registry.Registry()
        if not self.__file_name in registry_object.get_article_keys():
            self.__logger.error(self.__file_name + " does not exist")
            return False
        article_object = registry_object.get(self.__file_name)
        self.__heading    = article_object.get_heading()
        self.__content    = article_object.get_content()
        self.__categories = article_object.get_categories()
        self.__logger.info("Loaded " + self.__file_name + 
                ' with heading = ' + self.__heading)
        return True
    #-------------------------------------------------------------------------- 
    def __get_upload_path(self):
        upload_path = [UPLOAD_PATH]
        if self.__file_name:
            upload_path.append('?')
            upload_path.append(HTTP_ARG_FILE_NAME)
            upload_path.append('=')
            upload_path.append(self.__file_name)
        return ''.join(upload_path)
    #-------------------------------------------------------------------------- 
    def __get_content_checkbox(self):
        html = ['<input type="checkbox" name="contentexists" value="yes"']
        if self.__file_name:
            html.append('checked')
        html.append('/>Content</input> <br/>')
        return ''.join(html)
    #-------------------------------------------------------------------------- 
    def __get_categories_checkboxes(self):
        checkbox_html = []
        for cat in categories.get_categories().get_categories():
            checked = ''
            if cat in _self.__categories:
                checked = 'checked'
            checkbox_html.extend(['<input type="checkbox" name="category.', 
                cat, '" value="yes" formmethod="post"', checked, '/>', cat, 
                '</input> <br/>'])
        return ''.join(checkbox_html)
    #-------------------------------------------------------------------------- 
    def get_html(self, preview = False):
        page_object = page.Page()
        if not security.authenticate_cookie():
            page_object.set_set_content(
                    '<p class="error">Authentication failure</p>')
            return page_object.get_html()
        file_name = None
        page_object.add_css_link(CSS_POST_PATH)
        html_body = StringIO()
        html_body.write('''<h1>Make your post!</h1>
        <form action="''')
        html_body.write(self.__get_upload_path())
        html_body.write('''" method="post">
            Heading: 
            <input type="text"     id=input_heading"  name="heading" +
            value="''' + self.__heading + '''"/> <br/>
            Summary: <br/>
            <textarea              id="input_summary" name="summary">
            </textarea> <br/>''')
        html_body.write(self.__get_content_checkbox())
        html_body.write('''
            Content: <br/>
            <textarea              id="input_content" name="content">''' +
            self.__content +
            '''</textarea> <br/>
            <h2>Categories</h2>
            ''')
        html_body.write(self.__get_categories_checkboxes())
        html_body.write('''<table>
    <tr>
    <td><input type="submit" name="preview" value="Preview"></td>
    <td><input type="submit" name="post" value="Send"></td></tr>
    </table><br/>
    </form>''')
        html_body_string = html_body.getvalue()
        html_body.close()
        self.__logger.info(html_body_string)
        page_object.set_content(html_body_string)
        return page_object.get_html()

