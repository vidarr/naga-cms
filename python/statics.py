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
import os
import sys
from os.path import join
#------------------------------------------------------------------------------
ABS_PAGE_ROOT  = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR     = 'python'
sys.path.append(ABS_PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
#------------------------------------------------------------------------------
class Statics:

    def __init__(self, root_path = NAGA_ROOT, 
                       cfg_file_name = join(NAGA_ABS_ROOT, STATIC_FILE_PATH)):
        self._logger  = logging.getLogger('Statics')
        self._content = {}
        self._order   = []
        try:
            file_object = open(cfg_file_name, 'r') 
            for line in file_object:
                content_entry = line.split(CFG_LIST_SEPARATOR)
                if len(content_entry) < 2:
                    self._logger.error("Malformed line in " + str(cfg_file_name) + 
                    " : " + str(line))
                    break
                self._content[content_entry[0]] = join(root_path, STATIC_DIR,
                        content_entry[1])
                self._order.append(content_entry[0])
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
        return self._order

