from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from textSpeech.convert import Convert
from chatbot.app import Chatbot
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
from google.cloud import storage

# ngrok http --domain=martin-polished-remarkably.ngrok-free.app 8080
app = Flask(__name__)

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
from_number = "whatsapp:+14155238886"
BUCKET_NAME = "twillio-script-bucket"
SOURCE_FILE_PATH = "audiosGenerated/audio.ogg"
DESTINATION_BLOB_NAME = "audio.ogg"
CREDENTIALS_FILE = "credentials.json"
username = account_sid
password = auth_token
conversor = Convert()


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_reply():
    data = request.form.to_dict()
    text_message = data['Body']
    sender_id = data['From']
    print(sender_id)
    chatbot = Chatbot(sender_id)
    if 'MediaUrl0' in data.keys():
        audio_text = conversor.speech_to_text(data['MediaUrl0'], )
        print(audio_text)
        response = chatbot.response_question(audio_text)
        conversor.text_to_speech(response)
        upload_to_gcs(BUCKET_NAME, SOURCE_FILE_PATH, DESTINATION_BLOB_NAME, CREDENTIALS_FILE)
        send_audio_message(sender_id)
    else:
        response = chatbot.response_question(text_message)
        send_text_message(sender_id, response)
        print('Message sent.')
    return 'OK', 200


def send_text_message(to_number, text_message):
    client.messages.create(
        body=text_message,
        from_=from_number,
        to=to_number,
    )

def send_audio_message(to_number):
    audio_url = f"https://storage.cloud.google.com/twillio-script-bucket/audio.ogg"
    client.messages.create(
        media_url=audio_url,
        from_=from_number,
        to=to_number,
    )

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the target bucket
    bucket = storage_client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")



if __name__ == '__main__':
    app.run(port=8080)
