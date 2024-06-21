from openai import OpenAI
from pathlib import Path


class Convert:
    def __init__(self):
        self.client = OpenAI()
        self.speech_file_path = Path(__file__).parent / "audiosGenerated" / "audio.mp3"

    def speech_to_text(self, path):
        audio_file = open(path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcription.text

    def text_to_speech(self, text):
        response = self.client.audio.with_streaming_response.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(self.speech_file_path)
