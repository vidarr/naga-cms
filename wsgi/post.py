# -*- coding: UTF-8 -*-
#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2013, 2014, 2015 
#                  Michael J. Beer <michael.josef.beer@googlemail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
#-------------------------------------------------------------------------------
PAGE_ROOT     = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR    = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
from naga_config import *
import post_page
import page
import naga_wsgi
from wsgi_hooks import EnsureAuthenticatedHook, ErrorCatchingHook
#------------------------------------------------------------------------------
__logger = logging.getLogger("post.py")
#------------------------------------------------------------------------------
def post(request, start_response):
    __logger.info("Editing")
    (file_name) = request.get_get_variables(HTTP_ARG_FILE_NAME)
    if file_name is not None and file_name[0] is not None:
        __logger.info("Going to edit " + file_name[0])
        post = post_page.PostPage(request, FILENAME=file_name[0])
    else:
        post = post_page.PostPage(request)
    page_object = page.Page(request)
    page_object.add_css_link(CSS_POST_PATH)
    page_object.add_css_link(CSS_ARTICLE_PATH)
    html_string = post.to_html(True)
    page_object.set_content(html_string)
    response_body = page_object.get_html()
    return naga_wsgi.create_response(start_response, response_body)
#------------------------------------------------------------------------------
def application(environ, start_response):
    request = naga_wsgi.Wsgi(environ)
    errorCatchingHook = ErrorCatchingHook(post)
    ensureAuthenticatedHook = EnsureAuthenticatedHook(errorCatchingHook)
    return  ensureAuthenticatedHook(request, start_response)
