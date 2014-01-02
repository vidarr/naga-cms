#!/usr/bin/python3
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
from http import cookies
#---------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR)
from naga_config import *
from configuration import ConfigurationObject
#---------------------------------------------------------------------------    
__logger__ = logging.getLogger("security")
#---------------------------------------------------------------------------    
def sanitize_string(string_to_sanitize):
    "Return String that does not contain any special chars except underscore"
    return re.sub('[^0-9a-zA-Z]', '_', string_to_sanitize)
#---------------------------------------------------------------------------    
def authenticate(user, passphrase):
    '''
    Check whether user is registered with password, and return false if 
    unsuccessful. If successful, return something evaluating
    to true, possibly a list of rights
    '''
    return Authenticator().authenticate(user, passphrase)
#---------------------------------------------------------------------------    
def get_user(cgi_variables):
    '''
    Take the HTTP GET variables as cgi.FieldStorage, look for user and 
    return the associated value
    '''
    if not CREDENTIALS_USER in cgi_variables:
        __logger__.error("No user found")
        return None
    return cgi_variables[CREDENTIALS_USER].value
#---------------------------------------------------------------------------    
def get_passphrase(cgi_variables):
    '''
    Take the HTTP GET variables as cgi.FieldStorage, look for passphrase and 
    return the associated value
    '''
    if not CREDENTIALS_PASSPHRASE in cgi_variables:
        __logger__.error("No passphrase found")
        return None
    return cgi_variables[CREDENTIALS_PASSPHRASE].value
#---------------------------------------------------------------------------    
def authenticate_cgi(cgi_variables):
    '''
    Take the HTTP GET variables as a cgi.FieldStorage, look for one 'USER' and 
    one 'PASSPHRASE' and check whether their values are valid.
    '''
    user       = get_user(cgi_variables)
    passphrase = get_passphrase(cgi_variables)
    if not user or not passphrase:
        return None
    return authenticate(user, passphrase)
#---------------------------------------------------------------------------    
def forward_credentials(cgi_variables):
    '''
    Take the HTTP GET variables as cgi.FieldStorage, look for user and 
    passphrase and create HTTP GET string to forward credentials to another CGI
    script
    '''
    user_value       = get_user(cgi_variables)
    passphrase_value = get_passphrase(cgi_variables)
    if not user_value or passphrase_value:
        __logger__.error("No credentials found")
        return None
    return ''.join([CREDENTIALS_USER, "=", user_value,
        "&", CREDENTIALS_PASSPHRASE, "=", passphrase_value])
#---------------------------------------------------------------------------    
def authenticate_cookie():
    '''
    Looks for cookies 'user' and 'passphrase' and checks whether their 
    values are valid credentials
    '''
    try:
        cookie     = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
        user       = cookie[CREDENTIALS_USER].value
        passphrase = cookie[CREDENTIALS_PASSPHRASE].value
    except (cookies.CookieError, KeyError):
        __logger__.info("session cookie not set!")
        return None
    return authenticate(user, passphrase)
#---------------------------------------------------------------------------    
def get_credential_cookie(user, passphrase):
    '''
    Returns a cookie to be sent back to the client to automatically 
    authenticate with user,passphrase
    '''
    cookie  = cookies.SimpleCookie()
    cookie[CREDENTIALS_USER] = user
    cookie[CREDENTIALS_PASSPHRASE] = passphrase
    return cookie
#---------------------------------------------------------------------------    
class Authenticator(ConfigurationObject):
    '''
    Provides several ways of checking whether a combination of 
    user/passphrase is valid or not.
    '''
    def __init__(self, file_name = NAGA_ABS_ROOT + USERS_FILE_PATH):
        ConfigurationObject.__init__(self, file_name)
        self.__logger__ = logging.getLogger("Authenticator")
        self._hash_algorithm = 'sha512'
    #-----------------------------------------------------------------------    
    def authenticate(self, user, passphrase):
        '''
        Returns rights matrix of user if user,passphrase are valid 
        credentials
        '''
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

