from datetime import datetime, timedelta, tzinfo


class UTC10(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=10) + self.dst(dt)

    def dst(self, dt):
        """
        this function is for daylight saving time, Brisbane don't have a dst, so we can directly return 0.
        """
        return timedelta(0)

    def tzname(self, dt):
        return "UTC +10"


class UTC(tzinfo):
    """
    Google App Engine default timezone is UTC +0:00
    The default UTC timezone don't need to concern dst, so we can directly return 0
    """
    def utcoffset(self, dt):
        return timedelta(hours=0) + self.dst(dt)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC +0"


class UTC2(tzinfo):
    """
    Google App Engine default timezone is UTC +0:00
    The default UTC timezone don't need to concern dst, so we can directly return 0
    """
    def utcoffset(self, dt):
        return timedelta(hours=2) + self.dst(dt)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC +2"


def get_brisbane_time():
    return datetime.now(UTC()).astimezone(UTC10())

# def time():
#     fmt = '%Y-%m-%d %H:%M:%S %Z%z'
#     utc = pytz.utc
#     local_time = datetime.now()
#
#     utc_dt = utc.localize(datetime.now())
#     utc_dt.strftime(fmt)
#
#     au_tz = pytz.timezone('Australia/Brisbane')
#     au_dt = utc_dt.astimezone(au_tz)
#     au_dt.strftime(fmt)
#
#
#     return local_time, utc_dt, au_dt, bri
#
#
# def get_brisbane_time():
#     fmt = '%Y-%m-%d %H:%M:%S'
#     utc = pytz.utc
#
#     """
#     On Google app engine, the time zone is set at UTC as default
#     P.S. in summer, due to day-light-saving, British local time has 1 hour faster than UTC time.
#      but Brisbane time needn't to worry about that because Brisbane hasn't Day-light-saving. However, Sydney does have.
#     """
#     utc_dt = utc.localize(datetime.now())
#     utc_dt.strftime(fmt)
#
#     brisbane_timezone = pytz.timezone('Australia/Brisbane')  # Brisbane is UTC +10:00
#     brisbane_time = brisbane_timezone.normalize(utc_dt.astimezone(brisbane_timezone))
#     return brisbane_time.strftime(fmt)
#
#
# def show_time():
#     t = time()
#     a = ""
#     for i in t:
#         a += str(i) + '\n'
#     return a

# print(get_brisbane_time())

# 2016-06-08 18:03:54.135738
# 2016-06-08 18:03:54.135783+00:00
# 2016-06-09 04:03:54.135783+10:00
# 2016-06-09 04:03:54.135783+10:00
# 2016-06-08 18:03:54.135783+00:00
