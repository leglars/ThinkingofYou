import send_sms
import firebase_logging as log

from flask import Flask, redirect, request, render_template

from firebase import firebase
fb = firebase.FirebaseApplication("https://burning-heat-7654.firebaseio.com/", None)

app = Flask(__name__)


@app.route('/')
def hello_world():
    # log.query_builder('yi', "jolly")
    # return 'Hello World!'
    return render_template("index.html")


@app.route('/sending')
def send_message():

    res = send_sms.send_message()
    return "a message be sent"


@app.route("/receive", methods=['GET', 'POST'])
def receive():
    pass


@app.route("/income", methods=['GET', 'POST'])
def reply():

    def logger(from_number, response):
        data = fb.get("/contact", None)
        if not data[from_number]:
            pass
            # send_sms.error_response_number(response, from_number)

        contact = data[from_number]["name"]
        user = data[from_number]["user"]

        if log.daily_logging(user, contact, from_number, response):
            return True
        return False

    """
    POST /income HTTP/1.1
    Host: 04f80d2d.ngrok.io   // testing port
    Content-Length: 140
    Accept-Encoding: gzip, deflate
    Accept: */*
    User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.35 Safari/535.1
    connection: close
    X-Plivo-Signature: 1VBRa9BARNAi8GSusYTNxpE3T6U=
    Content-Type: application/x-www-form-urlencoded
    X-Forwarded-For: 54.177.70.197

    To=61429968959&From=61478417108&TotalRate=0&Units=1&Text=How+are+you&TotalAmount=0&Type=sms&MessageUUID=ca425462-27f0-11e6-890b-22000ae90d37
    """
    try:
        from_num = "+" + request.values.get('From', None)
        text = str(request.values.get('Text', None))

        if logger(from_num, text):
            res = send_sms.reply_message(from_num)
            return "replied"

        response = "Sorry, we got some problems. Could you resend you response to us again. Thank you"
        res = send_sms.reply_message(from_num, response)
        return "fail to record"
    except:
        return "reply module failure"


    # # Message UUID for which the details will be retrieved
    # params = {'message_uuid': '0936ec98-7c4c-11e4-9bd8-22000afa12b9'}
    # # Fetch the details
    # response = p.get_message(params)


@app.route("/delivery_report/", methods=['GET', 'POST'])
def report():
    # Sender's phone number
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # Status of the message
    status = request.values.get('Status')
    # Message UUID
    uuid = request.values.get('MessageUUID')

    if status != "delivered":
        pass

    # Prints the status of the message
    print("From: %s, To: %s, Status: %s, MessageUUID: %s" % (from_number, to_number, status, uuid))
    return "Delivery status reported"


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()