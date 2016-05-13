from twilio.rest import TwilioRestClient

account_sid = 'ACd7a0898f812377ef06121f8611f11b1e'
auth_token = 'eaae9bf97f64e5d844d5c65247216220'
client = TwilioRestClient(account_sid, auth_token)


def send_message(to, question):
    client.messages.create(
        to=to,
        from_="+61400357926",
        body=question
    )
