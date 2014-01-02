#!/usr/bin/python3
import cgi
import cgitb
import io
import os
import sys
import string
import hashlib
import base64
#------------------------------------------------------------------------------
ABS_PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__))) + '/..'
MODULE_DIR  = 'python'
sys.path.append(ABS_PAGE_ROOT + '/' + MODULE_DIR);
from naga_config import *
import article
import rss
import registry
import security
import page
#------------------------------------------------------------------------------
_logger    = logging.getLogger("upload")
_hash_func = hashlib.sha256()
#------------------------------------------------------------------------------
def get_new_channel():
    rss_channel = rss.Channel()
    rss_channel.set_title("Michael J. Beer")
    rss_channel.set_description("My Test")
    rss_channel.set_link("localhost/seite")
    return rss_channel
#------------------------------------------------------------------------------
def write_rss(heading, summary, file_name = None):
    rss_item = rss.Item()
    rss_item.set_title(heading)
    rss_item.set_description(summary)
    if file_name:
        link = NAGA_ROOT + PATH_SEPARATOR + SHOW_RELATIVE_PATH + '?' + \
                'type=article&content=' + file_name
    else:
        link = NAGA_ROOT
    rss_item.set_link(link)
    _logger.debug("Set link to " + rss_item.get_link())
    _logger.debug("NAGA_ROOT " + NAGA_ROOT)
    _logger.debug("SHOW_RELATIVE_PATH " + SHOW_RELATIVE_PATH)
    rss_object = rss.Rss(NAGA_ABS_ROOT + PATH_SEPARATOR + RSS_FEED_PATH)
    channel = rss_object.get_channels()
    _logger.debug( "upload.write_rss: got channel " + channel.__str__())
    if len(channel) < 1:
        channel = get_new_channel()
        rss_object.add_channel(channel)
    else:
        channel = channel[0]
    channel.add_item(rss_item)
    rss_object.to_file()
    rss_object = rss.Rss(NAGA_ABS_ROOT + PATH_SEPARATOR + RSS_ROLLING_FEED_PATH)
    channel = rss_object.get_channels()
    if len(channel) < 1:
        channel = get_new_channel()
        rss_object.add_channel(channel)
    else:
        channel = channel[0]
    channel.set_max_items(RSS_ROLLING_ENTRIES)
    channel.add_item(rss_item)
    rss_object.to_file()
#------------------------------------------------------------------------------
def write_content(heading, summary, content,categories, file_name):
    article_object = article.Article()
    article_object.set_heading(heading)
    article_object.set_summary(summary)
    article_object.set_content(content)
    article_object.set_categories(categories)
    registry_object = registry.Registry()
    registry_object.add(file_name, article_object)
    registry_object.save()
    return article_object
#------------------------------------------------------------------------------
def post_news(heading, summary, content = None, categories = None):
    _logger.info("New post")
    file_name = None
    if content:
        if type(content) == type ('a'):
            content_to_hash = content.encode(ENCODING)
        else:
            content_to_hash = content
        _hash_func.update(content_to_hash)
        if summary:
            if type(summary) == type ('a'):
                summary_to_hash = summary.encode(ENCODING)
            else:
                summary_to_hash = summary
            _hash_func.update(summary_to_hash)
        file_name = _hash_func.digest()
        file_name = base64.b32encode(file_name).decode(ENCODING)
        file_name = file_name + ".xml"
        if content:
            _logger.info("Posting article")
            article = write_content(heading   , summary, content, 
                                    categories, file_name)
    write_rss(heading, summary, file_name)
    return page.wrap("New post accepted")
#------------------------------------------------------------------------------
if __name__ == '__main__':
    cgitb.enable()
    _logger.info("upload.py: Upload request received")
    form = cgi.FieldStorage()
    # if not security.authenticate_cgi(form):
    if not security.authenticate_cookie():
        print(page.wrap('<p class="error">Authentication failure</p>'))
        sys.exit(1)
    if 'heading' not in form or 'summary' not in form:
        _logger.error("Error: Called without enough parameters")
        print(page.wrap('''
             <p class="error">Internal error: Called without
            enough parameters</p>'''))
        sys.exit(1)
    heading = form['heading'].value
    summary = form['summary'].value
    if 'contentexists' in form:
        categories = []
        for key_value in form.keys():
            _logger.debug(key_value)
            key_parts = key_value.split('.')
            if len(key_parts) == 2 and key_parts[0] == 'category':
                _logger.debug(form[key_value].value)
                categories.append(key_parts[1])
        print(post_news(heading, summary, form['content'].value, categories))
    else:
        print(post_news(heading, summary))

