#!/usr/bin/python3
import datetime
import os.path
import sys
import xml.etree.ElementTree as ET
import logging
import re
#------------------------------------------------------------------------------
PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import nagaUtils
#------------------------------------------------------------------------------
_logger = logging.getLogger('transformator')
#------------------------------------------------------------------------------
class Transformator:
    #---------------------------------------------------------------------------
    def __init__(self):
        self.left_marker = '['
        self.quoted_left_marker = self.left_marker + self.left_marker
        self.right_marker = ']'
        self.quoted_right_marker = self.right_marker + self.right_marker
        self.separator = ' '
        self.lookup = {}
        self._logger = logging.getLogger('Transformator')
    #---------------------------------------------------------------------------
    def register_callback(self, identifier, callback):
        self.lookup[identifier] = callback
    #---------------------------------------------------------------------------
    def _collapse_string(self, transformed_parts):
        stripped_parts = [x.replace(self.quoted_left_marker,
            self.left_marker).replace(
                self.quoted_right_marker, self.right_marker)
            for x in transformed_parts]
        return ''.join(stripped_parts)
    #---------------------------------------------------------------------------
    def treat_format_call(self, origin_string, transformed_parts):
        inner_part = None
        rest = ''
        position = 0
        while inner_part == None:
            position = origin_string.find(self.right_marker, position)
            if position < 0:
                self._logger.error(origin_string + 
                        " does not contain end markers ")
                return None
            if len(origin_string) == position + 1:
                inner_part = origin_string[:-1]
            else:
                if origin_string[position + 1] == self.right_marker:
                    position = position + 1
                else:
                    # We found the end - now cut it out
                    inner_part = origin_string[:position]
                    rest = origin_string[position + 1:]
        inner_part.replace(self.quoted_left_marker,
                self.left_marker).replace(self.quoted_right_marker,
                        self.right_marker)
        self._logger.info("got format call " + inner_part)
        print("got format call " + inner_part)
        call_parts = inner_part.partition(self.separator)
        if call_parts[0] == '':
            self._logger.error("error when trying to split " + inner_part)
            return None
        if call_parts[0] in self.lookup:
            transformed_parts.append(self.lookup[call_parts[0]](inner_part))
        else:
            transformed_parts.append(inner_part)
        return rest
    #---------------------------------------------------------------------------
    def transform(self, origin_string):
        if not type(origin_string) == type('string'):
            return '' 
        transformed_string = []
        parts = []
        while origin_string != None:
            parts = origin_string.partition(self.left_marker)
            transformed_string.append(parts[0])
            if parts[1] == '':
                return self._collapse_string(transformed_string)
            if parts[2].startswith(self.left_marker):
                # We remove second marker and just push the marker once 
                transformed_string.append(self.left_marker)
                parts = parts[2].partition(self.left_marker)
                origin_string = parts[2]
            else:
                # BINGO - we got a format call
                origin_string = self.treat_format_call(parts[2], 
                        transformed_string)

#         parts = origin_string.partition(self.left_marker)
#         while parts[1] != '':
#             if parts[0].startswith(self.left_marker):
#                 # Non-caught case: String started with '[' 
#                 # we encountered a quoted marker...
#                 transformed_string.append(self.left_marker)
#                 # if parts[2] == '' the original string ended in '[[[' - no
#                 # sense whatsoever ...
#                 if parts[2] == '':
#                     self._logger.error("String seems to end in [[[ : " +
#                             origin_string)
#                     return None
#                 stripped_string = parts[2]
#                 stripped_string = stripped_string[1:]
#                 converted_string_parts = treat_call(stripped_string)
#                 if converted_string_parts == None:
#                     self._logger.error("right marker missing " + origin_string)
#                     return None
        # TODO: Implement further
    #---------------------------------------------------------------------------
    def treat_call(self, stripped_string):
        parts = stripped_string.partition(self.right_marker)
        if parts[1] == '':
            return None
        call_parts = parts[0].partition(self.separator)
        handler = call_parts[0]
        if handler in self.lookup:
            parts[0] = self.lookup[handler](call_parts[2])
        return [parts[0], parts[2]]









        # string_parts = origin_string.split(self.left_marker)
        # string_parts.reverse()
        # if len(string_parts) < 1:
        #    self._logger.error("Parse error on " + origin_string + " at " + string_parts)
        #    print("Parse error on " + origin_string + " at " + string_parts)
        #    return None
        # transformed_string.append(string_parts.pop())
        # while len(string_parts) > 0:
        #     next_part = string_parts.pop()
        #     if next_part == '':
        #         transformed_string.append(self.left_marker)
        #     else:
        #         inner_parts = []
        #         found_end = False
        #         parts = next_part.split(self.right_marker)
        #         parts.reverse()
        #         # we ignore the case of an '[[]'
        #         if len(parts) < 1:
        #             self._logger.error("Parse error on " + origin_string + " at " + parts)
        #             print("Parse error on " + origin_string + " at " + parts)
        #             return None
        #         inner_parts.append(parts.pop())
        #         while not found_end and len(parts) > 0:
        #             part = parts.pop()
        #             if part == '': 
        #                 inner_parts.append(self.right_marker)
        #             else:
        #                 inner_parts.append(part)
        #                 found_end = True
        #         if not found_end:
        #             self._logger.error("Parse error on " + origin_string + " found opening marker before closing marker")
        #             print("Parse error on " + origin_string + " found opening marker before closing marker")
        #             return None
        #         # Discover handler and hand over to handler
        #         handler = inner_parts[0]
        #         result = ''.join(inner_parts)
        #         if handler in self.lookup:
        #             result = self.lookup[handler](result)
        #         else:
        #             self._logger.warn("No handler for " + handler + " found")
        #         transformed_string.append(result)
        #         # '' have been quoted ']', we do not check for single '[' -
        #         # they should not appear at this point ...
        #         rest = [self.right_marker if x == ''  else x for x in parts]
        #         transformed_string.append(''.join(rest))
        # return ''.join(transformed_string)
        # while len(origin_string) > 0:
        #     tokens_before = self.left_separator_pattern.split(origin_string, 1)
        #     if len(tokens_before) < 2:
        #         transformed_string.append(origin_string)
        #         return self.collapse_string(transformed_string)
        #     transformed_string.append(self.strip_escapes(tokens_before[0]))
        #     tokens_after = self.right_separator_pattern.split(tokens_before[1], 1)
        #     if len(tokens_after) < 2:
        #         self._logger.error("No closing separator found in " +
        #                 tokens_before[1])
        #         return self.collapse_string(transformed_string)
        #     origin_string = tokens_after[1]
        #     transform_tokens = tokens_after[0].split(self.separator)
        #     if len(transform_tokens) < 1 or not transform_tokens[0] in self.lookup:
        #         transformed_string.append(self.separator.join(transform_tokens))
        #     else:
        #         handler = self.lookup[transform_tokens[0]]
        #         transformed_string.append(handler(transform_tokens))
        # return self.collapse_string(transformed_string)
    #---------------------------------------------------------------------------
    def strip_escapes(self, esc_string):
        return esc_string.replace(self.left_marker + self.left_marker,
                self.left_marker).replace(self.right_marker + self.right_marker,
                        self.right_marker)
    #---------------------------------------------------------------------------
    def collapse_string(self, result_string_parts):
        print("Got " + ' '.join(result_string_parts))
        return ''.join([self.strip_escapes(token) for token in 
            result_string_parts])


