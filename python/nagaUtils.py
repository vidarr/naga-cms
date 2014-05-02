#
# Part of the CMS naga, See <https://ubeer.org>
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
import datetime
import time
import re
from email import utils
#------------------------------------------------------------------------------
def get_timestamp_now():
    now = datetime.datetime.utcnow()
    now_tuple = now.timetuple()
    now_timestamp = time.mktime(now_tuple)
    return utils.formatdate(now_timestamp)
#------------------------------------------------------------------------------
def to_rfc822_timestamp(timeval):
    if type(timeval) == int:
        timeval = datetime.datetime.fromtimestamp(timeval) 
    if type(timeval) == datetime.datetime:
        time_tuple = timeval.timetuple()
        timestamp = time.mktime(time_tuple)
        return utils.formatdate(timestamp)
    if type(timeval) == str:
        return timeval
    return None
#------------------------------------------------------------------------------
def to_posix_timestamp(time):
    if type(time) == str:
       time_tuple = utils.parsedate_tz(time)
       time = utils.mktime_tz(time_tuple)
    if type(time) == datetime.datetime:
       return utils.formatdate(time)
    if type(time) == int or type(time) == float:
       return int(time)
    return None
#------------------------------------------------------------------------------
def invalid_url(target):
    '''
    Test whether target contains a valid URL
    '''
    if not type(target) == type(''):
        return False
    return not re.match(r"[a-z]+://..*", target)
