#!/usr/bin/python
import os.path
import sys
import logging
import cgi
import cgitb
#------------------------------------------------------------------------------
ABSOLUTE_PAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR         = 'python'
sys.path.append(ABSOLUTE_PAGE_ROOT + '/../' + MODULE_DIR)
from naga_config import *
import article
import registry
import report
#------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------
if __name__ == '__main__':
    cgitb.enable()
    form = cgi.FieldStorage()
    criteria = []
    if 'category' in form:
        criteria = ['category', form['category']]
    article_registry = registry.Registry()
    found_articles = article_registry.find(criteria)
    if len(found_articles) < 1:
        content = "No articles found"
    else:
        content = report.create_short_article_report(article_registry, found_articles)
    print "Content-Type: text/html\n\n"
    print content





