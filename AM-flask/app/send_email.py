import smtplib
from email.mime.text import MIMEText
from time import sleep

import send_sms
import ENV_VAR as env

_ADMIN_EMAIL = "yi.zheng3@uqconnect.edu.au"
_ADMIN_LIST = ["leglars@gmail.com", "yi.zheng3@uqconnect.edu.au"]
# _SERVICE_EMAIL = "yi.zheng3@uqconnect.edu.au"
_SERVICE_EMAIL = "leglars@gmail.com"
_TEST_EMAIL = "this is a test email from ThinkingofYou"


def send_toy_message(username, contact_name, to_email=_ADMIN_EMAIL, email_content=_TEST_EMAIL):
    if username and contact_name:
        email_content = "I'm Thinking of You, " + contact_name + "!\n \000\000\000-- From Trish [TOY]"
    msg = MIMEText(email_content)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = "TOY message from " + username
    msg['From'] = _SERVICE_EMAIL
    msg['To'] = to_email

    # Send the message via our own SMTP server.
    s = smtplib.SMTP("smtp.google.com")
    s.login(_SERVICE_EMAIL, "1936887IWMzy")
    s.send_message(msg)
    s.quit()
    print("sending success")


def send_email():
    SERVER = "smtp.office365.com"
    FROM = "yi.zheng3@uqconnect.edu.au"
    TO = ["leglars@gmail.com"] # must be a list

    SUBJECT = "Hello!"
    TEXT = "This is a test of emailing through smtp in google."

    # Prepare actual message
    message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail
    server = smtplib.SMTP(SERVER, 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("yi.zheng3@uqconnect.edu.au", "1936887IWMuq")
    server.sendmail(FROM, TO, message)
    server.quit()


send_email()


class EmailHandler():
    """
    IMPORTANT NOTE:
    in order to access a gmail account with this handler,
    your account needs 'foreign-access' enabled (follow these steps):
    login to the account
    go here--> https://accounts.google.com/b/0/DisplayUnlockCaptcha
    press 'Continue'
    Done.
    """

    def __init__(self, service_account_info=env.SERVICE_EMAIL_ACCOUNT):
        self._service = service_account_info["account"]
        self._password = service_account_info["password"]
        self._host = service_account_info["host"]
        self._port = service_account_info["port"]
        self._recognizer = service_account_info["recognizer"]

    def send_mail(self, receivers, subject, text):
        """
        :param receivers: a email<string> or a list of email<string>
        :param subject: string
        :param text: string
        """

        if not isinstance(receivers, list):
            receivers = [receivers]

        # Send the message via our own SMTP server, but don't include the envelope header
        smtp = smtplib.SMTP(self._host, self._port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self._service, self._password)

        for receiver in receivers:

            msg = MIMEText(text)
            msg['Subject'] = subject
            # UserFirstName UserLastName <FromEmail@example.com>
            msg['From'] = "ToY <" + self._service + ">"
            msg['To'] = receiver

            try:
                smtp.sendmail(self._service, receiver, str(msg))
            except smtplib.SMTPRecipientsRefused:
                res = send_sms.error_toy_email_sending_fail(receiver)
            except smtplib.SMTPSenderRefused:
                # TODO threading a new thread
                self.send_mail(receiver, subject, text)

        smtp.quit()

        return True


email = EmailHandler()
email.send_mail("leglars@gmail.com", "testing", "this is a message from toy")
