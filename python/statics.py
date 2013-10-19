import StringIO
import os
import sys
#------------------------------------------------------------------------------
ABS_PAGE_ROOT  = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR     = 'python'
sys.path.append(ABS_PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
#------------------------------------------------------------------------------
class Statics:

    def __init__(self, root_path = NAGA_ROOT, 
                       cfg_file_name = NAGA_ABS_ROOT + PATH_SEPARATOR  +  \
                               STATIC_FILE_PATH):
        self._logger  = logging.getLogger('Statics')
        self._content = {}
        try:
            file_object = open(cfg_file_name, 'r') 
            for line in file_object:
                content_entry = line.split(CFG_LIST_SEPARATOR)
                if len(content_entry) < 2:
                    self._logger.error("Malformed line in " + str(cfg_file_name) + 
                    " : " + str(line))
                    break
                self._content[content_entry[0]] = root_path + \
                        PATH_SEPARATOR + STATIC_DIR + PATH_SEPARATOR + \
                        content_entry[1]
                self._logger.info('Found ' + self._content[content_entry[0]])
        except IOError as ex:
            self._logger.error(ex)
        self._logger.info(self._content)
    #--------------------------------------------------------------------------
    def get(self, static_key):
        '''
        Get link to a file registered as static
        '''
        if not static_key in self._content:
            self._logger.warn("No content found for " + static_key)
            return None
        return self._content[static_key]
    #--------------------------------------------------------------------------
    def get_statics(self):
        return self._content.keys()

