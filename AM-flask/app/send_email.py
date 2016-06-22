import smtplib
from email.mime.text import MIMEText
from threading import Thread

import ENV_VAR as env
import send_sms

_ADMIN_EMAIL = "leglars@gmail.com"


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
        self._backup_email_info = service_account_info["backupEmailAccount"]

    def send_mail(self, receivers=_ADMIN_EMAIL, text="This is a message from TOY.", subject="I'm Thinking of You!"):
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
            # set up display name by the following format
            # UserFirstName UserLastName <FromEmail@example.com>
            msg['From'] = self._recognizer + " <" + self._service + ">"
            msg['To'] = receiver

            try:
                smtp.sendmail(self._service, receiver, str(msg))
            except smtplib.SMTPRecipientsRefused:
                res = send_sms.error_toy_email_sending_fail(receiver)
            except smtplib.SMTPSenderRefused:
                # if self.send_email_by_backup_account(receiver, subject, text):
                #     continue
                # else:
                #     # TODO a error reporter
                #     pass
                pass

        return True

    def multi_send(self, smtp, receiver, subject, text, msg):
        try:
            smtp.sendmail(self._service, receiver, str(msg))
        except smtplib.SMTPRecipientsRefused:
            res = send_sms.error_toy_email_sending_fail(receiver)
        except smtplib.SMTPSenderRefused:
            # if self.send_email_by_backup_account(receiver, subject, text):
            #     pass
            # else:
            #     pass
            pass

    def send_email_by_backup_account(self, receivers, subject, text):

        server = self._backup_email_info["host"]
        port = self._backup_email_info["port"]
        service_email = self._backup_email_info["account"]

        password = self._backup_email_info["password"]

        if not isinstance(receivers, list):
            receivers = [receivers]

        # Send the message via our own SMTP server, but don't include the envelope header
        smtp = smtplib.SMTP(server, port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(service_email, password)

        for receiver in receivers:

            msg = MIMEText(text)
            msg['Subject'] = subject
            msg['From'] = self._recognizer + " <" + service_email + ">"
            msg['To'] = receiver
            try:
                smtp.sendmail(service_email, receiver, str(msg))
                break
            except:
                smtp.quit()
                return False

        smtp.quit()
        return True


# class SendMail(Thread):
#     def __init__(self, receivers=_ADMIN_EMAIL, text="This is a message from TOY.", /
#                   subject="I'm Thinking of You!", service_account_info=env.SERVICE_EMAIL_ACCOUNT):
#
#         self._service = service_account_info["account"]
#         self._password = service_account_info["password"]
#         self._host = service_account_info["host"]
#         self._port = service_account_info["port"]
#         self._recognizer = service_account_info["recognizer"]
#         self._backup_email_info = service_account_info["backupEmailAccount"]
#         self._receivers = receivers
#         self._text = text
#         self._subject = subject
#     def run(self):
#         try:
#             if not isinstance(self._receivers, list):
#                 receivers = [self._receivers]
#
#             # Send the message via our own SMTP server, but don't include the envelope header
#             smtp = smtplib.SMTP(self._host, self._port)
#             smtp.ehlo()
#             smtp.starttls()
#             smtp.ehlo()
#             smtp.login(self._service, self._password)
#
#             for receiver in receivers:
#
#                 msg = MIMEText(self._text)
#                 msg['Subject'] = self._subject
#                 # set up display name by the following format
#                 # UserFirstName UserLastName <FromEmail@example.com>
#                 msg['From'] = self._recognizer + " <" + self._service + ">"
#                 msg['To'] = receiver
#
#                 try:
#                     smtp.sendmail(self._service, receiver, str(msg))
#                 except smtplib.SMTPRecipientsRefused:
#                     res = send_sms.error_toy_email_sending_fail(receiver)
#                 except smtplib.SMTPSenderRefused:
#                     # TODO threading a new thread
#                     if self.send_email_by_backup_account(receiver, self._subject, self._text):
#                         continue
#                     else:
#                         # TODO a error reporter
#                         pass
#         except:
#               pass
#
#         print("finish thread")
#
# # email = EmailHandler()
# # email.send_mail("leglars@gmail.com", "testing", "this is a message from toy")
#
#
# def send():
#     if True:
#         mail = SendMail("leglars@gmail.com", "testing", "this is a message from toy")
#         mail.run()
#
#         mail = SendMail("leglars@gmail.com", "testing", "this is a message")
#         mail.run()
#
#         print("end if")
#
#     return "return"
#
# print(send())


