import send_sms
import firebase_logging as log
import dbAPI as db
import ENV_VAR as ENV
import timezone_handler as t

from flask import Flask, redirect, request, render_template

from firebase import firebase
fb = firebase.FirebaseApplication(ENV.FIREBASE_LINK, None)

app = Flask(__name__)


##############################
# url start
##############################


@app.route('/')  # index page
def hello_world():
    # log.query_builder('yi', "jolly")
    # return 'Hello World!'
    return render_template("index.html")


@app.route("/thinkingofyou", methods=['GET', 'POST'])
def send_thinkingofyou_message():
    contact_name = request.values.get('contact', None)
    username = request.values.get('user', None).title()
    contact_number = db.get_contact_number(username, contact_name)
    # res = send_sms.send_toy_message(contact_name, username, contact_number)
    print("I'am thinking of you!" + contact_name + "\nA message from " + username)
    return "success"

# sending logic: get user and contact name
# -> get the approach of sending: email or sms or ...
# -> different function
# -> get sending report
# -> return result


@app.route("/thinkingofyou/error/report", methods=['GET', 'POST'])
def thinkingofyou_error_report():
    username = request.values.get('user', None).title()
    res = send_sms.error_toy_message_sending_fail(username)
    return "report success"

# I can have a page to distribute the url, the personal page based on the inform, like a fake login
# the http can contain a "token" to keep "safe"
# render template based on data

@app.route("/user/trish")
def trish_page():
    return render_template("user_page.html")


################### ToY End ############################

################### Daily Message ######################

# TODO send different message based on the time, or the setting period
@app.route('/sending')
def send_message():

    # def send_message_by_list(contact_list, message):
    #     for number in contact_list:
    #         res = send_sms.send_message(number, message)
    #         # print("send to: " + number)
    #         # print("content is: " + message)
    #
    # contact_dict = db.contact_list_extractor()
    # for group in contact_dict:
    #     if group == "admin":
    #         question = "The daily message has been sent"
    #         sub_list = contact_dict[group]
    #         send_message_by_list(sub_list, question)
    #
    #     elif group == "user":
    #         for user in contact_dict["user"]:
    #             question = "Have you had any contact with " + user + " today Y/N\nIf yes, how many times?"
    #             sub_list = contact_dict["user"][user]
    #             send_message_by_list(sub_list, question)

    return "all message be sent"


@app.route("/income", methods=['GET', 'POST'])
def reply():

    def logger(from_number, message):
        # print("start logger func")
        data = fb.get("/contact", None)
        # print(data)
        # print(data[from_number])
        if not data[from_number]:
            send_sms.error_response_number(message, from_number)
            return False

        # print("find the contact by number")

        try:
            contact = data[from_number]["name"]
            # print(contact)
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
        # print("get the number and text")
        from_num = request.values.get('From', None)
        text = str(request.values.get('Text', None))

        if logger(from_num, text):
            res = send_sms.reply_message(from_num)
            # print("thank you, we have received your response")
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


############################## Daily Message End ###############################


######################################################################
# deprecated url; used for developing testing
######################################################################

@app.route("/receive", methods=['GET', 'POST'])
def receive():
    pass


@app.route("/time", methods=['GET', 'POST'])
def show_time():
    return str(t.get_brisbane_time())

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
