import datetime
from firebase import firebase
fb = firebase.FirebaseApplication("https://burning-heat-7654.firebaseio.com/", None)

_YES = ["yes", "Yes", "YES"]
_NO = ["no", "No", "NO"]


def daily_logging(user, contact, text):
    text.split(' ')
    i = 0

    query = query_builder(user, contact)

    for word in text:
        if word in _YES or word in _NO:
            if word in _YES:
                connected = 1
            else:
                connected = 0

            fb.patch(query, {'connected': connected})
            # fb.post_async(query, data)
            return 1

        elif word == "time" or word == "times":
            time = int(text[i-1])
            fb.patch(query, {'time': time})
            # fb.put(query, "123", {'time': time})    #  put is work too
            return 2
        i += 1

    return False


def query_builder(user, contact):
    query = "/logging/"
    postfix_query = user + "/" + contact + "/"
    start_date = datetime.datetime.strptime(str(fb.get("/logging/startDate", None)), "%Y%m%d").date()
    today = datetime.date.today()
    delta = int(str(today - start_date).split(' ')[0])
    if delta <= 0:
        query += "week1/day1/" + postfix_query
    else:
        week = str(delta // 7 + 1)
        day = str(delta % 7 + 1)
        query += "week" + week + "/day" + day + "/" + postfix_query
    return query


def status_logging():
    pass
# may need a new query builder. the path could be /logging/na