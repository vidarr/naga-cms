import io
import os
import sys

ABS_PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(ABS_PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import nagaUtils

LOG_LEVEL = ['ERROR', 'WARNING', 'INFO', 'DEBUG']

default_logger = None

def log(log_level, message):
    Logger.get_logger().log(log_level, message)

class Logger:

    def __init__(self, file_name, log_level = LOG_INFO):
        self.file_handle = open(file_name, 'a+')
        self.log_level   = log_level

    def log(self, log_level, message):
        if log_level <= self.log_level:
            self.file_handle.write(nagaUtils.get_timestamp_now())
            self.file_handle.write(' - ')
            self.file_handle.write(LOG_LEVEL[log_level])
            self.file_handle.write(' - ')
            self.file_handle.write(message)
            self.file_handle.write(LINEBREAK)
            self.file_handle.flush()

    @classmethod
    def get_logger(cls):
        if default_logger == None:
            return cls(ABS_PAGE_ROOT + PATH_SEPARATOR + '..' + 
                    PATH_SEPARATOR + '..' + LOG_FILE_PATH, LOG_LEVEL)
        return default_logger


