#!/usr/bin/python
import os.path
import sys
import logging
import re
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
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

    def __init__(self, file_name = USERS_ABS_PATH):
        ConfigurationObject.__init__(file_name)
        self._logger = logging.getLogger("Authenticator")
    #--------------------------------------------------------------------------    
    def authenticate(self, user, passphrase):
        hashed_ref_passphrase = self.get(user)
        if not hashed_ref_passphrase:
            return False


    

