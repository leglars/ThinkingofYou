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
