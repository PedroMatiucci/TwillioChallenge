from openai import OpenAI
import uuid
import os
from pathlib import Path
from dotenv import load_dotenv
from textSpeech.conversor import Conversor


class TextSpeech:

    load_dotenv()
    os.environ["TWILIO_ACCOUNT_SID"] = os.getenv("TWILIO_ACCOUNT_SID")
    os.environ["TWILIO_AUTH_TOKEN"] = os.getenv("TWILIO_AUTH_TOKEN")

    def __init__(self):
        self.client = OpenAI()
        self.generated_mp3_file_path = Path(__file__).parent / "audios" / "audiosGenerated" / "audio.mp3"
        self.username = os.getenv("TWILIO_ACCOUNT_SID")
        self.password = os.getenv("TWILIO_AUTH_TOKEN")
        self.conversor = Conversor()
        self.mp3_delete = ''

    def speech_to_text(self, media_url):
        path = self.conversor.convert_to_mp3(media_url)
        audio_file = open(path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='pt'
        )
        transcription_text = transcription.text
        self.mp3_delete = path
        return transcription_text

    def text_to_speech(self, text):
        mp3_file_path = f'audios/files/{uuid.uuid1()}.mp3'
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
            response_format="mp3"
        )
        response.stream_to_file(mp3_file_path)
        destination = self.conversor.convert_to_ogg(mp3_file_path)
        os.unlink(mp3_file_path)
        os.unlink(self.mp3_delete)
        return destination
