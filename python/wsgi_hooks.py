#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2013, 2014 Michael J. Beer <michael.josef.beer@googlemail.com>
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
import io
import os
import sys
import logging
#------------------------------------------------------------------------------
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
from security import authenticate_cookie
import naga_wsgi
import page
#------------------------------------------------------------------------------
class EnsureAuthenticatedHook:
    '''
    Checks wether a user is logged in and outputs an 'access denied' if not
    '''
    def __init__(self, chained_hook):
        self.__chained_hook = chained_hook
    #-----------------------------------------------------------------------    
    def __call__(self, request, start_response):
        response = None
        if not authenticate_cookie(request):
            page_object = page.Page(request) 
            page_object.set_content('''<h1>Authentication failure</h1>
                    You must be logged in to access this part''')
            response = naga_wsgi.create_response(start_response, \
                    page_object.get_html())
        else:
            response = self.__chained_hook(request, start_response)
        return response
#------------------------------------------------------------------------------
def __call__(chained_hook):
    return EnsureAuthenticatedHook(chained_hook)
#------------------------------------------------------------------------------
class ErrorCatchingHook:
    '''
    Catches Exceptions raised during web page creation
    '''
    def __init__(self, chained_hook):
        self.__chained_hook = chained_hook
        self.__logger = logging.getLogger('ErrorCatchingHook')
    #-----------------------------------------------------------------------    
    def __call__(self, request, start_response):
        response = None
        try:
            response = self.__chained_hook(request, start_response)
        except Exception as exception:
            self.__logger.exception(exception)
            page_object = page.Page(request) 
            page_object.set_content('''<h1>Internal Error</h1>
Something went wrong:''' + str(exception))
            response = naga_wsgi.create_response(start_response, \
                    page_object.get_html())
        return response
#------------------------------------------------------------------------------
def __call__(chained_hook):
    return ErrorCatchingHook(chained_hook)
