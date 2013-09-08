import datetime
import time
from email import utils

def get_timestamp_now():
        now = datetime.datetime.utcnow()
        now_tuple = now.timetuple()
        now_timestamp = time.mktime(now_tuple)
        return utils.formatdate(now_timestamp)

