import send_sms
import firebase_logging as log
import dbAPI as db

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
    contact_list = db.contact_list_extractor()
    for sub_list in contact_list:
        for number in sub_list:
            res = send_sms.send_message(number)
    return "a message be sent"


@app.route("/receive", methods=['GET', 'POST'])
def receive():
    pass


@app.route("/income", methods=['GET', 'POST'])
def reply():

    def logger(from_number, message):
        data = fb.get("/contact", None)
        if not data[from_number]:
            send_sms.error_response_number(message, from_number)
            return False

        try:
            contact = data[from_number]["name"]
            user = data[from_number]["user"]

            if log.daily_logging(user, contact, from_number, message):
                return True
            return False
        except:
            # warning = "WARN: can't log message"
            send_sms.error_logging_fail(message, from_number)
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

        response = "Sorry, we got some problems. Could you send your response again. Thank you!\nIf you got this message more than one, just leave it."
        res = send_sms.reply_message(from_num, response)
        return "fail to record"
    except Exception as err:
        print(err)
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
