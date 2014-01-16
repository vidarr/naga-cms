import datetime
import time
from email import utils

def get_timestamp_now():
    now = datetime.datetime.utcnow()
    now_tuple = now.timetuple()
    now_timestamp = time.mktime(now_tuple)
    return utils.formatdate(now_timestamp)

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

def to_posix_timestamp(time):
    if type(time) == str:
       time_tuple = utils.parsedate_tz(time)
       time = utils.mktime_tz(time_tuple)
    if type(time) == datetime.datetime:
       return utils.formatdate(time)
    if type(time) == int:
       return time
    return None
