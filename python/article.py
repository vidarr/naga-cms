import datetime
import StringIO
import os.path
import sys

PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import nagaUtils

class Article:

    def __init__(self):
        self.timestamp  = nagaUtils.get_timestamp_now()
        self.heading    = ''
        self.summary    = ''
        self.content    = ''
        self.categories = []

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        old_timestamp = self.timestamp
        self.timestamp = timestamp
        return old_timestamp

    def get_heading(self):
        return self.heading

    def set_heading(self, heading):
        old_heading = self.heading
        self.heading = heading
        return old_heading

    def get_summary(self):
        return self.summary

    def set_summary(self, summary):
        old_summary = self.summary
        self.summary = summary
        return old_summary

    
    def get_content(self):
        return self.content

    def set_content(self, content):
        old_content = self.content
        self.content = content
        return old_content

    def get_categories(self):
        return self.categories

    def set_categories(self, categories):
        old_categories = self.categories
        self.categories = categories
        return old_categories

    def to_xml(self):
        xml = StringIO.StringIO()
        xml.write("""
        <?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet href="../formatting/michael_josef_beer.xslt" type="application/xml"?>
        <michael.josef.beer.entry>
        <timestamp>""")
        xml.write(self.timestamp)
        xml.write("""
        </timestamp>
        <heading>
        """)
        xml.write(self.heading)
        xml.write("""
        </heading>
        <summary>
        """)
        xml.write(self.summary)
        xml.write("""
        </summary>
        <content>
        """)
        xml.write(self.content)
        xml.write("""
        </content>
        <categories>
        """)
        for category in self.categories:
            xml.write("<category>")
            xml.write(category)
            xml.write("</category>")
        xml.write("""
        </categories>
        </michael.josef.beer.entry>
        """)
        xml_string = xml.getvalue()
        xml.close()
        return xml_string

    def matches(self, criterion):
        point     = criterion[0]
        ref_value = criterion[1]
        if point ==  'heading':
            return self.get_heading() == ref_value
        if point == 'timestamp':
            return self.get_timestamp() == ref_value
        if point == 'category':
            return ref_value in self.get_categories()
        return False

