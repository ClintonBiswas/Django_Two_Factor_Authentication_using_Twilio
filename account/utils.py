# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'your account id'
auth_token = 'your auth token'
client = Client(account_sid, auth_token)

def send_sms(code_user, phone_number):
    message = client.messages \
                .create(
                     body=f'Hi, Your User verification code is {code_user}',
                     from_='your trial number',
                     to=f'{phone_number}'
                 )

    print(message.sid)