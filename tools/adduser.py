#!/usr/bin/python3 
import os.path
import sys
import logging
import re
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import security
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("adduser.py USER PASSPHRASE", file=sys.stderr)
        sys.exit(1)
    authenticator = security.Authenticator()
    authenticator.add_user(sys.argv[1], sys.argv[2])
    authenticator.to_file()
