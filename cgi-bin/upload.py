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
import registry

_logger = logging.getLogger("upload")

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
    _logger.debug( "upload.write_rss: got channel " + channel.__str__())
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
    article_object = article.Article()
    article_object.set_heading(heading)
    article_object.set_summary(summary)
    article_object.set_content(content)
    article_object.set_categories(categories)
    timestamp = article_object.get_timestamp()
    file_name = timestamp + ".xml"
    registry_object = registry.Registry()
    registry_object.add(file_name, article_object)
    registry_object.save()
    return article_object

def post_news(heading, summary, content_exists, content, categories):
    _logger.info("New post")
    if content_exists:
        _logger.info("Posting article")
        article = write_content(heading, summary, content, categories)
    write_rss(heading, summary, content, categories)
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
    _logger.info("Request")
    form = cgi.FieldStorage()
    if 'heading' not in form or 'summary' not in form or 'content' not in form:
        _logger.error("Error: Called without enough parameters")
    else:
        categories = []
        for key_value in form.keys():
            _logger.debug(key_value)
            key_parts = key_value.split('.')
            if len(key_parts) == 2 and key_parts[0] == 'category':
                _logger.debug(form[key_value].value)
                categories.append(key_parts[1])
        print "Content-Type: text/html\n\n"
        print post_news(form['heading'].value, form['summary'].value,
        form.getvalue('contentexists'), form['content'].value, categories)

