#!/usr/bin/python
import traceback
import os.path
import sys
import xml.etree.ElementTree as ET
from   collections import deque
import logging
from io import BytesIO
#------------------------------------------------------------------------------    
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import page
import nagaUtils
#------------------------------------------------------------------------------    
_logger = logging.getLogger("rss")
#------------------------------------------------------------------------------    
def item_from_xml_tree(xml_tree):
   if xml_tree.tag != 'item':
       raise Exception(xml_tree.__str__())
   item = Item()
   for node in xml_tree:
       _logger.debug( "Item.from_xml_tree: " + str(ET.tostring(node,
            encoding = ENCODING)))
       if node.tag == 'title':
           item.set_title(node.text)
       elif node.tag == 'description':
           item.set_description(node.text)
       elif node.tag == 'link':
           item.set_link(node.text)
       elif node.tag == 'guid':
           item.set_guid(node.text)
       elif node.tag == 'pubDate':
           item.set_pub_date(node.text)
       else:
           _logger.warning("Parsing RSS/Item: Unknown tag: " +
               node.tag)
   _logger.debug( "Got " + item.__str__())
   return item
#------------------------------------------------------------------------------    
def channel_from_xml_tree(xml_tree):
    if not xml_tree.tag == 'channel':
        raise Exception(xml_tree.__str__())
    channel = Channel()
    for item in xml_tree:
        _logger.debug( "Channel.from_xml: " + str(ET.tostring(item)))
        if item.tag == 'title':
            channel.set_title(item.text)
        elif item.tag == 'description':
            channel.set_description(item.text)
        elif item.tag == 'link':
            channel.set_link(item.text)
        elif item.tag == 'lastBuildDate':
            channel.set_last_build_date(item.text)
        elif item.tag == 'pubDate':
            channel.set_pub_date(item.text)
        elif item.tag == 'item':
            #try:
            channel.add_item(item_from_xml_tree(item))
            # except Exception as ex:
            #     _logger.debug( "Channel.from_xml: Exception occured" + ex.__str__())
            _logger.debug( "Read channel " + channel.get_title()) 
    return channel
#==============================================================================    
class Rss:

    def __init__(self, file_name = ""):
        self.file_name = file_name
        self.channels  = []
        self.logger        = logging.getLogger("Rss")
        if file_name != "":
            try:
                self.from_file()
            except Exception as ex:
                self.logger.warning("Rss.__init__: " + ex.__str__() + ' ' +
                        traceback.format_exc(20))
    #-------------------------------------------------------------------------- 
    def from_file(self):
        if self.file_name == "":
            raise IOError("File name not set")
        try:
            rss_file = open(self.file_name, "r")
        except IOError:
            self.logger.info("Rss.from_file: File does not exist")
            return 
        rss_content = rss_file.read()
        rss_file.close()
        if rss_content:
            self.from_xml(rss_content)
        else:
            self.logger.debug( "Rss.from_file: File empty")
        self.logger.debug( "Rss.from_file: Read " + self.file_name)
    #-------------------------------------------------------------------------- 
    def from_xml(self, rss_content):
        xml_tree = ET.fromstring(rss_content)
        if xml_tree.tag != 'rss':
            raise Exception(xml_tree.__str__())
        for node in xml_tree:
            if node.tag == 'channel':
                channel = channel_from_xml_tree(node)
                self.add_channel(channel)
    #-------------------------------------------------------------------------- 
    def add_channel(self, chan):
        self.channels.append(chan)
    #-------------------------------------------------------------------------- 
    def remove_channel(self, chan):
        self.channels.remove(chan)
    #-------------------------------------------------------------------------- 
    def get_channels(self):
        return self.channels
    #-------------------------------------------------------------------------- 
    def to_xml(self):
        xml_tree = self.to_xml_tree()
        return ET.tostring(xml_tree, encoding = ENCODING)
    #-------------------------------------------------------------------------- 
    def to_html(self):
        html = []
        for channel in self.channels:
            html.append(channel.to_html())
        html_string = ''.join(html)
        return html_string
    #-------------------------------------------------------------------------- 
    def to_file(self):
        if self.file_name == "":
            raise IOError("File name not set")
        rss_file = open(self.file_name, 'wb')
        rss_file.write(self.to_xml())
        rss_file.close()
        self.logger.debug( "Rss.to_file: Wrote " + self.file_name)
    #-------------------------------------------------------------------------- 
    def to_xml_tree(self):
        xml_tree = ET.Element('rss', {'version' : '2.0'})
        for chan in self.channels:
            xml_tree.append(chan.to_xml_tree())
        return xml_tree
#==============================================================================    
class Item:

    def __init__(self):
        self.title         = ""
        self.description   = ""
        self.link          = ""
        self.pub_date      = None
        self.guid          = None
        self.logger        = logging.getLogger("Item")
    #-------------------------------------------------------------------------- 
    def set_title(self, title):
        self.title = title
    #-------------------------------------------------------------------------- 
    def get_title(self):
        return self.title
    #-------------------------------------------------------------------------- 
    def set_description(self, description):
        self.description = description
    #-------------------------------------------------------------------------- 
    def get_description(self):
        return self.description
    #-------------------------------------------------------------------------- 
    def set_link(self, link):
        self.link = link
    #-------------------------------------------------------------------------- 
    def get_link(self):
        return self.link
    #-------------------------------------------------------------------------- 
    def get_guid(self):
        if self.guid:
            return self.guid
        return self.title + '-' + nagaUtils.get_timestamp_now()
    #-------------------------------------------------------------------------- 
    def set_guid(self, guid):
        self.guid = guid
    #-------------------------------------------------------------------------- 
    def set_pub_date(self, pub_date):
        self.pub_date = pub_date
    #-------------------------------------------------------------------------- 
    def get_pub_date(self):
        if self.pub_date:
            return self.pub_date
        return nagaUtils.get_timestamp_now()
    #-------------------------------------------------------------------------- 
    def to_xml_tree(self):
        xml_tree        = ET.Element('item')
        title           = ET.SubElement(xml_tree, 'title')
        title.text      = self.get_title()
        desc            = ET.SubElement(xml_tree, 'description')
        desc.text       = self.get_description()
        link            = ET.SubElement(xml_tree, 'link')
        link.text       = self.get_link()
        guid            = ET.SubElement(xml_tree, 'guid')
        guid.text       = self.get_guid()
        pub_date        = ET.SubElement(xml_tree, 'pubDate')
        pub_date.text   = self.get_pub_date()
        return xml_tree
    #-------------------------------------------------------------------------- 
    def to_html(self):
        html = ['<div class="rss_item"><p class="alignLeft"><a href="', 
        self.get_link(), '">', 
        self.get_title(), 
        '</a></p><p class="rss_timestamp">', 
        self.get_pub_date(), '</p><p class="rss_description">', 
        self.get_description(), '</p></div>'] 
        html_string = ''.join(html)
        return html_string
    #-------------------------------------------------------------------------- 
    def to_xml(self):
        return ET.tostring(self.to_xml_tree(), encoding =
                ENCODING).decode(ENCODING)
    #-------------------------------------------------------------------------- 
    def __str__(self):
        return str(self.to_xml())
#==============================================================================    
class Channel(Item):

    def __init__(self, max_items = 0):
        Item.__init__(self)
        self.tag_name        = 'channel'
        self.ttl             = '1800'
        self.items           = deque()
        self.pub_date        = ""
        self.last_build_date = ""
        self.max_items       = max_items
        self.logger          = logging.getLogger("Channel")
    #-------------------------------------------------------------------------- 
    def set_ttl(self, ttl):
        self.ttl = ttl
    #-------------------------------------------------------------------------- 
    def get_ttl(self):
        return self.ttl
    #-------------------------------------------------------------------------- 
    def set_last_build_date(self, last_build_date):
        self.last_build_date = last_build_date
    #-------------------------------------------------------------------------- 
    def add_item(self, item):
        """ Inserts a new RSS item to this channel """
        if len(self.items) > self.max_items > 0:
            self.logger.debug( len(self.items) + " >= " + self.max_items + 
                " Removing last item...")
            self.remove_last_item()
        self.items.append(item)
        self.logger.debug( "Channel: Added item " + item.to_xml())
        self.logger.debug( "Channel.add_item: Items are now " + [" * " +
            it.get_title() for it in self.items].__str__())
    #-------------------------------------------------------------------------- 
    def remove_item(self, item):
        self.items.remove(item)
    #-------------------------------------------------------------------------- 
    def remove_last_item(self):
        self.items.popleft()
    #-------------------------------------------------------------------------- 
    def get_items(self):
        return self.items
    #-------------------------------------------------------------------------- 
    def set_max_items(self, max_items):
        self.max_items = max_items
        if max_items > 0:
            while len(self.items) > max_items:
                self.remove_last_item()
    #-------------------------------------------------------------------------- 
    def to_html(self):
        html = []
        for item in self.items:
            html.append(item.to_html())
        html_string = ''.join(html)
        return html_string
    #-------------------------------------------------------------------------- 
    def to_xml_tree(self):
        xml_tree             = ET.Element('channel')
        title                = ET.SubElement(xml_tree, 'title')
        title.text           = self.get_title()
        description          = ET.SubElement(xml_tree, 'description')
        description.text     = self.get_description()
        link                 = ET.SubElement(xml_tree, 'link')
        link.text            = self.get_link()
        last_build_date      = ET.SubElement(xml_tree, 'lastBuildDate')
        last_build_date.text = nagaUtils.get_timestamp_now()
        pub_date             = ET.SubElement(xml_tree, 'pubDate')
        pub_date.text        = self.get_pub_date()
        ttl                  = ET.SubElement(xml_tree, 'ttl')
        ttl.text             = self.get_ttl()
        items = self.items
        items.reverse()
        for item in items:
            xml_tree.append(item.to_xml_tree())
        return xml_tree
    
