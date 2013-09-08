#!/usr/bin/python
import StringIO
import os.path
import sys


PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import naga_config
import page
import nagaUtils

class XmlTag:

    def __init__(self, tag_name, attributes = {}, content = ""):
        self.tag_name = tag_name
        self.attributes = attributes
        self.content = content

    def open_tag(self):
        xml = StringIO.StringIO()
        xml.write('<' + self.tag_name)
        for attribute in self.attributes.items():
            xml.write(attribute[0])
            xml.write('=')
            xml.write(attribute[1])
            xml.write(' ')
        xml.write('>')
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def close_tag(self):
        return '</' + self.tag_name + '>'

    def __str__(self):
        xml = StringIO.StringIO()
        xml.write(self.open_tag())
        xml.write(self.content)
        xml.write(self.close_tag())
        xml_string = xml.getvalue()
        xml.close()
        return xml_string


class Rss:

    def __init__(self, file_name = ""):
        self.file_name = file_name
        try:
            with open(file_name): pass
            # Parse file
        except IOError:
            pass
            # Init new file
        self.channels  = []

    def add_channel(self, chan):
        self.channels.append(chan)

    def remove_channel(self, chan):
        self.channels.remove(chan)

    def to_xml(self):
        xml = StringIO.StringIO()
        xml.write('''<?xml version="1.0" encoding="UTF-8" ?>
                     <rss version="2.0">''')
        for chan in self.channels:
            xml.write(chan.to_xml())
        xml.write('</rss>')
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def to_file(self):
        if self.file_name == "":
            raise IOError("File name not set")
        rss_file = open(self.file_name, 'w')
        rss_file.write(self.to_xml())
        rss_file.close()


class Item(XmlTag):

    def __init__(self):
        XmlTag.__init__(self, 'item')
        self.title         = ""
        self.description   = ""
        self.link          = ""

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

    def get_common_data_as_xml(self):
        xml = StringIO.StringIO()
        xml.write('<title>')
        xml.write(self.title)
        xml.write('</title>')
        xml.write('<description>')
        xml.write(self.description)
        xml.write('</description>')
        xml.write('<link>')
        xml.write(self.link)
        xml.write('</link>')
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def get_specific_data_as_xml(self):
        timestamp = nagaUtils.get_timestamp_now()
        xml = StringIO.StringIO()
        xml.write('<guid>')
        xml.write(self.title) 
        xml.write('-')
        xml.write(timestamp)
        xml.write('</guid>')
        xml.write('<pubDate>')
        xml.write(timestamp)
        xml.write('</pubDate>')
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


class Channel(Item):

    def __init__(self):
        Item.__init__(self)
        self.tag_name = 'channel'
        self.ttl = 1800
        self.items = []
    
    def set_ttl(self, ttl):
        self.ttl = ttl
    
    def get_ttl(self):
        return self.ttl

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def remove_last_item(self):
        self.items.pop()

    def get_specific_data_as_xml(self):
        timestamp = nagaUtils.get_timestamp_now()
        xml = StringIO.StringIO()
        xml.write('<lastBuildDate>')
        xml.write(timestamp)
        xml.write('</lastBuildDate>')
        xml.write('<pubDate>')
        xml.write(timestamp)
        xml.write('</pubDate>')
        xml.write('<ttl>')
        xml.write(self.ttl)
        xml.write('</ttl>')
        for item in self.items:
            xml.write(item.to_xml())
        xml_string = xml.getvalue()
        xml.close()
        return xml_string


