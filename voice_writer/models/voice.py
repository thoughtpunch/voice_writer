import os
import re
import tempfile
from django.core.files import File
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from voice_writer.lib.transcription import VoiceTranscriber
from voice_writer.lib.summarize import TranscriptionSummarizer
from voice_writer.utils.audio import extract_audio_metadata
from voice_writer.tasks.voice import async_transcribe_voice_recording


class VoiceRecording(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    bitrate = models.IntegerField(blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)
    file = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/voice",
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

            # 3. Summarize the transcription and update records
            voice_transcription.summarize()
        else:
            raise Exception("Transcription failed")

    def async_transcribe(self):
        async_transcribe_voice_recording.apply_async(
            args=[self.id],
            countdown=10
        )


class VoiceTranscription(models.Model):
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
        # 2. Async transcribe the recording
        instance.async_transcribe()
        # 3. Flag the recording as processed
        instance.is_processed = True
        instance.save()
