import datetime
import re
from firebase import firebase

import ENV_VAR as ENV
import timezone_handler as tz

# fb = firebase.FirebaseApplication("https://burning-heat-7654.firebaseio.com/", None)
fb = firebase.FirebaseApplication(ENV.FIREBASE_LINK, None)

# _YES = ["yes", "Yes", "YES", "Y", "y"]
# _NO = ["no", "No", "NO", "N", "n"]
TIME_LINE = 190000  # 24 hour standard ==> 19:00:00
RECORD_DAY_CHANGE_TIME_LINE = 180000  # 1 hour before TIME_LINE  ==> 18:00:00


def get_brisbane_time():
    return tz.get_brisbane_time().time()


def get_date():
    """
    just simple get today's date
    :return <class 'datetime.date'>, 2016-06-03
    """

    return tz.get_brisbane_time().date()


def get_start_date(query):
    """
    get the evaluation start-date of this contact
    :param query: string   a path contains startDate key   /logging/response/<contact_name>
    :return <class 'datetime.date'>, 2016-06-03
    """
    return datetime.datetime.strptime(fb.get(query, None)["startDate"], "%Y%m%d").date()


def str_date(date):
    """
    convert the datetime.date into string
    :param date: <class 'datetime.date'>, 2016-06-10 02:03:46.788409+10:00
    :return 20160603
    """
    d = str(date).split('-')
    string_date = ""
    for i in range(len(d)):
        string_date += d[i]
    return string_date


def time_is_over_day_segment():
    """
    a return of get_brisbane_time() follows this format: 16:21:26.009927
    we need 16:21:26 ==> 162126
    """
    now_list = str(get_brisbane_time()).split('.')[0].split(':')
    now_string = ""
    for segment in now_list:
        now_string += segment

    now = int(now_string)
    """
    if the response time is less than RECORD_DAY_CHANGE_TIME_LINE, 18 o'clock, we seems it's the previous day's
    response so that delta should minus 1. Otherwise, delta is right.
    """
    if now < RECORD_DAY_CHANGE_TIME_LINE:
        return False
    return True


def generate_query_by_time(query):
    """
     this function generates the time layout query based on the date
     :param query: string; the base of query path: "/logging/response/"
     :param contact: string
     :return the final query path: "/logging/response/<contact>/dailyMessage/week1/day1"
    """
    # the format of delta: 18 days, 0:00:00


    try:
        delta_string = str(get_date() - get_start_date(query)).split(' ')[0]
        delta = int(delta_string)

    except TypeError as err:
        """
        could get_start_date of contact because it hasn't been initialized.
        """
        # print("the contact hasn't initialize the evaluation: ", err)
        return None, err

    except ValueError as err:
        """
        this exception is used to handle the first day record error.
        minus the same dates will get "0:00:00".
        """
        if delta_string == "0:00:00":
            delta = 0
        else:
            # print("the date has some problem: ", err)
            return None, err
    # print(delta)
    query += "/dailyMessage/" + generate_time_path_by_delta(delta)

    return query


def generate_time_path_by_delta(delta):
    if delta <= 0:
        return "week1/day1"
    else:
        if not time_is_over_day_segment():
            delta -= 1
        week = str(delta // 7 + 1)
        day = str(delta % 7 + 1)
        return "week" + week + "/day" + day


def is_new_contact(contact):
    """

    :param contact: string of contact name
    :return if user has data, means not a new contact, return false; if none, return true.
    """
    query = "/logging/response/" + str(contact)
    if fb.get(query, None):
        return False
    return True


def create_contact_info(contact, user, number):
    """
    create the basic info of contact under /logging/response
    :param contact: string
    :param user: string
    :param number: string  "61478417108"
    """

    query = "/logging/response/" + contact
    data = {
        'startDate': str_date(get_date()),
        'number': number,
        'user': user
    }

    fb.patch(query, data)


def text_parse(text):
    """
    parse the response text and split the record
    :param text:
    :return tuple <times(int), is_connected(boolean)>
    """
    is_connected = False
    times = 0

    text = clean_text(text)

    """
    Since the response follow that, if yes, "Y<whatever>3"; if no, "N"
    we just need find the digit in the text

    if the text does contain digit, it must be no;
    if contains and great than 0, it must be yes.
    """
    match = re.search(r"\d+", text)
    if match:
        times = int(match.group())
        if times > 0:
            is_connected = True

    elif "once" in text:
        is_connected = True
        times = 1

    return times, is_connected


def clean_text(text):
    """
    :param text: any string
    re.complie("\W+") pick up all letters
    .sub(" ", text) break down string at " "
    .lower() output at lowercase
    """
    return re.compile("\W+").sub(" ", text).strip().lower()


def daily_message_logger(contact, text):
    query = "/logging/response/" + contact
    query = generate_query_by_time(query)

    if not query[0]:
        raise Exception("query module report an error")

    times, is_connected = text_parse(text)

    response_time = str(tz.get_brisbane_time())

    data = {
        'date': str_date(get_date()),
        'isResponsed': True,
        'responseText': text,
        'isConnected': is_connected,
        'times': times,
        'responseTime': response_time,
    }

    fb.patch(query, data)


def daily_logging(user, contact, number, text):
    """
    create the daily message logging automatically, also create the record the data based on the time changing
    :param user: string
    :param contact: string
    :param number: string "61478417108"
    :param text: string
    :return success update return True, or not
    """
    # print("daily_logging")
    try:
        if is_new_contact(contact):
            create_contact_info(contact, user, number)

        daily_message_logger(contact, text)
        return True
    except Exception as err:
        # print("Handling unknown error:  ", err)
        return False


def status_logging():
    pass
# may need a new query builder. the path could be /logging/na


#################################################################

def toy_message_logging(username, contact_name):
    if not is_a_valid_user(username):
        # TODO: a error reporter
        print("can't find user: " + username)
        pass
    query = "/logging/toy/" + username + "/"

    if is_new_toy_logging(query):
        create_toy_logging(query)

    query = generate_query_by_time(query)
    total = get_total_times(query)
    if total is None:
        data = {"date": str_date(get_date()),
                "total": 1}
        fb.patch(query, data)
    else:
        total += 1
        data = {"total": total}
        fb.patch(query, data)

    query += "/originRecord"

    record_data = {"loggingTime": str(tz.get_brisbane_time()),
                   "target": contact_name}
    fb.post(query, record_data)

    return True


def is_a_valid_user(username):
    query = "/user/" + username
    if fb.get(query, None):
        return True
    return False


def is_new_toy_logging(query):
    if not fb.get(query, None):
        return True
    return False


def create_toy_logging(query):
    data = {'startDate': str_date(get_date())}
    fb.patch(query, data)


def get_total_times(query):
    return fb.get(query + "/total", None)
