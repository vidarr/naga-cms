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
import logging
from cgi import parse_qs, escape, FieldStorage
#------------------------------------------------------------------------------
_logger = logging.getLogger("wsgi_naga")
#------------------------------------------------------------------------------
def serialize_cookie(cookie):
    return cookie.output(header='', sep=';  ')
#------------------------------------------------------------------------------
def is_post_request(environ):
    if environ['REQUEST_METHOD'].upper() != 'POST':
        return False
    content_type = environ.get('CONTENT_TYPE', 
            'application/x-www-form-urlencoded')
    _logger.debug('CONTENT_TYPE is:')
    _logger.debug(content_type)
    return (content_type.startswith('application/x-www-form-urlencoded')
            or content_type.startswith('multipart/form-data'))
#------------------------------------------------------------------------------
def wsgi_get_get_variables(environ, *field_names):
    '''
    Tries to extract all GET variables whose names are given in field_names
    and return their content as a list
    '''
    values = []
    if not 'QUERY_STRING' in environ:
        _logger.error("QUERY_STRING not found in environment")
        values = [None for i in field_names]
    else:
        _logger.debug("QUERY_STRING is")
        _logger.debug(environ['QUERY_STRING'])
        get_variables = parse_qs(environ['QUERY_STRING'])
        for field_name in field_names:
            field_value = get_variables.get(field_name, None)
            if field_value:
                field_value = escape(field_value[0])
            values.append(field_value)
    return values
#------------------------------------------------------------------------------
def wsgi_get_post_variables(environ, *field_names):
    '''
    Tries to extract all GET variables whose names are given in field_names
    and return their content as a list. 
    BEWARE: The returned values are FieldStorage objects since unlike with
    GET requests, their value might not necessarily be a string but could 
    be a file object or else.
    '''
    assert is_post_request(environ)
    values = []
    if not 'wsgi.input' in environ:
        _logger.error("'wsgi.input' not found in environment")
        values = [None for i in field_names]
    else:
        _logger.debug("wsgi.input is")
        _logger.debug(environ['wsgi.input'])
        try:
            length= int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length= 0
        if length!=0:
            env_copy = environ.copy()
            env_copy['QUERY_STRING'] = ''
            input = environ['wsgi.input']
            post_form = FieldStorage(fp=input,
                    environ=env_copy,
                    keep_blank_values=1)
        for field_name in field_names:
            field_value = None
            if field_name in post_form:
                field_value = post_form[field_name]
            values.append(field_value)
    return values
#------------------------------------------------------------------------------
def wsgi_create_response(start_response_callback, response_body, **options):
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

