import whisper
from whisper.utils import get_writer
from typing import Optional

class VoiceTranscriber:
    def __init__(self, audio_file, upload_path):
        self.audio_file = audio_file
        self.upload_path = upload_path
        self.transcription = None
        self.provider = 'whisper'

    def transcribe(self):
        # Load the audio file from the VoiceRecording model
        audio_file_path = self.audio_file.path
        model = whisper.load_model("base")
        result = model.transcribe(
            audio_file_path,
            word_timestamps=True,
            language="en",
            task="transcribe"
        )
        self.transcription = result

        return self.transcription["text"]

    def save_srt_file(self, options: Optional[dict] = {}):
        # Save the transcription to a file
        vtt_writer = get_writer(
            output_format='srt',
            output_dir=self.upload_path
        )
        vtt_writer(
            result=self.transcription,  # type: ignore
            audio_path=self.audio_file.path,
            options=options
        )


