from firebase import firebase
fb = firebase.FirebaseApplication("https://burning-heat-7654.firebaseio.com/", None)


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

# print(contact_list_extractor())
