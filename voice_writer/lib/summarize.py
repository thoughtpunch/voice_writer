import os
import json
import openai
from openai import OpenAI


# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


class TranscriptionSummarizer:
    def __init__(self, transcription: str):
        self.transcription = transcription
        self.summary = None

    def summarize(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following text transcription from an audio file. It is highly likely that this text is an audio recording from a book author writing a book. Here is the text transcript:\n\n{self.transcription}\n\n. Please come up with an appropriate 'title', 'summary', and 'keywords'. Please return a JSON object",
                }
            ],
        )
        self.summary = json.loads(
            response.choices[0].message.content
        )
        return self.summary

    @property
    def client(self):
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
