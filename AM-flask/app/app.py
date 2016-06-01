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
    print(res)


@app.route("/receive", methods=['GET', 'POST'])
def receive():
    pass
    # resp = twilio.twiml.Response()
    # resp.message("hello, this is haha")
    # return str(resp)


@app.route("/income", methods=['GET', 'POST'])
def reply():

    def logger(context_data):
        if not context_data[from_num]:
            send_sms.error_response_number(text, from_num)

        contact = context_data[from_num]["name"]
        user = context_data[from_num]["user"]

        log_result = log.daily_logging(user, contact, text)
        if log_result == 1:
            pass
        elif log_result == 2:
            pass
        elif not log_result:
            # send_sms.error_response_warning(text)
            return "error response warning"

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
    from_num = request.values.get('From', None)
    text = str(request.values.get('Text', None))

    data = fb.get("/contact", None)

    logger(data)



    response = "we got your message: " + text
    # res = send_sms.reply_message(from_num, response)
    res = send_sms.send_message(from_num, response)

    print(res)
    print(type(res))
    return "replied"


    #
    #
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
