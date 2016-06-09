from datetime import datetime, timedelta
import pytz
from pytz import timezone


def time():
    utc = pytz.utc
    print(utc.zone)
    local_time = datetime.now()
    print(local_time)

    fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    utc_dt = utc.localize(datetime.now())
    utc_dt.strftime(fmt)
    print(utc_dt)

    au_tz = timezone('Australia/Brisbane')
    au_dt = utc_dt.astimezone(au_tz)
    au_dt.strftime(fmt)
    print(au_dt)

    bri = au_tz.normalize(utc_dt.astimezone(au_tz))
    bri.strftime(fmt)
    print(bri)

    utc_dt2 = au_dt.astimezone(utc)
    utc_dt2.strftime(fmt)
    print(utc_dt2)

    return local_time, utc_dt, au_dt, bri, utc_dt2


def show_time():
    t = time()
    a = ""
    for i in t:
        a += str(i) + '\n'
    return a

print(show_time())

# 2016-06-08 18:03:54.135738 2016-06-08 18:03:54.135783+00:00 2016-06-09 04:03:54.135783+10:00 2016-06-09 04:03:54.135783+10:00 2016-06-08 18:03:54.135783+00:00
