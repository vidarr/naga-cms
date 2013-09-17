#!/usr/bin/python
import cgi
import cgitb
import StringIO
import io
import os
import sys
import string

ABS_PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/..'
MODULE_DIR  = 'python'
sys.path.append(ABS_PAGE_ROOT + '/' + MODULE_DIR);
from naga_config import *
import article
import rss
from logger import log

def get_new_channel():
    rss_channel = rss.Channel()
    rss_channel.set_title("Michael J. Beer")
    rss_channel.set_description("My Test")
    rss_channel.set_link("localhost/seite")
    return rss_channel

def write_rss(heading, summary, content, categories):
    rss_item = rss.Item()
    rss_item.set_title(heading)
    rss_item.set_description(summary)
    rss_item.set_link("localhost/seite")
    rss_object = rss.Rss(ABS_PAGE_ROOT + PATH_SEPARATOR + '..' + RSS_FEED_PATH)
    channel = rss_object.get_channels()
    log(LOG_DEBUG, "upload.write_rss: got channel " + channel.__str__())
    if len(channel) < 1:
        channel = get_new_channel()
        rss_object.add_channel(channel)
    else:
        channel = channel[0]
    channel.add_item(rss_item)
    rss_object.to_file()
    rss_object = rss.Rss(ABS_PAGE_ROOT + PATH_SEPARATOR + '..' + RSS_ROLLING_FEED_PATH)
    channel = rss_object.get_channels()
    if len(channel) < 1:
        channel = get_new_channel()
        rss_object.add_channel(channel)
    else:
        channel = channel[0]
    channel.set_max_items(RSS_ROLLING_ENTRIES)
    channel.add_item(rss_item)
    rss_object.to_file()

def write_content(heading, summary, content,categories):
    xml = article.Article()
    xml.set_heading(heading)
    xml.set_summary(summary)
    xml.set_content(content)
    xml.set_categories(categories)
    timestamp = xml.get_timestamp()
    file_name = '/' + ABS_PAGE_ROOT + PATH_SEPARATOR +  \
         CONTENT_DIR + PATH_SEPARATOR + timestamp + ".xml"
    xml_file=open(file_name, 'w+')
    xml_file.write(xml.to_xml())
    xml_file.close()
    return xml

def post_news(heading, summary, content_exists, content):
    log(LOG_INFO, "New post")
    if content_exists:
        log(LOG_INFO, "Posting article")
        article = write_content(heading, summary, content, [])
    write_rss(heading, summary, content, [])
    page=StringIO.StringIO()
    page.write("""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>""")
    page.write("Neuer Post hochgeladen:\n")
    page.write("""
    </body>
    </html>
    """)
    ret_page = page.getvalue()
    page.close()
    return ret_page


if __name__ == '__main__':
    cgitb.enable()
    log(LOG_INFO, "Request")
    form = cgi.FieldStorage()
    if 'heading' not in form or 'summary' not in form or 'content' not in form:
        print "Error: Called without enough parameters"
    else:
        print "Content-Type: text/html\n\n"
        print post_news(form['heading'].value, form['summary'].value,
        form.getvalue('contentexists'), form['content'].value)

