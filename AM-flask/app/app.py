from flask import Flask, redirect, request, render_template
from firebase import firebase
fb = firebase.FirebaseApplication("https://burning-heat-7654.firebaseio.com/", None)
# import send_sms
import firebase_logging as log

app = Flask(__name__)


@app.route('/')
def hello_world():
    # log.query_builder('yi', "jolly")
    # return 'Hello World!'
    return render_template("index.html")


@app.route("/receive", methods=['GET', 'POST'])
def hello():
    pass
    # resp = twilio.twiml.Response()
    # resp.message("hello, this is haha")
    # return str(resp)


@app.route("/income", methods=['GET', 'POST'])
def reply():

    from_num = "+" + str(request.values.get('From', None)).strip()
    # the number get from http is " 61400111222"
    text = str(request.values.get('Body', None))
    data = fb.get("/contact", None)

    # if not data[from_num]:
    #     send_sms.error_response_number(text, from_num)

    contact = data[from_num]["name"]
    user = data[from_num]["user"]

    log_result = log.daily_logging(user, contact, text)
    if log_result == 1:
        pass
    elif log_result == 2:
        pass
    elif not log_result:
        # send_sms.error_response_warning(text)
        return "error response warning"


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
