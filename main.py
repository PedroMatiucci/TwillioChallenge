import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

from_number = "whatsapp:+14155238886"
to_number = "whatsapp:+5516997088287"

message = client.messages.create(
    body="Hello there!",
    from_=from_number,
    to=to_number,
)

print(message.body)
