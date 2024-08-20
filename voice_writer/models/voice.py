import os
import re
from typing import Optional
from common.models import BaseModel
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from voice_writer.lib.openai.whisper.transcription import VoiceTranscriber
from voice_writer.lib.openai.chatgpt.summarize_transcript import (
    TranscriptionSummarizer
)
from voice_writer.utils.audio import extract_audio_metadata_from_file
from voice_writer.tasks.voice import async_transcribe_voice_recording


class AudioSource(models.TextChoices):
    APP = 'app', 'App'
    UPLOAD = 'upload', 'Upload'
    API = 'api', 'API'


class VoiceRecording(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    audio_source = models.CharField(
        max_length=10,
        choices=AudioSource.choices,
        default=AudioSource.APP,
    )
    duration_ms = models.BigIntegerField(default=0)
    recorded_at = models.DateTimeField(default=timezone.now)
    bitrate_kbps = models.IntegerField(default=0)
    file_size = models.PositiveIntegerField(default=0)
    format = models.CharField(max_length=10)
    file = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/voice",
        blank=True
    )
    is_processed = models.BooleanField(default=False)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    segment_count = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Voice Recording"

    def transcribe(self):
        # 1. transcribe the audio recording use OpenAI whisper
        transcription = VoiceTranscriber(
            audio_file_path=self.file.url
        ).transcribe()

        # 2. Create and save a VoiceTranscription model
        if transcription and transcription.transcription:
            srt_content = transcription.srt_subtitles
            voice_transcription = VoiceTranscription(
                recording=self,
                transcription=transcription.transcription['text'],
                srt_subtitles=srt_content,
                metadata=transcription.transcription
            )
            voice_transcription.save()
            # Change something

            # 3. Summarize the transcription and update records
            voice_transcription.summarize(overwrite_values=True)

            # 4. Update the VoiceRecording model
            self.is_processed = True
            self.save()
        else:
            raise Exception("Transcription failed")

    def async_transcribe(self):
        async_transcribe_voice_recording.apply_async(args=[self.id])


class VoiceSegment(BaseModel):
    recording = models.ForeignKey(
        VoiceRecording,
        related_name='segments',
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/voice_segments"
    )
    duration_ms = models.BigIntegerField(blank=True, null=True)
    start_time_ms = models.BigIntegerField(blank=True, null=True)
    end_time_ms = models.BigIntegerField(blank=True, null=True)
    order = models.PositiveIntegerField()  # Order of the segment
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']  # Ensure the segments are retrieved in order

    def __str__(self):
        return f"{self.recording.title} - Segment {self.order}"


class VoiceTranscription(BaseModel):
    recording = models.ForeignKey(
        VoiceRecording,
        on_delete=models.CASCADE,
        related_name='transcriptions'
    )
    provider = models.CharField(max_length=255, default='whisper')
    transcription = models.TextField(blank=True, null=True)
    srt_subtitles = models.TextField(blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.recording.title:
            return f"{self.recording.title}"
        else:
            return "Transcription"

    @property
    def user(self):
        return self.recording.user

    def summarize(self, overwrite_values: Optional[bool] = True):
        if self.transcription and self.user:
            # Use the filename as the title if it's not set
            summary_title = (
                self.recording.title
                if self.recording.title
                else os.path.basename(self.recording.file.name).split('.')[0]
            )
            cleaned_summary_title = re.sub(r'\W+', ' ', summary_title).strip().lower()

            # Summarize the transcription with OpenAI
            summarizer = TranscriptionSummarizer(
                author=f"{self.user.first_name} {self.user.last_name}",
                title=cleaned_summary_title,
                transcription=self.transcription
            )
            summary = summarizer.summarize()

            # Set local attributes, considering the overwrite flag
            self.keywords = summary.get('keywords') if overwrite_values or not self.keywords else self.keywords
            self.metadata = summary if overwrite_values or not self.metadata else self.metadata
            self.save()

            # Set related attributes, considering the overwrite flag
            self.recording.keywords = summary.get('keywords') if overwrite_values or not self.recording.keywords else self.recording.keywords
            self.recording.title = summary.get('title') if overwrite_values or not self.recording.title else self.recording.title
            self.recording.description = summary.get('summary') if overwrite_values or not self.recording.description else self.recording.description
            self.recording.save()

            return summary
        else:
            raise Exception("Transcription not available or user not set")


@receiver(pre_save, sender=VoiceRecording)
def pre_save_voice_recording(sender, instance, **kwargs):
    # Extract audio metadata
    audio_meta_data = extract_audio_metadata_from_file(instance.file)
    for key, value in audio_meta_data.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
    if not instance.metadata:
        instance.metadata = {}
    instance.metadata['audio'] = audio_meta_data


@receiver(post_save, sender=VoiceRecording)
def post_save_voice_recording(sender, instance, created, **kwargs):
    if created:
        # Async transcribe the recording
        instance.async_transcribe()
