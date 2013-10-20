#!/usr/bin/python
import os.path
import sys
import logging
import re
import string
import random
import hashlib
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
from configuration import ConfigurationObject
#------------------------------------------------------------------------------    
_logger = logging.getLogger("security")
#------------------------------------------------------------------------------    
def sanitize_string(string_to_sanitize):
    "Return String that does not contain any special chars except underscore"
    return re.sub('[^0-9a-zA-Z]', '_', string_to_sanitize)
#------------------------------------------------------------------------------    
def authenticate(user, passphrase):
    '''
    Check whether user is registered with password, and return false if 
    unsuccessful. If successful, return something evaluating
    to true, possibly a list of rights
    '''
    return Authenticator().authenticate(user, passphrase)
#------------------------------------------------------------------------------    
class Authenticator(ConfigurationObject):

    def __init__(self, file_name = NAGA_ABS_ROOT + USERS_FILE_PATH):
        ConfigurationObject.__init__(self, file_name)
        self._logger = logging.getLogger("Authenticator")
        self._hash_algorithm = 'sha512'
    #--------------------------------------------------------------------------    
    def authenticate(self, user, passphrase):
        [salt, hashed_passphrase] = self.get(user)
        if not salt or not hashed_passphrase:
            return False
        if self.hash_passphrase(salt, passphrase) == hashed_passphrase:
            return True
        return False
    #--------------------------------------------------------------------------    
    def add_user(self, user, passphrase):
        salt = random.choice(string.ascii_uppercase + string.ascii_lowercase
                            + string.digits)
        hashed_passphrase = self.hash_passphrase(salt, passphrase)
        self.set(user, [salt, hashed_passphrase])
    #--------------------------------------------------------------------------    
    def hash_passphrase(self, salt, passphrase):
        digester = hashlib.new(self._hash_algorithm)
        to_hash = salt + passphrase
        digester.update(to_hash.encode("utf-8"))
        return digester.hexdigest()

