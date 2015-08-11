# -*- coding: UTF-8 -*-
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
import article
ENVIRONMENT  = 'ENVIRONMENT'
FILENAME = 'FILENAME'
HEADING  = 'HEADING'
SUMMARY  = 'SUMMARY'
CONTENT  = 'CONTENT'
CATEGORIES = 'CATEGORIES'
#------------------------------------------------------------------------------ 
class PostPage:
    '''
    Provides page to post/edit an entry
    '''
    #-------------------------------------------------------------------------- 
    def __init__(self, wsgi_request, **arguments):
        self.__logger     = logging.getLogger()
        self.__request    = None
        self.set_request(wsgi_request)
        self.__file_name  = None
        self.__heading    = ''
        self.__summary    = ''
        self.__content    = None
        self.__categories = []
        if FILENAME in arguments:
            self.__file_name = arguments[FILENAME]
            if self.__file_name != None:
                self.__initialize_data_vars()
        if HEADING in arguments:
            self.__heading    = arguments[HEADING]
        if SUMMARY in arguments:
            self.__summary    = arguments[SUMMARY] 
        if CONTENT in arguments:
            self.__content    = arguments[CONTENT] 
        if CATEGORIES in arguments:
            self.__categories = arguments[CATEGORIES]
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
    def set_request(self, request):
        if request is None:
            self.__logger.error("set_request: request is not WsgiRequest")
        else:
            self.__request = request
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
        if self.__content != None:
            html.append('checked')
        html.append('/>Content</input> <br/>')
        return ''.join(html)
    #-------------------------------------------------------------------------- 
    def __get_categories_checkboxes(self):
        checkbox_html = []
        for cat in categories.get_categories().get_categories():
            checked = ''
            if cat in self.__categories:
                checked = 'checked'
            checkbox_html.extend(['<input type="checkbox" name="category.', 
                cat, '" value="yes" formmethod="post"', checked, '/>', cat, 
                '</input> <br/>'])
        return ''.join(checkbox_html)
    #-------------------------------------------------------------------------- 
    def to_html(self, preview = False):
        if not security.authenticate_cookie(self.__request):
                return '<p class="error">Authentication failure</p>'
        file_name = None
        html_body = StringIO()
        if preview:
            article_object = article.Article()
            article_object.set_heading(self.__heading)
            article_object.set_summary(self.__summary)
            if self.__content != None:
                article_object.set_content(self.__content)
            article_object.set_categories(self.__categories)
            html_body.write(article_object.to_html())
        html_body.write('''<h1>Make your post!</h1>
        <form action="''')
        html_body.write(self.__get_upload_path())
        html_body.write('''" method="post">
            Heading: 
            <input type="text"     id=input_heading"  name="heading" +
            value="''' + self.__heading + '''"/> <br/>
            Summary: <br/>
            <textarea              id="input_summary" name="summary"> ''' +
            self.__summary + 
            '''</textarea> <br/>''')
        html_body.write(self.__get_content_checkbox())
        content = self.__content
        if content == None:
            content = ''
        html_body.write('''
            Content: <br/>
            <textarea              id="input_content" name="content">''' +
            content +
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
        return html_body_string

