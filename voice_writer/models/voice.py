import os
import re
import requests
from celery import chain
from typing import Optional
from common.models import BaseModel
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from lib.languages import LanguageChoices
from voice_writer.lib.openai.whisper.transcription import VoiceTranscriber
from voice_writer.lib.openai.dalle.generate_cover_art import CoverArtGenerator
from voice_writer.lib.openai.chatgpt.summarize_transcript import (
    TranscriptionSummarizer
)
from voice_writer.utils.audio import extract_audio_metadata_from_file
from voice_writer.tasks.voice import (
    async_transcribe_voice_recording,
    async_generate_cover_art
)


class AudioSource(models.TextChoices):
    APP = 'app', 'App'
    UPLOAD = 'upload', 'Upload'
    API = 'api', 'API'


class VoiceRecordingCollection(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cover = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/voice_collection_cover_art",
        blank=True
    )
    recording_count = models.PositiveBigIntegerField(default=0)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VoiceRecording(BaseModel):
    collection = models.ForeignKey(
        VoiceRecordingCollection,
        related_name='recordings',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.ENGLISH,
    )
    cover = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/voice_cover_art",
        blank=True
    )
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
        upload_to=f"{settings.USER_UPLOADS_PATH}/voice"
    )
    is_processed = models.BooleanField(default=False)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    segment_count = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.title:
            return str(self.title)
        else:
            return "Voice Recording"

    def transcribe(self):
        if not self.is_processed:
            # 1. transcribe the audio recording use OpenAI whisper
            transcription = VoiceTranscriber(
                audio_file_url=self.file.url,
                audio_file_format=self.format.lower(),
                language=self.language,
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
        else:
            raise Exception("Recording already processed")

    def generate_cover_art(self):
        if self.is_processed:
            # Generate cover art for the recording
            audio_metadata = self.metadata['audio']
            audio_metadata['description'] = self.description
            audio_metadata['keywords'] = self.keywords
            cover_art = CoverArtGenerator(
                audio_metadata=audio_metadata
            ).generate_cover_art()
            if cover_art and cover_art.generated_cover_url:
                # Stream the content from the URL without downloading
                image_name = f"{self.title}_cover.png"
                image_url = cover_art.generated_cover_url
                # Get content from URL
                with requests.get(image_url, stream=True) as r:
                    r.raise_for_status()
                    content = ContentFile(r.content)
                    # Save the content directly to the FileField
                    self.cover.save(image_name, content, save=True)
        else:
            raise Exception("Transcribe the recording before generating cover art")


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
        if self.recording and self.recording.title:
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

            # Write data back up to the parent VoiceRecording model
            # - Set Keywords if not set
            if summary.get('keywords') and (overwrite_values or not self.recording.keywords):
                self.recording.keywords = summary.get('keywords')

            # - Set Title and Slug if not set
            if summary.get('title') and (overwrite_values or not self.recording.title):
                self.recording.title = summary.get('title')
                first_octet = str(self.recording.id).split('-')[0]
                self.recording.slug = f"{slugify(self.recording.title).replace('-', '_')}_{first_octet}"

            # - Set Description if not set
            if summary.get('summary') and (overwrite_values or not self.recording.description):
                self.recording.description = summary.get('summary')

            # Save the parent VoiceRecording model
            self.recording.save()

            return summary
        else:
            raise Exception("Transcription not available or user not set")


@receiver(pre_save, sender=VoiceRecordingCollection)
def pre_save_voice_recording_collection(sender, instance, **kwargs):
    # Set slug if not set
    if instance.id and instance.title and not instance.slug:
        first_octet = str(instance.id).split('-')[0]
        instance.slug = f"{slugify(instance.title).replace('-', '_')}_{first_octet}"


@receiver(pre_save, sender=VoiceRecording)
def pre_save_voice_recording(sender, instance, **kwargs):
    # Extract audio metadata from Mutagen
    if instance.file and not instance.is_processed:
        audio_meta_data = extract_audio_metadata_from_file(instance.file)
        for key, value in audio_meta_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        if not instance.metadata:
            instance.metadata = {}
        instance.metadata['audio'] = audio_meta_data


@receiver(post_save, sender=VoiceRecording)
def post_save_voice_recording(sender, instance, created, **kwargs):
    # On creation, async transcribe the recording, then generate cover art
    if created and instance.file:
        chain(
            async_transcribe_voice_recording.si(instance.id),
            async_generate_cover_art.si(instance.id)
        ).apply_async()
