# from twilio.rest import TwilioRestClient
#
# account_sid = 'ACd7a0898f812377ef06121f8611f11b1e'
# auth_token = 'eaae9bf97f64e5d844d5c65247216220'
# client = TwilioRestClient(account_sid, auth_token)

import plivo
import ENV_VAR as ENV

auth_id = ENV.PLIVO["id"]
auth_token = ENV.PLIVO["token"]

p = plivo.RestAPI(auth_id, auth_token)

_ADMIN_NUMBER = "61478417108"
_ADMIN_LIST = ["61424945548", "61478417108"]
_SERVICE_NUMBER = "61429968959"
_TEST_QUESTION = "this is a test message from ThinkingofYou"


# Auto daily message start #####################################

def send_message(to_number=_ADMIN_NUMBER, question=_TEST_QUESTION):
    # client.messages.create(
    #     to=to,
    #     from_=_SERVICE_NUMBER,
    #     body=question
    # )

    params = {
        'src': _SERVICE_NUMBER,
        'dst': to_number,
        'text': question,
        # 'url': "http://thinkingofyou.uqcloud.net/automessage/report",
        'method': "POST"
    }

    response = p.send_message(params)
    """
    This is an example of response:
    tuple(int, dictionary{})
    (
        202,
        {
            'message_uuid': ['3829ba15-12c8-499b-aa88-730619e17272'],
            'message': 'message(s) queued',
            'api_id': 'b1d5f55d-27f8-11e6-be4a-22000ae40186'
        }
    )
    """
    return response


def reply_message(from_number, text="Thanks, we've received your message.", to_number=_SERVICE_NUMBER):
    """
    :param from_number: get who send this message
    :param text: this is the default message
    :param to_number: here, we just have 1 service number, if the app need send many messages, maybe have more than one
                        service number, so this parameter would be useful to identify
    """
    params = {
        "src": to_number,
        "dst": from_number,
        "text": text,
        "method": "POST"
    }

    # # Generate a Message XML with the details of
    # # the reply to be sent.
    # r = plivoxml.Response()
    # r.addMessage(text, **params)

    response = p.send_message(params)
    return response


def error_response_warning(error, user, name, question):
    error_body = "User " + user + "'s contact " + name + " may arouse a wrong response for question " + question \
                 + "\nThe response is here: " + error

    params = {
        'src': _SERVICE_NUMBER,
        'dst': _ADMIN_NUMBER,
        'text': error_body,
        # 'url': "http://thinkingofyou.uqcloud.net/automessage/report",
        'method': "POST"
    }

    # client.messages.create(
    #     to=_ADMIN_NUMBER,
    #     from_=_SERVICE_NUMBER,
    #     body=error_body
    # )


def error_response_number(text, number):
    error_body = "Get a response from an unknown number: " + number + "\nThe content is here: " + text

    for num in _ADMIN_LIST:
        send_message(num, error_body)


def error_logging_fail(text, number):
    warning = "WARNING: logging fail\nNumber: " + number + "\nContent: " + text
    send_message(_ADMIN_NUMBER, warning)


# Auto daily message End ###################################################

# TOY message start ########################################################

def send_toy_message(contact_name, username, to_number=_ADMIN_NUMBER):
    message = "I'm Thinking of You, " + contact_name + "!\n-- A message from " + username
    return send_message(to_number, message)

def error_toy_message_sending_fail(username, to_number=_ADMIN_NUMBER):
    warning = "WARNING: " + username + " can't send toy message, post function failure!"
    return send_message(to_number, warning)
