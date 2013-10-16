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



