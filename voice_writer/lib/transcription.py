import whisper
from whisper.utils import get_writer
from typing import Optional


class VoiceTranscriber:
    def __init__(self, audio_file_path: str, user_upload_path: str):
        self.audio_file_path = audio_file_path
        self.transcription_file_path = None
        self.user_upload_path = user_upload_path
        self.transcription = None

    def transcribe(self, save_to_file: Optional[bool] = True):
        # Load the audio file from the VoiceRecording model
        model = whisper.load_model("base")
        result = model.transcribe(
            self.audio_file_path,
            word_timestamps=True,
            language="en",
            task="transcribe"
        )
        self.transcription = result

        # write to SRT file if asked
        if save_to_file:
            self.save_srt_file()

        return self

    def save_srt_file(self, options: Optional[dict] = {}):
        if self.transcription:
            # Save the transcription to a file
            vtt_writer = get_writer(
                output_format='srt',
                output_dir=self.user_upload_path
            )
            vtt_writer(
                result=self.transcription,  # type: ignore
                audio_path=self.audio_file_path,
                options=options
            )
            audio_file_path_without_ext = self.audio_file_path.split(".")[0]
            srt_file_path = f"{audio_file_path_without_ext}.srt"
            self.transcription_file_path = srt_file_path
            return srt_file_path
        else:
            raise Exception("Transcribe the audio file first")

