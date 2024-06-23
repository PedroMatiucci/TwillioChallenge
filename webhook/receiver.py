from flask import Flask, request, jsonify, redirect
from twilio.twiml.messaging_response import MessagingResponse
from textSpeech.convert import Convert
import requests
import os
from dotenv import load_dotenv


# ngrok http --domain=martin-polished-remarkably.ngrok-free.app 8080
app = Flask(__name__)

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
username = account_sid
password = auth_token

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_reply():
    conversor = Convert()
    try:
        data = request.form.to_dict()
    except Exception as e:
        print(e)
    query = data['Body']
    sender_id = data['From']
    if 'MediaUrl0' in data.keys():
        audio_test = conversor.speech_to_text(data['MediaUrl0'],)
        print(audio_test)
    return 'OK', 200
#         transcript = transcript_audio(data['MediaUrl0'])
#         if transcript['status'] == 1:
#             print(f'Query - {transcript["transcript"]}')
#             response = chat_completion(transcript['transcript'])
#         else:
#             response = config.ERROR_MESSAGE
#     else:
#         print(f'Query - {query}')
#         response = chat_completion(query)
#     print(f'Response - {response}')
#     send_message(sender_id, response)
#     print('Message sent.')

if __name__ == '__main__':
    app.run(port=8080)
