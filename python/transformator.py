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
# Standard call backs to convert to html
#------------------------------------------------------------------------------
def heading(call, arg):
    return '<h>' + arg + '</h>'
#------------------------------------------------------------------------------
def listing(call, arg):
    sur_tag = 'ol'
    if call == 'ulist':
        sur_tag = 'ul'
    elements = arg.split('*')
    if len(elements) < 2:
        _logger.warn("wont build empty list from " + arg)
        return ''
    result = ['<', sur_tag, '>']
    for item in elements[1:]:
        result.append('<li>')
        result.append(item)
        result.append('</li>')
    result.append('<')
    result.extend(['</', sur_tag, '>'])
    return ''.join(result)
#------------------------------------------------------------------------------
def bold(call, arg):
    return '<b>' + arg + '</b>'
#------------------------------------------------------------------------------
def italic(call, arg):
    return '<i>' + arg + '</i>'
#------------------------------------------------------------------------------
def line_break(call, arg):
    return '<br>'
#------------------------------------------------------------------------------
def make_link(separator, ilink_prefix = ''):
    'Tada'
    def link(call, arg):
        parts = arg.partition(separator)
        (target, description) = (parts[0], parts[2])
        if call == 'ilink':
            # ilink will link to internal article
            target = ilink_prefix + target
        if description == '':
            description = target
        return '<a href="' + target + '">' + description + '</a>'
    return link
#------------------------------------------------------------------------------
def make_do_nothing(separator):
    def do_nothing(call, arg):
        return call + separator + arg
    return do_nothing
#------------------------------------------------------------------------------
class Transformator:
    #---------------------------------------------------------------------------
    def __init__(self, **params):
        self.left_marker = '['
        if 'left_marker' in params:
            self.left_marker = params['left_marker']
        self.right_marker = ']'
        if 'right_marker' in params:
            self.right_marker = params['right_marker']
        self.separator = ' '
        if 'separator' in params:
            self.separator = params['separator']
        self.lookup = {
                'heading' : heading, 
                'olist'   : listing,
                'ulist'   : listing,
                'br'      : line_break,
                'b'       : bold,
                'i'       : italic,
                'link'    : make_link(self.separator),
                'DEFAULT' : make_do_nothing(self.separator)
                }
        if 'handlers' in params:
            self.lookup = params['handlers']
        self.quoted_left_marker = self.left_marker + self.left_marker
        self.quoted_right_marker = self.right_marker + self.right_marker
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
    def escaped(self, origin_string, i):
        if i > len(origin_string) - 1:
            return None
        elif i + 1 == len(origin_string):
            None
        elif origin_string[i + 1] == origin_string[i]:
            return True
        return None
    #---------------------------------------------------------------------------
    def get_call_end_position(self, origin_string, position):
        print("Called get_call_end_position : " + origin_string)
        if len(origin_string) < 1:
            self._logger.error(origin_string + " is empty")
            return None
        level = 1
        for i in range(position, len(origin_string)):
            print (origin_string[i])
            if origin_string[i] == self.right_marker:
                print("right marker")
                if not self.escaped(origin_string, i):
                    print("level -- ")
                    level = level - 1
                    print ("level = " + str(level))
                    if level == 0:
                        return i
            elif origin_string[i] == self.left_marker:
                print ("left marker")
                if not self.escaped(origin_string, i):
                    print("level ++")
                    level = level + 1
        self._logger.error("Found no end marker")
    #---------------------------------------------------------------------------
    def treat_format_call(self, origin_string, transformed_parts):
        inner_part = None
        position = 0
        position = self.get_call_end_position(origin_string, position)
        if position == None:
            self._logger.error("Could not isolate call part from " +
                    origin_string)
            return None
        inner_part = origin_string[:position]
        self._logger.info("got format call " + inner_part)
        if position + 1 == len(origin_string):
            rest = ''
        else:
            rest = origin_string[position + 1:]
        call_parts = inner_part.partition(self.separator)
        if call_parts[0] == '':
            self._logger.error("error when trying to split " + inner_part)
            return None
        arguments = self.transform(call_parts[2])
        if call_parts[0] in self.lookup:
            transformed_parts.append(self.lookup[call_parts[0]](call_parts[0],
                arguments))
        else:
            transformed_parts.append(self.lookup['DEFAULT'](call_parts[0],
                arguments))
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

