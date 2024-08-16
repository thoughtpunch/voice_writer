import os
import json
import openai
from openai import OpenAI

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


JSON_TEMPLATE = """
{
    "ManuscriptType": "memoir",
    "ManuscriptTitle": "Dance of Hope: A Childhood Journey.",
    "Genre": ["non-fiction", "autobiography"],
    "Sections": [
        {
            "SectionType": "title_page",
            "title": "Dance of Hope: A Childhood Journey.",
            "text_with_timestamps": [
                "1
                00:00:00,000 --> 00:00:10,460
                So this file is the beginning of my memoir. The memoirs titled Dance Hope, A Childhood Journey."
            ]
        },
        {
            "SectionType": "preface",
            "title": "preface",
            "text_with_timestamps": [
                "1
                00:00:00,000 --> 00:00:10,460
                So this file is the beginning of my memoir. The memoirs titled Dance Hope, A Childhood Journey."
            ]
        },
        {
            "SectionType": "chapter",
            "title": "Chapter 1",
            "text_with_timestamps": [
                "2
                00:00:11,620 --> 00:00:19,140
                Chapter 1. I was born and then I got older and then I died. The end.'"
            ]
        }
    ]
}
"""


class ManuscriptDetailSummarizer:
    def __init__(self, transcription: str):
        self.transcription = transcription
        self.summary = None

    def _manuscript_extraction_prompt(self):
        return f"""
                    Context:
                    I have a SRT audio transcription of an audio file from my VoiceWriter app. This transcription includes content that may reference different parts of a manuscript, such as chapters, memoirs, or other sections. In my app there is exactly one `Manuscript` that can have many sections like 'Chapter 1', 'Abstract', 'Table of Contents', etc. A `Section` is analogous to a chapter or section in a book or manuscript. A `Manuscript` can have many `Sections`, but a child `Section` can only belong to one `Manuscript`. A `Section` can contain many group timestamps or blocks of texts. For example, an SRT audio transcription may contain timestamps and text blocks like "Chapter 1", "Chapter 2", "Preface", "Acknowledgments", etc. The goal is to extract and categorize these sections and timestamps from the SRT audio transcription into a structured JSON format.

                    Objective:
                    Group timestamps from a SRT audio transcript while categorizing and extracting key details from the SRT audio transcription. Identify the ManuscriptType, SectionType, and Genre(s) based on the content. The goal is to accurately classify each part of the transcription according to the manuscript's structure and type, and group in corresponding sections in time order by timestamps. Each timestamped section in the transcription may represent a different `Section`, or may belong to the previous section. If a timestamped section does not have an unambiguous `Section` classification, group it under the previous timestamped Section. For example, if a timestamped section mentions "Chapter 1", it should be classified as a "Chapter" with the title "Chapter 1", all the following timestamped sections should be classified as part of "Chapter 1" until a new chapter is mentioned and grouped in the `Section` model as an attribute `text`. When a timestamp could contain data for multiple Section records, duplicate the timestamped data and label according to the JSON schema example below. The schema returned should be in JSON format and look exactly like this JSON schema example:

                    Example:
                    SRT TRANSCRIPTION:
                    1
                    00:00:00,000 --> 00:00:10,460
                    So this file is the beginning of my memoir. The memoirs titled Dance Hope, A Childhood Journey.

                    2
                    00:00:11,620 --> 00:00:19,140
                    Chapter 1. I was born and then I got older and then I died. The end.

                    OUTPUT JSON SCHEMA:
                    '{JSON_TEMPLATE}'

                    Specific Questions/Requirements:

                    ManuscriptType: Based on the transcription, determine the most appropriate ManuscriptType. Consider options like "book", "memoir", "thesis", etc.
                    SectionType: Identify the SectionType for each distinct part of the transcription. For example, if the transcription mentions "Chapter 1", it should be classified as a "Chapter".
                    Genre: If possible, infer the genre of the manuscript from the text. This could include options like "fiction", "non-fiction", "memoir", "poetry", etc.
                    Preferred Format/Details:

                    Provide the identified ManuscriptType, SectionType, and Genre for the given transcription in JSON format.
                    If the transcription contains multiple sections or types, list each one separately with its corresponding classification.
                    Explain any assumptions made during the classification process.
                    Additional Considerations:

                    If the transcription mentions specific keywords or phrases that strongly suggest a particular type or section (e.g., "Chapter", "Memoir", "Abstract"), prioritize those cues in your classification.
                    For ambiguous cases, offer the most likely classifications based on the content provided.
                    Please return a JSON object with this data. I can only accept JSON data.

                    HERE IS THE TRANSCRIPTION: {self.transcription} .\n\n USE THE TRANSCRIPTION I JUST PROVIDED.
            """

    def summarize(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": self._manuscript_extraction_prompt(),
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
