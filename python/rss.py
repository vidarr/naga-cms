#!/usr/bin/python
import StringIO
import os.path
import sys
import xml.dom.minidom


PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import page
import nagaUtils
from logger import log

class XmlTag:

    def __init__(self, tag_name, attributes = {}, content = ""):
        self.tag_name = tag_name
        self.attributes = attributes
        self.content = content

    def open_tag(self):
        xml = StringIO.StringIO()
        xml.write('<' + self.tag_name)
        for attribute in self.attributes.items():
            xml.write(' ')
            xml.write(attribute[0])
            xml.write("='")
            xml.write(attribute[1])
            xml.write("'")
        xml.write('>')
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def close_tag(self):
        return '</' + self.tag_name + '>' + LINEBREAK

    def __str__(self):
        xml = StringIO.StringIO()
        xml.write(self.open_tag())
        xml.write(self.content)
        xml.write(self.close_tag())
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    @classmethod
    def get_text(cls, node):
        for child in node.childNodes:
            if node.nodeType == node.TEXT_NODE:
                return node.nodeValue
        return ""

class Rss(XmlTag):

    def __init__(self, file_name = ""):
        XmlTag.__init__(self, 'rss', {'version' : '2.0'}, '')
        self.file_name = file_name
        self.channels  = []
        if file_name != "":
            try:
                self.from_file()
            except:
                pass

    def from_file(self):
        if self.file_name == "":
            raise IOError("File name not set")
        rss_file = open(self.file_name, "r")
        rss_content = rss_file.read()
        rss_file.close()
        if rss_content:
            dom = xml.dom.minidom.parseString(rss_content)
            self.from_xml(dom)
        log(LOG_DEBUG, "Rss.from_file: Read " + self.file_name)
    
    def from_xml(self, rss_content):
        if rss_content.documentElement.nodeName != 'rss' or not rss_content.documentElement.hasChildNodes():
            return None
        for node in rss_content.documentElement.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                channel = Channel.from_xml(node)
                self.add_channel(channel)

    def add_channel(self, chan):
        self.channels.append(chan)

    def remove_channel(self, chan):
        self.channels.remove(chan)

    def get_channels(self):
        return self.channels

    def to_xml(self):
        xml = StringIO.StringIO()
        xml.write('<?xml version="1.0" encoding="UTF-8" ?>')
        xml.write(LINEBREAK)
        xml.write(self.open_tag())
        for chan in self.channels:
            xml.write(chan.to_xml())
        xml.write(self.close_tag())
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def to_file(self):
        if self.file_name == "":
            raise IOError("File name not set")
        rss_file = open(self.file_name, 'w')
        rss_file.write(self.to_xml())
        rss_file.close()
        log(LOG_DEBUG, "Rss.to_file: Wrote " + self.file_name)


class Item(XmlTag):

    def __init__(self):
        XmlTag.__init__(self, 'item')
        self.title         = ""
        self.description   = ""
        self.link          = ""
        self.pub_date      = None
        self.guid          = None

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_link(self, link):
        self.link = link

    def get_link(self):
        return self.link

    def get_guid(self):
        if self.guid:
            return self.guid
        return self.title + '-' + nagaUtils.get_timestamp_now()

    def set_guid(self, guid):
        self.guid = guid

    def set_pub_date(self, pub_date):
        self.pub_date = pub_date

    def get_pub_date(self):
        if self.pub_date:
            return self.pub_date
        return nagaUtils.get_timestamp_now()

    def get_common_data_as_xml(self):
        xml = StringIO.StringIO()
        tag = XmlTag('title', {}, self.title)
        xml.write(tag)
        tag = XmlTag('description', {}, self.description)
        xml.write(tag)
        tag = XmlTag('link', {}, self.link)
        xml.write(tag)
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def get_specific_data_as_xml(self):
        xml = StringIO.StringIO()
        tag = XmlTag('guid', {}, self.get_guid())
        xml.write(tag)
        tag = XmlTag('pubDate', {}, self.get_pub_date())
        xml.write(tag)
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def to_xml(self):
        xml = StringIO.StringIO()
        xml.write(self.open_tag())
        xml.write(self.get_common_data_as_xml())
        xml.write(self.get_specific_data_as_xml())
        xml.write(self.close_tag())
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    @classmethod
    def from_xml(cls, dom):
        if not dom.nodeName == 'item' or not dom.hasChildNodes():
            return None
        children = dom.childNodes
        item = Item()
        for child in children:
            log(LOG_DEBUG, "Item.from_xml: " + child.nodeName + " " +
                    child.nodeType.__str__())
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == 'title':
                    item.set_title(XmlTag.get_text(child))
                elif child.nodeName == 'description':
                    item.set_description(XmlTag.get_text(child))
                elif child.nodeName == 'link':
                    item.set_link(XmlTag.get_text(child))
                elif child.nodeName == 'guid':
                    item.set_guid(XmlTag.get_text(child))
                elif child.nodeName == 'pubDate':
                    item.set_pub_date(XmlTag.get_text(child))
                else:
                    log(LOG_WARNING, "Parsing RSS/Item: Unknown tag: " +
                            child.nodeName)
        log(LOG_DEBUG, "Got " + item.__str__())
        return item

class Channel(Item):

    def __init__(self, max_items = 0):
        Item.__init__(self)
        self.tag_name        = 'channel'
        self.ttl             = 1800
        self.items           = []
        log(LOG_DEBUG, "Channel.__init__: Items are " + [" * " + item.__str__() for item
            in self.items].__str__())
        self.pub_date        = ""
        self.last_build_date = ""
        self.max_items       = max_items
    
    def set_ttl(self, ttl):
        self.ttl = ttl
    
    def get_ttl(self):
        return self.ttl

    def add_item(self, item):
        """ Inserts a new RSS item to this channel """
        if len(self.items) > self.max_items > 0:
            log(LOG_DEBUG, len(self.items) + " >= " + self.max_items + 
                " Removing last item...")
            self.remove_last_item()
        self.items.append(item)
        log(LOG_DEBUG, "Channel: Added item " + item.to_xml())
        log(LOG_DEBUG, "Channel.add_item: Items are now " + [" * " + it.__str__() for it in self.items].__str__())

    def remove_item(self, item):
        self.items.remove(item)

    def remove_last_item(self):
        self.items.pop()

    def get_items(self):
        return self.items

    def set_max_items(self, max_items):
        self.max_items = max_items
        if max_items > 0:
            while len(self.items) > max_items:
                self.remove_last_item()

    def get_specific_data_as_xml(self):
        timestamp = nagaUtils.get_timestamp_now()
        xml = StringIO.StringIO()
        tag = XmlTag('lastBuildDate', {}, timestamp)
        xml.write(tag)
        tag = XmlTag('pubDate', {}, timestamp)
        xml.write(tag)
        tag = XmlTag('ttl', {}, self.ttl)
        xml.write(tag)
        for item in self.items:
            log(LOG_DEBUG, "Channel.get_specific_data_as_xml: item " +
                    item.__str__())
            xml.write(item.to_xml())
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    @classmethod
    def from_xml(cls, dom):
        if not dom.nodeName == 'channel' or not dom.hasChildNodes():
            return None
        children = dom.childNodes
        channel = Channel()
        for item in children:
            log(LOG_DEBUG, "Channel.from_xml: " + item.nodeName + " " +
                    item.nodeType.__str__())
            if item.nodeType == item.ELEMENT_NODE:
                if item.nodeName == 'title':
                    channel.set_title(XmlTag.get_text(item))
                elif item.nodeName == 'description':
                    channel.set_description(XmlTag.get_text(item))
                elif item.nodeName == 'link':
                    channel.set_link(XmlTag.get_text(item))
                elif item.nodeName == 'lastBuildDate':
                    channel.last_build_date = XmlTag.get_text(item)
                elif item.nodeName == 'pubDate':
                    channel.pub_date = XmlTag.get_text(item)
                elif item.nodeName == 'item':
                    try:
                        channel.add_item(Item.from_xml(item))
                    except Exception as ex:
                        log(LOG_DEBUG, "Channel.from_xml: Exception occured" + ex.__str__())
                    log(LOG_DEBUG, "Read channel " + channel.__str__()) 
        return channel
    
