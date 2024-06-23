from openai import OpenAI
from pathlib import Path
import requests
import uuid
import soundfile as sf
import os



class Convert:
    def __init__(self):
        self.client = OpenAI()
        self.speech_file_path = Path(__file__).parent / "audiosGenerated" / "audio.mp3"
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.username = account_sid
        self.password = auth_token

    def speech_to_text(self, media_url):
        path = self.convert_to_mp3(media_url)
        audio_file = open(path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        transcription_text = transcription.text
        return transcription_text

    def text_to_speech(self, text):
        response = self.client.audio.with_streaming_response.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(self.speech_file_path)


##descobrir como autenticar os arquivos de audio
    def convert_to_mp3(self, media_url):
        try:
            ogg_file_path = f'files/{uuid.uuid1()}.ogg'
            data = requests.get(media_url, auth=(self.username, self.password))
            print(data)
            with open(ogg_file_path, 'wb') as file:
                file.write(data.content)
            audio_data, sample_rate = sf.read(ogg_file_path)
            mp3_file_path = f'files/{uuid.uuid1()}.mp3'
            sf.write(mp3_file_path, audio_data, sample_rate)
            os.unlink(ogg_file_path)
            return mp3_file_path
        except Exception as e:
            print('Error at transcript_audio...')
            print(e)
            return None
