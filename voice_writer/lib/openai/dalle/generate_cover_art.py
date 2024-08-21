import os
import openai
import requests
from openai import OpenAI
from io import BytesIO
from PIL import Image


openai.api_key = os.getenv('OPENAI_API_KEY')


class CoverArtGenerator:
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description
        self.generated_cover_image = BytesIO()
        self.generated_cover_name = title
        pass

    def _cover_art_prompt(self):
        return f"""
            Cover art for an audio file or audiobook titled '{self.title}'. The description of the audio file is as follows: '{self.description}'.
        """

    def generate_cover_art(self):
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=self._cover_art_prompt(),
                size="1024x1024",
                n=1,
            )
            if response and response.data:
                image_url = response.data[0].url
                # Download the image using requests
                image_content = requests.get(image_url).content
                image = Image.open(BytesIO(image_content))

                # Save the image to a Django FileField
                image_io = BytesIO()
                image.save(image_io, format='PNG')
                image_name = f"{self.title}_cover.png"

                self.generated_cover_image = image_io
                self.generated_cover_name = image_name
                return self
            else:
                raise Exception("Failed to generate cover art")
        except Exception as e:
            print(f"Error generating cover art: {e}")

    @property
    def client(self):
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
