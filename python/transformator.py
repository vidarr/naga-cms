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
import store
#------------------------------------------------------------------------------
_logger = logging.getLogger('transformator')
#------------------------------------------------------------------------------
# 'CONSTANTS'
#------------------------------------------------------------------------------
_DEFAULT = 'DEFAULT'   # Key for default call back
#------------------------------------------------------------------------------
# Standard call backs to convert to html
#------------------------------------------------------------------------------
def heading(call, arg):
    '''
    Callback: Format heading.
    '''
    return '<h1>' + arg + '</h1>'
#------------------------------------------------------------------------------
def listing(call, arg):
    '''
    Callback: Format list in two flavors:
    If call == 'ulist', format unordered list.
    else format ordered list
    '''
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
    result.extend(['</', sur_tag, '>'])
    return ''.join(result)
#------------------------------------------------------------------------------
def bold(call, arg):
    '''
    Callback: Format bold
    '''
    del call # Just to get rid of 'Unused arg' warning
    return '<b>' + arg + '</b>'
#------------------------------------------------------------------------------
def italic(call, arg):
    '''
    Callback: Format italcs.
    '''
    del call # Just to get rid of 'Unused arg' warning
    return '<i>' + arg + '</i>'
#------------------------------------------------------------------------------
def line_break(call, arg):
    '''
    Callback: Format line break.
    '''
    del call, arg # Just to get rid of 'Unused arg' warning
    return '<br>'
#------------------------------------------------------------------------------
def code(call, arg):
    '''
    Callback: Format code.
    '''
    del call # Just to get rid of 'Unused arg' warning
    return ''.join(['<code>', arg, '</code>'])
#------------------------------------------------------------------------------
def make_link(separator, internal_link_prefix='', internal_link_postfix=''):
    '''
    Returns a function to be used as callback to format links.
    The callback will distinuish between internal and external links.
    An External link will be taken 'as is'.
    An Internal link will be surrounded with internal_link_prefix and
    internal_link_postfix.
    '''
    def link(call, arg):
        '''
        Callback to format links.
        Expects one or several arguments.
        The first argument is the link target.
        If additional arguments are given, they will be used as link text to
        appear in the formatted output, otherwise the link target will act as
        text.
        If the link target is of the form PROTOCOL://SOMETHING , the link
        is interpreted as external link and taken as is.
        Otherwise, the link target will be interpreted as internal link and
        altered to point to internal resources. Refer to the code for details,
        please!
        '''
        del call # Just to get rid of 'Unused arg' warning
        parts = arg.partition(separator)
        (target, description) = (parts[0], parts[2])
        if nagaUtils.invalid_url(target):
            # target does not match some dns name
            target_substitute = target
            target = ''.join([internal_link_prefix, target, '.',
                XML_FILE_EXTENSION, internal_link_postfix])
        if description == None or description == '':
            description = target_substitute
        return ''.join(['<a href="', target, '">', description,
            '</a>'])
    return link
#------------------------------------------------------------------------------
# Formatters for treating store links
def format_image_html(target, description):
    '''
    Formats HTML for an image link
    '''
    postfix = '" ' + IMAGE_OPTIONS + '/>'
    prefix = ''
    if description != None and description != '':
        prefix = '<table><tr><td>'
        postfix = ''.join([postfix,
            '</td></tr><tr><td><b>Image:</b> ',
            description, '</td></tr></table>'])
    prefix = ''.join(['<div class="center">', prefix, '<img src="'])
    postfix = postfix + '</div>'
    return ''.join([prefix, target, postfix])
#--------------------------------------------------------------------------
def format_file_html(target, description):
    '''
    Formats HTML for a file link
    '''
    if description == None or description == '':
        description = target
    return ''.join(['<a href="', target, '">', description, '</a>'])
#--------------------------------------------------------------------------
def make_store_link(separator, store_object, formatter):
    '''
    Returns a function to be used as callback to format images.
    The callback will distinuish between internal and external image links.
    An External image link will be taken 'as is'.
    An Internal image link will be surrounded with internal_link_prefix and
    internal_link_postfix.
    '''
    def link(call, arg):
        '''
        Callback to format image links.
        Expects one or several arguments.
        The first argument is the link target.
        If additional arguments are given, they will be used as image subscript.
        If the link target is of the form PROTOCOL://SOMETHING , the link
        is interpreted as external link and taken as is.
        Otherwise, the link target will be interpreted as internal link and
        altered to point to internal resources. Refer to the code for details,
        please!
        '''
        del call # Just to get rid of 'Unused arg' warning
        parts = arg.partition(separator)
        (target, description) = (parts[0], parts[2])
        if nagaUtils.invalid_url(target):
            # target does not match some dns name
            # description = target
            target_uri = store_object.get_uri(target)
            if target_uri == None:
                return ''.join([
                    '<div class="center"><code>', target,
                    '</code> not found</div>'])
            target = target_uri
        return formatter(target, description)
    return link
#------------------------------------------------------------------------------
def make_do_nothing(separator):
    '''
    Create callback to handle DEFAULT case, i.e. handle an unknown format string
    '''
    def do_nothing(call, arg):
        '''
        Callback to format unknown format strings.
        Just returns call + separator + arg
        '''
        return call + separator + arg
    return do_nothing
#------------------------------------------------------------------------------
def make_default_transformator():
    '''
    Creates a Transformator to format to HTML
    '''
    transformator = Transformator()
    link_prefix = NAGA_ROOT + PATH_SEPARATOR + SHOW_RELATIVE_PATH + '?' + \
            'type=article&content='
    transformator.register_callback('link',
            make_link(MARKUP_LINK_SEPARATOR, link_prefix))
    transformator.register_callback('image',
            make_store_link(MARKUP_LINK_SEPARATOR,
                store.get_store(STORE_TYPE_IMAGE), format_image_html))
    transformator.register_callback('file',
            make_store_link(MARKUP_LINK_SEPARATOR,
                store.get_store(STORE_TYPE_FILE), format_file_html))
    return transformator
#------------------------------------------------------------------------------
class Transformator(object):
    '''
    Transforms text from naga formatting to something different, e.g. HTML.
    Naga formatting is done by inserting format strings into plain text.
    For example:

    [heading An example]

    This is a [b simple] example. See [link https://ubeer.org [b ubeer.org] ].

    Format strings are composed thus:
         [FROMAT_STRING ARG1 ... ]

    If you intend to use the chars '[' or ']' they must be
    quoted by doubling them, i.e:

    A .[ needs to be [b escaped] like .[.[.

    Format strings can be nested.

    [link https://ubeer.org [b ubeer] ] or [link https://ubeer.org [b ubeer]]

    is correct.
    '''
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
                'c'       : code,
                'link'    : make_link(self.separator),
                _DEFAULT : make_do_nothing(self.separator)
                }
        if 'handlers' in params:
            self.lookup = params['handlers']
        self.quote_char = '.'
        self.quoted_left_marker = self.quote_char + self.left_marker
        self.quoted_right_marker = self.quote_char + self.right_marker
        self.__logger = logging.getLogger('Transformator')
    #---------------------------------------------------------------------------
    def register_default_callback(self, callback):
        '''
        Register the callback to handle unknown format strings.
        '''
        self.lookup[_DEFAULT] = callback
    #---------------------------------------------------------------------------
    def register_callback(self, identifier, callback):
        '''
        Register callback with a format string.
        '''
        self.lookup[identifier] = callback
    #---------------------------------------------------------------------------
    def __replace_chars(self, input):
        return re.sub('[\r\n]', '', input)
    #---------------------------------------------------------------------------
    def __collapse_string(self, transformed_parts):
        '''
        Collect strings where all format calls have been treated and
        unite it to one return string.
        '''
        return ''.join(transformed_parts)
    #---------------------------------------------------------------------------
    def __unquote_string(self, string_to_unquote):
        '''
        Repaces escaped characters within string_to_unquote by the actual chars.
        '''
        return string_to_unquote.replace(
                self.quoted_left_marker, self.left_marker).replace(
                self.quoted_right_marker, self.right_marker)
    #---------------------------------------------------------------------------
    def escaped(self, origin_string, i):
        '''
        Checks whether a character at position i in string origin_string is
        escaped. This is done in a generic way, it is only checked whether the
        character at position i is preceded by '.'.
        '''
        if i > 0:
            if origin_string[i - 1] == self.quote_char:
                return True
        return None
    #---------------------------------------------------------------------------
    def get_call_end_position(self, origin_string, position):
        '''
        Finds end of format string and returns its position.
        '''
        self.__logger.info("looking at " + origin_string[position:])
        if len(origin_string) < 1:
            self.__logger.error(origin_string + " is empty")
            return None
        level = 1
        for i in range(position, len(origin_string)):
            self.__logger.debug("position " + str(i) + " char " +
                    origin_string[i])
            if origin_string[i] == self.right_marker:
                if not self.escaped(origin_string, i):
                    level = level - 1
                    self.__logger.debug(origin_string[i] + " not escaped - decreatsing to " + str(level))
                    if level == 0:
                        return i
                else:
                    self.__logger.debug(origin_string[i] + " escaped")
            elif origin_string[i] == self.left_marker:
                if not self.escaped(origin_string, i):
                    level = level + 1
                    self.__logger.debug(origin_string[i] + " not escaped - increasing to " + str(level))
                else:
                    self.__logger.debug(origin_string[i] + " escaped")
        self.__logger.error("Found no end marker")
        return None
    #---------------------------------------------------------------------------
    def treat_format_call(self, origin_string, transformed_parts):
        '''
        Assumes that origin_string starts with a format call followed by some
        'rest'.
        Takes the format call, cuts it off the origin_string, treats it and
        appends the return value of the format call to transformed_parts.
        Returns the remainder of origin_string.
        '''
        inner_part = None
        position = 0
        position = self.get_call_end_position(origin_string, position)
        if position == None:
            self.__logger.error("Could not isolate call part from " +
                    origin_string)
            return None
        inner_part = origin_string[:position]
        self.__logger.debug("got format call " + inner_part)
        rest = origin_string[position + 1:]
        call_parts = inner_part.partition(self.separator)
        if call_parts[0] == '':
            self.__logger.error("error when trying to split " + inner_part)
            return None
        arguments = self.__transform(call_parts[2])
        if call_parts[0] in self.lookup:
            transformed_parts.append(self.lookup[call_parts[0]](call_parts[0],
                arguments))
        else:
            transformed_parts.append(self.lookup[_DEFAULT](call_parts[0],
                arguments))
        return rest
    #---------------------------------------------------------------------------
    def __transform(self, origin_string):
        '''
        Takes a string containing format strings and transforms it.
        Does not treat escapes.
        '''
        if not type(origin_string) == type('string'):
            return ''
        transformed_string = []
        parts = []
        start_position = 0
        while origin_string != None:
            self.__logger.debug("transform: Looking at " + origin_string[start_position:])
            position = origin_string.find(self.left_marker, start_position)
            if position < 0:
                # Not found
                self.__logger.debug("transform: No start marker found in " + origin_string[start_position:])
                modified_string = self.__replace_chars(origin_string)
                transformed_string.append(modified_string)
                return self.__collapse_string(transformed_string)
            if self.escaped(origin_string, position):
                start_position = position + 1
                self.__logger.debug("transform: Escaped " +
                        origin_string[position] + " continuing at " +
                        str(position))
            else:
                # Got format call
                self.__logger.debug("transform: Got call " + origin_string[position:])
                modified_string = self.__replace_chars(origin_string[:position])
                transformed_string.append(modified_string)
                remainder = origin_string[position + 1:]
                if remainder == '':
                    return self.__collapse_string(transformed_string)
                origin_string = self.treat_format_call(remainder, transformed_string)
                start_position = 0
        return self.__collapse_string(transformed_string)
    #---------------------------------------------------------------------------
    def transform(self, origin_string):
        '''
        Takes a string containing format strings and transforms it.
        '''
        return self.__unquote_string(self.__transform(origin_string))
