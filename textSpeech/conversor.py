import requests
import uuid
import soundfile as sf
import os
from pydub import AudioSegment
from dotenv import load_dotenv


class Conversor:
    load_dotenv()
    os.environ["TWILIO_ACCOUNT_SID"] = os.getenv("TWILIO_ACCOUNT_SID")
    os.environ["TWILIO_AUTH_TOKEN"] = os.getenv("TWILIO_AUTH_TOKEN")

    def __init__(self):
        self.username = os.getenv("TWILIO_ACCOUNT_SID")
        self.password = os.getenv("TWILIO_AUTH_TOKEN")

    def convert_to_mp3(self, media_url):
        ogg_file_path = f'audios/files/{uuid.uuid1()}.ogg'
        mp3_file_path = f'audios/files/{uuid.uuid1()}.mp3'
        data = requests.get(media_url, auth=(self.username, self.password))
        with open(ogg_file_path, 'wb') as file:
            file.write(data.content)
        audio_data, sample_rate = sf.read(ogg_file_path)
        sf.write(mp3_file_path, audio_data, sample_rate)
        os.unlink(ogg_file_path)
        return mp3_file_path

    def convert_to_ogg(self, source_file):
        destination = f'audios/audiosGenerated/{uuid.uuid1()}.ogg'
        segment = AudioSegment.from_mp3(source_file)
        segment.export(destination, format="ogg", codec='libopus')
        return destination
