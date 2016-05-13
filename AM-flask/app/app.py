from flask import Flask, redirect, request
import twilio.twiml
from firebase import firebase
fb = firebase.FirebaseApplication("https://burning-heat-7654.firebaseio.com/", None)
import send_sms

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/receive", methods=['GET', 'POST'])
def hello():
    resp = twilio.twiml.Response()
    resp.message("hello, this is haha")
    return str(resp)


@app.route("/income", methods=['GET', 'POST'])
def reply():

    from_num = request.values.get('From', None)
    from_num = "+" + str(from_num).strip()
    # the number get from http is " 61400111222"
    text = request.values.get('Body', None)
    text = str(text)
    data = fb.get("/contact", None)

    # if not data[from_num]:
    #     send_sms.error_response_number(text, from_num)

    name = data[from_num]["name"]
    user = data[from_num]["user"]

    text_s = text.split(' ')  # place here because error catch need a full text string

    i = 0
    yes = ["yes", "Yes", "YES"]
    no = ["no", "No", "NO"]

    query = "/logging/week1/day1/" + user + "/" + name + "/"

    for word in text_s:
        if word in yes or word in no:
            if word in yes:
                connected = 1
            else:
                connected = 0

            fb.patch(query, {'connected': connected})
            # fb.post_async(query, data)
            return "send q2 and connected yes"

        elif word == "time" or word == "times":
            time = int(text[i-1])
            fb.patch(query, {'time': time})
            # fb.put(query, "123", {'time': time})    #  put is work too
            return "time yes"
        i += 1
    # send_sms.error_response_warning(text)
    return "error response warning"


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
