import os
import json
import openai
from openai import OpenAI
from typing import Optional

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


class TranscriptionSummarizer:
    def __init__(self, author: Optional[str], title: Optional[str], transcription: str):
        self.author = author
        self.title = title
        self.transcription = transcription
        self.summary = None

    def _summary_prompt(self):
        return f"""
            Please summarize the following text transcription from an audio file.
            The context is that this audio transcription is was authored by {self.author}, an author who is dictating a story, book, or manuscript using their voice.
            The title of the audio file is '{self.title}' which may be related to theme or topic of the transcription or may just be a random file name.
            Here is the text transcript:\n\n'{self.transcription}'.\n\n
            Using the information I have provided please generate an appropriate 'title', 'summary', and 'keywords' and return in JSON format. Please return a JSON object.
            """

    def summarize(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": self._summary_prompt(),
                }
            ],
        )
        if response and response.choices:
            self.summary = json.loads(
                response.choices[0].message.content
            )
            return self.summary
        else:
            raise Exception("Failed to summarize the transcription")

    @property
    def client(self):
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
