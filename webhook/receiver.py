from flask import Flask, request
from textSpeech.text_speech import TextSpeech
from chatbot.chatbot import Chatbot
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import uuid
from database.crud import Crud


# ngrok http --domain=martin-polished-remarkably.ngrok-free.app 8080
app = Flask(__name__)

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
from_number = "whatsapp:+14155238886"
username = account_sid
password = auth_token
speech = TextSpeech()
crud = Crud()


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_reply():
    data = request.form.to_dict()
    text_message = data['Body']
    sender_id = data['From']
    chatbot = Chatbot(sender_id)
    response_twilio = MessagingResponse()
    if 'MediaUrl0' in data.keys():
        audio_text = speech.speech_to_text(data['MediaUrl0'], )
        print(audio_text)
        response = chatbot.answer_question(audio_text)
        answer_path = speech.text_to_speech(response)
        path = crud.upload_to_gcs(answer_path, f'{uuid.uuid1()}.ogg')
        os.unlink(answer_path)
        msg = response_twilio.message(response)
        msg.media(path)
    else:
        response = chatbot.answer_question(text_message)
        response_twilio.message(response)
    return str(response_twilio)


def send_text_message(to_number, text_message):
    client.messages.create(
        body=text_message,
        from_=from_number,
        to=to_number,
    )


if __name__ == '__main__':
    app.run(port=8080)
