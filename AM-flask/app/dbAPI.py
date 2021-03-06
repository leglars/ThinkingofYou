from firebase import firebase
import ENV_VAR as ENV
fb = firebase.FirebaseApplication(ENV.FIREBASE_LINK, None)


def contact_list_extractor(group="default"):
    contact_list = {}
    user_data = fb.get("/user", None)

    if group == "default":
        contact_list["user"] = extract_user_contact(user_data)
        contact_list["admin"] = extract_admin_contact()

    return contact_list


def extract_user_contact(data):
    """
    :param data: the path of data: <username>/contact/{<contact name 1>: {"number": "+61xxxxxxxxx",
                                                                           "relationship": "friend"},
                                                        <contact name 2: data>,
                                                        ...}
    :return user_contacts_number_list: ["+61xxxxxxxxx", "+61xxxxxxxxx", ...]
    """
    contacts_dict = {}
    for user in data:
        user_contacts_number_list = []
        contact_data = data[user]["contact"]
        for contact in contact_data:
            user_contacts_number_list.append(contact_data[contact]["number"])

        contacts_dict[user] = user_contacts_number_list

    return contacts_dict


def extract_admin_contact():
    admin_number_list = []
    data = fb.get("/admin", None)
    for contact in data:
        admin_number_list.append(data[contact]["number"])
    return admin_number_list


def add_contact_info(number, name, user):
    data = {
        "name": name,
        "user": user
    }
    query = '/contact/' + number
    fb.patch(query, data)


def get_contact_number(username, contact_name):
    query = "/user/" + username + "/contact/" + contact_name
    contact_info = fb.get(query, None)
    contact_number = contact_info["number"]
    return contact_number


def is_toy_message_send_by_email(username, contact_name):
    query = "/user/" + username + "/contact/" + contact_name
    contact_info = fb.get(query, None)
    return contact_info["isToySendByEmail"]


def get_contact_email(username, contact_name):
    query = "/user/" + username + "/contact/" + contact_name
    contact_info = fb.get(query, None)
    contact_email = contact_info["email"]
    return contact_email


def get_schedule(username):
    """
    :param username: string of user
    get schedule<dict> --> schedule_list<list> [baseline, implementation, postline]
    """
    query = "/user/" + username + "/schedule"
    schedule = fb.get(query, None)
    stage_list = ["baseline", "implementation", "postline"]
    weeks = 0
    schedule_list = []
    for key in stage_list:
        weeks += schedule[key]
        schedule_list.append(weeks)
    return schedule_list


def get_contact_name_and_username_by_number(number):
    query = "/contact/" + number
    data = fb.get(query, None)
    return data["name"], data["user"]

# print(contact_list_extractor())


###################################################################

WEEK_ORDER = ["week1", "week2", "week3", "week4", "week5", "week6", "week7"]
DAY_ORDER = ["day1", "day2", "day3", "day4", "day5", "day6", "day7"]

def get_daily_message_record(username):
    contact_list = get_contacts(username)
    data = {}
    for contact in contact_list:
        data[contact] = get_contact_daily_message_record(contact)
    data["user"] = username
    return data


def get_contact_daily_message_record(contact):
    query = "/logging/response/" + contact + "/dailyMessage"
    dailyMessage = fb.get(query, None)

    weekly_results = []
    for week in range(len(dailyMessage)):
        times = []
        sub = 0
        for day in DAY_ORDER:
            try:
                time = dailyMessage[WEEK_ORDER[week]][day]["times"]
                sub += int(time)
                times.append(time)
            except KeyError:
                continue
        weekly_results.append((WEEK_ORDER[week], sub, times))
    return weekly_results


def get_contacts(username):
    query = "/user/" + username + "/contact"
    data = fb.get(query, None)
    contact_list = []
    for contact in data:
        contact_list.append(contact)
    return contact_list


import csv


def dailyMessage2CSV(data):
    with open('data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Name", "Week", "Sub", "Original record"])
    for d in data:
        if d != "user":
            csv += d + "," + record_transfer(data[d][0]) + "\n"
            for i in range(1, len(data[d])):
                csv += "," + record_transfer(data[d][i]) + "\n"
    return csv


def record_transfer(data):
    week, sub, record = data
    r = ""
    for i in record:
        r += str(i) + ","
    result = week + "," + str(sub) + "," + r[:-1]
    return result


