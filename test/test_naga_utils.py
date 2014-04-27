#!/usr/bin/python
#
# Part of the CMS naga, See <https://ubeer.org
#
#    Copyright (C) 2013, 2014 Michael J. Beer <michael.josef.beer@googlemail.com>
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
#------------------------------------------------------------------------------
PAGE_ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR  = 'python'
sys.path.append(PAGE_ROOT + '/../' + MODULE_DIR);
import registry
from article import Article
import nagaUtils
#------------------------------------------------------------------------------
_test_timestamp = "Mon, 06 Sep 2010 00:01:00 +0000"
posix = nagaUtils.to_posix_timestamp(_test_timestamp)
print(_test_timestamp)
print(posix)
print(nagaUtils.to_rfc822_timestamp(posix))

