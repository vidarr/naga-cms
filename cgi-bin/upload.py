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
    registry_object = registry.Registry()
    if file_name in registry_object.get_article_keys():
        # If article is being updated, remove old version, modify summary
        article_object = registry_object.get(file_name)
        summary_old    = article_object.get_summary()
        summary        = ''.join([summary_old, '<br>', summary])
        registry_object.remove(file_name)
    article_object = article.Article()
    article_object.set_heading(heading)
    article_object.set_summary(summary)
    article_object.set_content(content)
    article_object.set_categories(categories)
    registry_object.add(file_name, article_object)
    registry_object.save()
#------------------------------------------------------------------------------
def post_entry(heading, summary, content = None, categories = None, file_name =
        None):
    _logger.info("New post")
    if content:
        if file_name:
            summary = UPDATE_LABEL + summary
        else:
            file_name = create_file_name(heading, summary, content)
        _logger.info("Posting article")
        write_content(heading   , summary, content, 
            categories, file_name)
    write_rss(heading, summary, file_name)
    page_object = page.Page()
    page_object.set_content("New post accepted")
    return page_object.get_html()
#------------------------------------------------------------------------------
def create_file_name(heading, summary, content):
    '''
    Create a 'unique' file name from heading, summary and content
    '''
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
    return file_name + ".xml"
#------------------------------------------------------------------------------
def get_chosen_categories(form):
    '''
    Return an array containing the names of all categories whose checkboxes 
    have been selected
    '''
    categories = []
    for key_value in form.keys():
        _logger.debug(key_value)
        key_parts = key_value.split('.')
        if len(key_parts) == 2 and key_parts[0] == 'category':
            _logger.debug(form[key_value].value)
            categories.append(key_parts[1])
    return categories
#------------------------------------------------------------------------------
def get_file_name(form):
    '''
    Return value of 'file_name' variable if contained within form,
    None otherwise
    '''
    file_name = None
    if 'file_name' in form.keys():
        file_name = form['file_name'].value
    return file_name
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
        print(post_entry(heading, summary, form['content'].value, 
            get_chosen_categories(form), get_file_name(form)))
    else:
        print(post_entry(heading, summary))

