from datetime import datetime
from django.utils.dateformat import format

def to_timestamp(dt):
    return format(dt, 'U')

def get_today_epoch():
    now = datetime.utcnow()
    return now.replace(now.year, now.month, now.day, 0, 0, 0, 0)

def get_difference_epoch(epoch):
    diff = datetime.utcnow() - epoch
    return int(diff.total_seconds() * 1000000)