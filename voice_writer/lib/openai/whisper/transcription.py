import os
import whisper
import tempfile
from whisper.utils import get_writer
from typing import Optional


class VoiceTranscriber:
    def __init__(self, audio_file_path: str):
        self.audio_file_path = audio_file_path
        self.transcription = None
        self.srt_subtitles = None

    def transcribe(self):
        # Load the audio file from the VoiceRecording model
        self._whisper_transcribe_audio()
        # Generate the SRT subtitles
        self._generate_srt()
        return self

    def _whisper_transcribe_audio(self) -> Optional[str]:
        model = whisper.load_model("medium")
        result = model.transcribe(
            self.audio_file_path,
            word_timestamps=True,
            language="en",
            task="transcribe"
        )
        self.transcription = result

    def _generate_srt(self) -> str:
        if self.transcription:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Instantiate the writer with the temporary directory
                vtt_writer = get_writer(
                    output_format='srt',
                    output_dir=temp_dir
                )
                # Write the result to the temporary directory
                vtt_writer(
                    result=self.transcription,  # type: ignore
                    audio_path=self.audio_file_path
                )
                # Construct the expected file path
                audio_file_name_without_ext = os.path.splitext(os.path.basename(self.audio_file_path))[0]
                srt_file_name = f"{audio_file_name_without_ext}.srt"

                # Read the SRT file and store it in the instance
                with open(os.path.join(temp_dir, srt_file_name), 'r', encoding='utf-8') as file:
                    self.srt_subtitles = file.read()

                return self.srt_subtitles
        else:
            raise Exception("Transcribe the audio file first")

