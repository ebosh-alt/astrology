import datetime
from dateutil.rrule import *


def transform_date(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    day, month, year = date
    return f'{day} {months[int(month) - 1]} {year} года'


def get_date_response(add_days):
    offset = datetime.timedelta(hours=3)
    current_date = datetime.datetime.now(datetime.timezone(offset, name='МСК'))
    business_days_to_add = add_days
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday > 5:
            continue
        business_days_to_add -= 1
    day = current_date.day
    year = current_date.year
    month = current_date.month
    result = transform_date([day, month, year])
    return result
