from typing import Optional

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from common.models import BaseModel
from lib.languages import LanguageChoices
# from voice_writer.lib.openai.chatgpt.summarize_transcript import \
#     TranscriptionSummarizer
# from voice_writer.lib.openai.dalle.generate_cover_art import CoverArtGenerator
# from voice_writer.lib.openai.whisper.transcription import VoiceTranscriber
from voice_writer.utils.audio import extract_audio_metadata_from_file

# Path Functions


def collection_cover_upload_path(instance, filename):
    """Uploads to 'uploads/{USER_ID}/voice/collection_{COLLECTION_ID}/'"""
    return f"uploads/user_{instance.user.id}/voice/collection_{instance.id}/{filename}"


def recording_audio_upload_path(instance, filename):
    """Uploads to 'uploads/{USER_ID}/voice/collection_{COLLECTION_ID}/recording_{RECORDING_ID}/'"""
    collection_id = instance.collection.id
    return f"uploads/user_{instance.user.id}/voice/collection_{collection_id}/recording_{instance.id}/{filename}"


def segment_audio_upload_path(instance, filename):
    """Uploads to the parent recording's directory"""
    recording = instance.recording
    collection_id = recording.collection.id
    return f"uploads/user_{recording.user.id}/voice/collection_{collection_id}/recording_{recording.id}/{filename}"


# Models

class AudioSource(models.TextChoices):
    APP = 'app', 'App'
    UPLOAD = 'upload', 'Upload'
    API = 'api', 'API'


class VoiceRecordingCollection(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover = models.FileField(upload_to=collection_cover_upload_path, blank=True, max_length=255)
    recording_count = models.PositiveBigIntegerField(default=0)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VoiceRecording(BaseModel):
    collection = models.ForeignKey(
        VoiceRecordingCollection,
        related_name='recordings',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.ENGLISH,
        blank=True,
        null=True
    )
    cover = models.FileField(
        upload_to=recording_audio_upload_path,
        max_length=255,
        blank=True,
        null=True
        )
    audio_source = models.CharField(
        max_length=10,
        choices=AudioSource.choices,
        default=AudioSource.APP,
        blank=True,
        null=True
    )
    duration_ms = models.BigIntegerField(
        default=0,
        blank=True,
        null=True
    )
    bitrate_kbps = models.IntegerField(default=0)
    file_size = models.PositiveIntegerField(default=0)
    format = models.CharField(max_length=10)
    file = models.FileField(upload_to=recording_audio_upload_path, max_length=255)
    is_processed = models.BooleanField(default=False)
    keywords = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    segment_count = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure a collection exists before saving the recording
        if not self.collection:
            # Create and assign a new collection for this recording
            self.collection = VoiceRecordingCollection.objects.create(
                user=self.user,
                title=self.title or "Untitled Collection",
                description=self.description or "No description"
            )
            # Save the collection immediately to ensure it's available
            self.collection.save()

        # Proceed with saving the VoiceRecording as usual
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title) if self.title else "Voice Recording"

    def transcribe(self):
        # Transcription logic here...
        pass

    def generate_cover_art(self):
        # Cover art generation logic here...
        pass


class VoiceSegment(BaseModel):
    recording = models.ForeignKey(
        VoiceRecording,
        related_name='segments',
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to=segment_audio_upload_path, max_length=255)
    cover = models.FileField(upload_to=segment_audio_upload_path, blank=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.ENGLISH,
    )
    duration_ms = models.BigIntegerField(blank=True, null=True)
    start_time_ms = models.BigIntegerField(blank=True, null=True)
    end_time_ms = models.BigIntegerField(blank=True, null=True)
    order = models.PositiveIntegerField()  # Order of the segment
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']  # Ensure segments are retrieved in order

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
        return f"{self.recording.title} Transcription" if self.recording.title else "Transcription"

    @property
    def user(self):
        return self.recording.user

    def summarize(self, overwrite_values: Optional[bool] = True):
        # Summarization logic here...
        pass


# Signal Handlers
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