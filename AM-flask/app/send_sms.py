# from twilio.rest import TwilioRestClient
#
# account_sid = 'ACd7a0898f812377ef06121f8611f11b1e'
# auth_token = 'eaae9bf97f64e5d844d5c65247216220'
# client = TwilioRestClient(account_sid, auth_token)

import plivo

auth_id = "MAMGEWZGE5NWRJNME3ZJ"
auth_token = "ZTNiNmIyZDU1N2JjNWQ4MGM5NWE4NmI5MjM1OThm"

p = plivo.RestAPI(auth_id, auth_token)

_ADMIN_NUMBER = "+61478417108"
_SERVICE_NUMBER = "+61400357926"


def send_message(to, question):
    # client.messages.create(
    #     to=to,
    #     from_=_SERVICE_NUMBER,
    #     body=question
    # )

    params = {
        'src': _SERVICE_NUMBER,
        'dst': _ADMIN_NUMBER,
        'text': "this is a test message from plivo",
        # 'url': "http://thinkingofyou.uqcloud.net/automessage/report",
        'method': "POST"
    }

    response = p.send_message(params)


def error_response_warning(error, user, name, question):
    error_body = "User " + user + "'s contact " + name + " may arouse a wrong response for question " + question \
                 + "\nThe response is here: " + error
    client.messages.create(
        to=_ADMIN_NUMBER,
        from_=_SERVICE_NUMBER,
        body=error_body
    )


def error_response_number(text, number):
    error_body = "Get a response from an unknown number: " + number + "\nThe content is here: " + text
    client.messages.create(
        to=_ADMIN_NUMBER,
        from_=_SERVICE_NUMBER,
        body=error_body
    )
