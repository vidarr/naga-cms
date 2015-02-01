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
import os.path
import sys
import logging
from urllib.parse import parse_qs
from cgi import escape, FieldStorage
from http import cookies
#------------------------------------------------------------------------------
_logger = logging.getLogger("wsgi_naga")
#---------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR)
#------------------------------------------------------------------------------
def serialize_cookie(cookie):
    return cookie.output(header='', sep=';  ')
#------------------------------------------------------------------------------
def create_response(start_response_callback, response_body, **options):
    '''
    Create appropriate HTTP header
    '''
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))]
    if 'additional_headers' in options:
        response_headers.extend(options['additional_headers'])
    if 'cookie' in options:
        cookie = options['cookie']
        cookie = serialize_cookie(cookie)
        cookies = cookie.split(';  ')
        for c in cookies:
            response_headers.append(('Set-Cookie', c))
    start_response_callback(status, response_headers)
    return [response_body]
#------------------------------------------------------------------------------
class Wsgi:
    '''
    '''
    #--------------------------------------------------------------------------
    def __init__(self, environ):
        self.get_variables  = self.__get_get_variables(environ)
        self.post_variables = self.__get_post_variables(environ)
        self.__cookie_string = environ.get("HTTP_COOKIE", None)
        self.__cookie = None
    #--------------------------------------------------------------------------
    def is_post_request(self, environ):
        if environ['REQUEST_METHOD'].upper() != 'POST':
            return False
        content_type = environ.get('CONTENT_TYPE', 
                'application/x-www-form-urlencoded')
        _logger.debug('CONTENT_TYPE is:')
        _logger.debug(content_type)
        return (content_type.startswith('application/x-www-form-urlencoded')
                or content_type.startswith('multipart/form-data'))
    #--------------------------------------------------------------------------
    def __get_get_variables(self, environ):
        get_variables = {}
        if not 'QUERY_STRING' in environ:
            _logger.error("QUERY_STRING not found in environment")
        else:
            env_copy = environ.copy()
            query = env_copy['QUERY_STRING']
            _logger.debug("QUERY_STRING is" + str(query))
            get_variables = parse_qs(query)
            _logger.debug("__get_get_variables: " +
                    "Found " + ';'.join(get_variables.keys()))
        return get_variables
    #--------------------------------------------------------------------------
    def get_get_variables(self, *field_names):
        '''
        Returns a list of values of HTTP GET variables.
        takes a variable number of arguments being the names of variables.
        Returnes a list of their values in the order of the names.
        If a variable has not been set, the value in the list is None.
        BEWARE: The returned values are FieldStorage objects since unlike with
        GET requests, their value might not necessarily be a string but could 
        be a file object or else.
        '''
        def get_variable_value(variable_hash, variable_name):
            value = variable_hash.get(variable_name, None)
            if value:
                value = escape(value[0])
            return value
        #----------------------------------------------------------------------
        values = []
        for field_name in field_names:
            field_value = get_variable_value(self.get_variables, field_name)
            values.append(field_value)
        return values
    #--------------------------------------------------------------------------
    def __get_post_variables(self, environ):
        if not self.is_post_request(environ):
            return {}
        post_form = None
        if not 'wsgi.input' in environ:
            _logger.error("'wsgi.input' not found in environment")
        else:
            _logger.debug("wsgi.input is")
            _logger.debug(environ['wsgi.input'])
            try:
                length= int(environ.get('CONTENT_LENGTH', '0'))
            except ValueError:
                length = 0
            if length != 0:
                env_copy = environ.copy()
                env_copy['QUERY_STRING'] = ''
                input = env_copy['wsgi.input']
                post_form = FieldStorage(fp=input, environ=env_copy,
                        keep_blank_values=1)
                _logger.debug("__get_post_variables: " +
                        "Found " + ';'.join(post_form.keys()))
            else:
                _logger.debug("__get_post_variables: " +
                "No post variables found")
        return post_form
    #--------------------------------------------------------------------------
    def get_post_variables(self, *field_names):
        '''
        Returns a list of values of HTTP POST variables.
        takes a variable number of arguments being the names of variables.
        Returnes a list of their values in the order of the names.
        If a variable has not been set, the value in the list is None.
        BEWARE: The returned values are FieldStorage objects since unlike with
        GET requests, their value might not necessarily be a string but could 
        be a file object or else.
        '''
        values = []
        for field_name in field_names:
            field_value = None
            if field_name in self.post_variables:
                field_value = self.post_variables[field_name]
            values.append(field_value)
        return values
    #--------------------------------------------------------------------------
    def __ensure_cookie_parsed(self):
        if self.__cookie is None:
            try:
                self.__cookie     = cookies.SimpleCookie(self.__cookie_string)
            except (cookies.CookieError, KeyError):
                __logger__.info("No cookie set")
    #--------------------------------------------------------------------------
    def get_cookie(self, name):
        '''
        Returns the value of cookie with name 'name' or None if no such cookie
        '''
        self.__ensure_cookie_parsed()
        try:
            value = self.__cookie[name]
        except(cookies.CookieError, KeyError):
            value = None
        return value
    #--------------------------------------------------------------------------
    def set_cookie(self, cookie):
        if cookie is not None:
            self.__cookie = cookie
