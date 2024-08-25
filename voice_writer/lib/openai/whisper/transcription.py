import os
from typing import Optional
from openai import OpenAI


class VoiceTranscriber:
    def __init__(self, audio_file_path: str, language: str):
        self.audio_file_path = audio_file_path
        self.language = language
        self.transcription = None
        self.srt_subtitles = ""

    def transcribe(self):
        # Transcribe the audio file using OpenAI Whisper API
        self._whisper_transcribe_audio()
        # Generate the SRT subtitles
        self._generate_srt()
        return self

    def _whisper_transcribe_audio(self) -> Optional[str]:
        with open(self.audio_file_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
                response_format="verbose_json"
            )
            self.transcription = response

    def _generate_srt(self) -> str:
        if self.transcription:
            for segment in self.transcription['segments']: # type: ignore
                start = segment['start']
                end = segment['end']
                text = segment['text']
                start_time = self._format_timecode(start)
                end_time = self._format_timecode(end)
                self.srt_subtitles += f"{start_time} --> {end_time}\n{text}\n\n"

            return self.srt_subtitles
        else:
            raise Exception("Transcribe the audio file first")

    @staticmethod
    def _format_timecode(seconds: float) -> str:
        """Helper method to convert seconds to SRT timecode format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

    @property
    def client(self):
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
