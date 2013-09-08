#!/usr/bin/python
import cgi
import cgitb
import StringIO
import io
import os
import sys

PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/..'
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/' + MODULE_DIR);
import naga_config
import article
import rss

def post_news(heading, summary, content):
    write_content(heading, summary, content, [])
    rss_channel = rss.Channel()
    rss_channel.set_title("Michael J. Beer")
    rss_channel.set_description("My Test")
    rss_channel.set_link("localhost/seite")
    rss_object = rss.Rss(PAGE_ROOT + '/../' + naga_config.RSS_FEED_PATH)
    rss_object.add_channel(rss_channel)
    rss_item = rss.Item()
    rss_item.set_title(heading)
    rss_item.set_description(summary)
    rss_item.set_link("localhost/seite")
    rss_channel.add_item(rss_item)
    rss_object.to_file()
    page=StringIO.StringIO()
    page.write("""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>""")
    page.write(rss_object.to_xml())
    page.write("""
    </body>
    </html>
    """)
    ret_page = page.getvalue()
    page.close()
    return ret_page


def write_content(heading, summary, content,categories):
    xml = article.Article()
    xml.set_heading(heading)
    xml.set_summary(summary)
    xml.set_content(content)
    xml.set_categories(categories)
    timestamp = xml.get_timestamp()
    file_name = '/' + PAGE_ROOT + '/' + naga_config.CONTENT_DIR + '/' + timestamp + ".xml"
    xml_file=open(file_name, 'w+')
    xml_file.write(xml.to_xml())
    xml_file.close()


cgitb.enable()
form = cgi.FieldStorage()
if 'heading' not in form or 'summary' not in form or 'content' not in form:
    print "Error: Called without enough parameters"
else:
    print "Content-Type: text/html\n\n"
    print post_news(form['heading'].value, form['summary'].value,
            form['content'].value)

