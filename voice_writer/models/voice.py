import os
import re
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from voice_writer.lib.transcription import VoiceTranscriber
from voice_writer.lib.summarize import TranscriptionSummarizer
from voice_writer.utils.file import (
    async_move_uploads_to_user_upload_path,
    user_upload_path,
)
from voice_writer.utils.audio import extract_audio_metadata
from voice_writer.tasks.voice import async_transcribe_voice_recording


class VoiceRecordingStorage(FileSystemStorage):
    # Override the get_available_name method to prevent Django from
    #  appending a suffix to the file name. We don't need this
    #  as we are storing the files in a directory structure
    def get_available_name(self, name, max_length=None):
        return name


class VoiceRecording(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    bitrate = models.IntegerField(blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)
    file = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/unprocessed/voice",
        storage=VoiceRecordingStorage(),
        blank=True
    )
    is_processed = models.BooleanField(default=False)
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Voice Recording"

    @property
    def relative_local_path(self):
        return self.file.path.replace(str(settings.BASE_DIR), '')

    def transcribe(self):
        # transcribe the audio recording use OpenAI whisper
        transcription = VoiceTranscriber(
            audio_file_path=self.file.path,
            user_upload_path=user_upload_path(self, full_path=True)
        ).transcribe()

        # Create and save a VoiceTranscription model
        voice_transcription = VoiceTranscription(
            recording=self,
            file=transcription.transcription_file_path,
            transcription=transcription.transcription['text'],
            metadata=transcription.transcription
        )
        voice_transcription.save()
        # Summarize the transcription and update records
        voice_transcription.summarize()

    def async_transcribe(self):
        async_transcribe_voice_recording.apply_async(
            args=[self.id],
            countdown=5
        )


class VoiceTranscription(models.Model):
    recording = models.ForeignKey(
        VoiceRecording,
        on_delete=models.CASCADE,
        related_name='transcriptions'
    )
    provider = models.CharField(max_length=255, default='whisper')
    transcription = models.TextField(blank=True, null=True)
    file = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/unprocessed/transcripts",
        blank=True
    )
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.recording.title:
            return f"{self.recording.title} - Transcription for Recording#{self.recording.id}"
        else:
            return "Transcription"

    @property
    def user(self):
        return self.recording.user

    @property
    def relative_local_path(self):
        return self.file.path.replace(str(settings.BASE_DIR), '')

    def summarize(self):
        if self.transcription and self.user:
            # Use the filename as the title if it's not set
            if self.recording.title:
                summary_title = self.recording.title
            else:
                summary_title = os.path.basename(
                    self.recording.file.name
                ).split('.')[0]
            cleaned_summary_title = re.sub(r'\W+', ' ', summary_title).strip()
            # Summarize the transcription with OpenAI
            summarizer = TranscriptionSummarizer(
                author=f"{self.user.first_name} {self.user.last_name}",
                title=cleaned_summary_title.lower(),
                transcription=self.transcription
            )
            summary = summarizer.summarize()
            # Set local attributes from AI summarization
            if not self.keywords:
                self.keywords = summary.get('keywords')
            if not self.metadata:
                self.metadata = summary
            self.save()
            # Set related attributes from AI summarization
            if not self.recording.keywords:
                self.recording.keywords = summary.get('keywords')
            if not self.recording.title:
                self.recording.title = summary.get('title')
            if not self.recording.description:
                self.recording.description = summary.get('summary')
            self.recording.save()
        return summary


@receiver(post_save, sender=VoiceRecording)
def post_save_signal_handler(sender, instance, created, **kwargs):
    if created:
        # 1. Extract audio metadata
        extract_audio_metadata(instance)
        # 2. Async move the file to it's user upload path
        async_move_uploads_to_user_upload_path(
            instance.__class__.__name__,
            instance.id
        )
        # 3. Async transcribe the recording
        instance.async_transcribe()
        # 4. Flag the recording as processed
        instance.is_processed = True
        instance.save()
