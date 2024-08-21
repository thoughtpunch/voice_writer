import os
import openai
from openai import OpenAI


openai.api_key = os.getenv('OPENAI_API_KEY')


class CoverArtGenerator:
    def __init__(self, audio_metadata: dict) -> None:
        # The parsed tags and metadata for the audio file
        self.audio_metadata = audio_metadata
        self.generated_cover_url = None
        pass

    def _cover_art_prompt(self):
        prompt = "A cover design for an album or book cover. The design should be inspired by the audio file metadata provided: "
        if 'title' in self.audio_metadata:
            prompt += f"Title: '{self.audio_metadata['title']}', "
        if 'keywords' in self.audio_metadata:
            prompt += f"Keywords: '{', '.join(self.audio_metadata['keywords'])}', "
        if 'description' in self.audio_metadata:
            prompt += f"Description/Summary: '{self.audio_metadata['description']}', "
        if 'album' in self.audio_metadata:
            prompt += f"Album: '{self.audio_metadata['album']}', "
        return prompt

    def generate_cover_art(self):
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=self._cover_art_prompt(),
                size="1024x1024",
                n=1,
            )
            if response and response.data and response.data[0].url:
                self.generated_cover_url = response.data[0].url
                return self
            else:
                raise Exception("Failed to generate cover art")
        except Exception as e:
            print(f"Error generating cover art: {e}")

    @property
    def client(self):
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
