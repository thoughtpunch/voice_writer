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
            Here is an audio text transcript:\n\n'{self.transcription}'. I'll refer to this as the 'transcript'.\n\n
            Please summarize the 'transcript' and provide the following information in JSON format.\n\n
            * GENERATE A 'MANUSCRIPT/WRITTEN WORK TYPE': Please provide a 'manuscript_type' from one of these categories that most closely matches the list. It must only be one of these values: BOOK, RESEARCH_PAPER, ARTICLE, ESSAY, BLOG_POST, THESIS, SHORT_STORY, POEM, SCRIPT, PLAY, REVIEW, REPORT, LETTER, MANUAL, GUIDE, OTHER.\n\n
            * GENERATE A 'TITLE': The 'user_provided_title' of the audio file was provided as '{self.title}' which may be related to theme or topic of the transcription or may just be a random file name. You will know the 'user_provided_title' is relevant and meaningful if it corresponds to the transcript in a meaningful way. Using that context provided, please generate a nice meaningful 'title' of this audio transcript using all available information provided.\n\n
            * GENERATE AN 'AUTHOR': The 'user_provided_author' information provided for this 'transcript' is '{self.author}', who is assumed to be the author. It is possible that this 'user_provided_author' is incorrect and may only be the user who transcribed the file. If this transcript derives word-for-word from a known written work in your database or public record, you can assume that work's author is the 'author'. If the transcript specifically mentions an author by name, use that value for 'author'. In all other cases simple return the value of 'user_provided_author' for 'author'.\n\n
            * GENERATE A LIST OF 'GENRES': The 'genre' should be a comma-seperated list of one or more values from this list: [ADVENTURE, ART, BIOGRAPHY, CHILDREN, COOKING, DRAMA, EDUCATION, FANTASY, FICTION, HISTORY, HORROR, HUMOR, MULTI_GENRE, MUSIC, MYSTERY, NON_FICTION, OTHER, PHILOSOPHY, POETRY, RELIGION, ROMANCE, SCIENCE, SCIENCE_FICTION, SELF_HELP, THRILLER, TRAVEL]. If the 'transcript' mentions a genre, use the closest value. If the 'transcript' is a known work, use the genre of that work. If the genre is unclear or not mentioned, use 'OTHER'.\n\n
            * SPLIT 'transcript' INTO COMPLETE CHAPTERS/SECTIONS IN ORDER, WITH 'TYPE': It's possible that the 'user_provided_title' or 'transcript' might reference one or more parts, sub-sections, or subdivisions of a book or manuscript. These sub-sections might be divisions of a written work like chapters or specific to the type of text like 'Act', 'Title Page', 'Table of Contents', 'Afterword', etc. Scan the transcript for words or phrases that denote or mark a transition from one chapter/section to another and split into a list of 'section' objects in JSON like so: `'section_type': <TYPE>, 'section_text': <TEXT OF THE SECTION>, 'section_number': <ORDINAL_RANK_OF_SECTION> for example 'Chapter 1'`. A 'section' object always has a 'section_type' is always one and only of the following: [ABOUT_THE_AUTHOR, ABSTRACT, ACKNOWLEDGEMENTS, ACT, AFTERWORD, ANNEXES, APPENDIX, BIBLIOGRAPHY, CAST_LIST, CHAPTER, CHARACTER_LIST, CONCLUSION, COPYRIGHT_PAGE, COVER, DEDICATION, DISCUSSION, EPILOGUE, EXECUTIVE_SUMMARY, FOREWORD, GLOSSARY, INDEX, INTRODUCTION, LITERATURE_REVIEW, METHODOLOGY, OTHER, PREFACE, PREFATORY_NOTE, PROLOGUE, REFERENCES, RESULTS, SCENE, STAGE_DIRECTIONS, TABLE_OF_CONTENTS, TITLE_PAGE.]. If the 'user_provided_title' or 'transcript' does not contain any chapter information, you can assume that the entire text is a single section object with type 'CHAPTER'. A response should always have at least one 'section' object/element in the lists of 'sections' No text from the 'transcript' should be omitted, every token/word/charecter from the 'transcript' should be present in exactly one 'section'. IMPORTANT!!! DO NOT OMIT ANY TEXT!!! DO NOT SUMMARIZE, SHORTEN, EDIT, OR TRUNCATE THE SECTION TEXT IN ANY WAY!!! PLEASE!!! \n\n
            Using the information I have provided please generate this JSON: 'manuscript_type', 'title', 'author', 'genre', 'summary', 'keywords', 'word_count', 'sections' and return in JSON format Make this JSON is fully escaped and fully safe to be parsed. It should comply with strict JSON format.
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
            try:
                self.summary = json.loads(
                    response.choices[0].message.content
                )
            except:
                self.summary = response.choices[0].message.content
            return self.summary
        else:
            raise Exception("Failed to summarize the transcription")

    @property
    def client(self):
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
