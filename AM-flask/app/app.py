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
    str_from_num = "+" + str(from_num).strip()

    data = fb.get("/contact", None)
    name = data[str_from_num]["name"]



if __name__ == '__main__':
    app.run()
