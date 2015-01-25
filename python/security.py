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
'''
Provides authentication mechanisms, currently via cookies,
as well as helper functions.
'''
import os.path
import sys
import logging
import re
import string
import random
import hashlib
from cgi import escape
from http import cookies
#---------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR)
from naga_config import *
from configuration import ConfigurationObject
from naga_wsgi import serialize_cookie, wsgi_get_get_variables
#---------------------------------------------------------------------------    
__logger__ = logging.getLogger("security")
#---------------------------------------------------------------------------    
def sanitize_string(string_to_sanitize, **options):
    '''
    Return String that does not contain any special chars except underscore.
    If keep_dot=True, the string might contain dots as well.
    '''
    keep_dot = False
    if 'keep_dot' in options:
        keep_dot = options['keep_dot']
    if not keep_dot:
        return re.sub('[^0-9a-zA-Z]', '_', string_to_sanitize)
    return re.sub('[^0-9a-zA-Z.]', '_', string_to_sanitize)
#---------------------------------------------------------------------------    
def authenticate(user, passphrase):
    '''
    Check whether user is registered with password, and return false if 
    unsuccessful. If successful, return something evaluating
    to true, possibly a list of rights
    '''
    return Authenticator().authenticate(user, passphrase)
#---------------------------------------------------------------------------    
def get_user(environment):
    '''
    Takes an environment, and tries to extract the user name from the 
    GET request string contained within, return the associated value
    '''
    user = wsgi_get_get_variables(environment, CREDENTIALS_USER)[0]
    if not user:
        __logger__.error("No user found")
    else:
        __logger__.info("Got user from GET variables:" + user)
    return user
#---------------------------------------------------------------------------    
def get_passphrase(environment):
    '''
    Takes an environment, and tries to extract the password from the 
    GET request string contained within, return the associated value
    '''
    passphrase = wsgi_get_get_variables(environment, CREDENTIALS_PASSPHRASE)[0]
    if not passphrase:
        __logger__.error("No passphrase found")
    return passphrase
#---------------------------------------------------------------------------    
def authenticate_cookie(environ):
    '''
    Looks for cookies 'user' and 'passphrase' and checks whether their 
    values are valid credentials
    '''
    if not environ:
        __logger__.info("environ not given")
        return None
    try:
        cookie     = cookies.SimpleCookie(environ["HTTP_COOKIE"])
        __logger__.info("Cookie is " + environ['HTTP_COOKIE'])
        user       = cookie[CREDENTIALS_USER].value
        passphrase = cookie[CREDENTIALS_PASSPHRASE].value
    except (cookies.CookieError, KeyError):
        __logger__.info("session cookie not set!")
        return None
    return authenticate(user, passphrase)
#---------------------------------------------------------------------------    
def get_credential_cookies(user, passphrase):
    '''
    Returns a cookie to be sent back to the client to automatically 
    authenticate with user,passphrase
    '''
    cookie  = cookies.SimpleCookie()
    cookie[CREDENTIALS_USER]           = user
    cookie[CREDENTIALS_USER]['secure'] = True
    cookie[CREDENTIALS_PASSPHRASE]     = passphrase
    cookie[CREDENTIALS_PASSPHRASE]['secure'] = True
    return cookie
#---------------------------------------------------------------------------    
def get_logout_cookie():
    '''
    Returns a cookie with invalid username and password
    '''
    cookie  = cookies.SimpleCookie()
    cookie[CREDENTIALS_USER]       = ''
    cookie[CREDENTIALS_USER]['expires']       = 0
    cookie[CREDENTIALS_PASSPHRASE] = ''
    cookie[CREDENTIALS_PASSPHRASE]['expires'] = 0
    return cookie
#---------------------------------------------------------------------------    
def set_cookie_for_current_request(environ, cookie):
    '''
    When setting cookie, it will become active only for the next request.
    This 'sets' the cookie already for current request
    '''
    environ["HTTP_COOKIE"] = serialize_cookie(cookie)
#---------------------------------------------------------------------------    
class Authenticator(ConfigurationObject):
    '''
    Provides several ways of checking whether a combination of 
    user/passphrase is valid or not.
    '''
    def __init__(self, file_name=
            os.path.join(NAGA_ABS_ROOT, USERS_FILE_PATH)):
        ConfigurationObject.__init__(self, file_name)
        self.__logger__ = logging.getLogger("Authenticator")
        self._hash_algorithm = 'sha512'
    #-----------------------------------------------------------------------    
    def authenticate(self, user, passphrase):
        '''
        Returns rights matrix of user if user,passphrase are valid 
        credentials
        '''
        if not user or not passphrase:
            self.__logger__.error("Too few arguments given")
            return False
        pass_infos = self.get(user)
        if not pass_infos:
            self.__logger__.error("User " + user + " not registered")
            return False
        [salt, hashed_passphrase] = pass_infos
        if not salt or not hashed_passphrase:
            self.__logger__.error("Could not authenticate user " + user)
            return False
        if self.hash_passphrase(salt, passphrase) == hashed_passphrase:
            self.__logger__.info("Authenticated user " + user)
            return True
        self.__logger__.error("Could not authenticate user " + user + 
                " - wrong passphrase")
        return False
    #-----------------------------------------------------------------------    
    def add_user(self, user, passphrase):
        salt = random.choice(string.ascii_uppercase + string.ascii_lowercase
                            + string.digits)
        hashed_passphrase = self.hash_passphrase(salt, passphrase)
        self.set(user, [salt, hashed_passphrase])
    #-----------------------------------------------------------------------    
    def hash_passphrase(self, salt, passphrase):
        digester = hashlib.new(self._hash_algorithm)
        to_hash = salt + passphrase
        digester.update(to_hash.encode("utf-8"))
        return digester.hexdigest()

