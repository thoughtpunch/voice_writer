import os
import re
import shutil
import unicodedata
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from mutagen import File as MutagenFile

VOICE_FILE_DIR = 'user_uploads/voice_files'
VOICE_FILE_BASE_PATH = os.path.join(settings.MEDIA_ROOT, VOICE_FILE_DIR)


class VoiceRecordingStorage(FileSystemStorage):
    # Override the get_available_name method to prevent Django from
    #  appending a suffix to the file name. We don't need this
    #  as we are storing the files in a directory structure
    def get_available_name(self, name, max_length=None):
        return name


class VoiceRecording(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    bitrate = models.IntegerField(blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)
    file = models.FileField(
        upload_to='unprocessed/voice_recordings',
        storage=VoiceRecordingStorage(),
        blank=True
    )
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class VoiceTranscription(models.Model):
    recording = models.ForeignKey(VoiceRecording, on_delete=models.CASCADE)
    provider = models.CharField(max_length=255, default='whisper')
    file = models.FileField(
        upload_to='unprocessed/voice_transcriptions',
        blank=True
    )
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transcription for {self.recording.title} by {self.provider.name}"

    @property
    def user(self):
        return self.recording.user


# Return a unified path for both the audio recording and the transcription
def upload_path(instance) -> str:
    if instance.user:
        user_id = instance.user.id
        if isinstance(instance, VoiceRecording):
            recording_id = instance.id
        else:
            recording_id = instance.recording.id

        path_segments = [
            VOICE_FILE_BASE_PATH,
            f'user_{user_id}',
            f'recording_{recording_id}',
        ]
        return os.path.join(*path_segments)
    else:
        raise ValueError("User must be set before saving the instance")


# Extract audio metadata using the Mutagen library
def extract_audio_metadata(instance):
    if hasattr(instance, 'duration'):
        audio = MutagenFile(instance.file)
        if audio and audio.info:
            instance.duration = audio.info.length
            instance.bitrate = audio.info.bitrate // 1000  # Convert to kbps
            instance.file_size = instance.file.size
            instance.format = instance.file.name.split('.')[-1].upper()
            instance.save()


# Sanitize the file name to remove any special characters and
#  ensure can be slugified for use in URLs
def sanitize_filename(filename):
    # Normalize the text to remove accents and diacritics
    text = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase
    text = text.lower()
    # Replace any non-alphanumeric character with a hyphen
    text = re.sub(r'[^a-z0-9]+', '_', text)
    # Strip leading and trailing hyphens
    text = text.strip('-')
    return text


# Move both the original audio recording and the transcription
#  to the same directory as we want to keep them together
def move_file_to_upload_path(instance):
    if instance.file:
        if instance.file.path.startswith(VOICE_FILE_BASE_PATH):
            return instance.file.path
        else:
            # Define the original and new paths
            old_path = instance.file.path
            # Sanitize the name and prep to store in new path
            base_name = os.path.basename(instance.file.path)
            file_name, ext = os.path.splitext(base_name)
            sanitized_filename = f"{sanitize_filename(file_name)}{ext}"
            new_dir = os.path.join(VOICE_FILE_BASE_PATH, upload_path(instance))
            new_path = os.path.join(new_dir, sanitized_filename)

            # Create the new directory if it doesn't exist
            os.makedirs(new_dir, exist_ok=True)

            # Move the file
            shutil.move(old_path, new_path)

            # Update the file path in the model instance
            instance.file.name = new_path
            instance.original_filename = base_name
            instance.save()
    return instance


@receiver(post_save, sender=VoiceRecording)
@receiver(post_save, sender=VoiceTranscription)
def post_save_signal_handler(sender, instance, **kwargs):
    move_file_to_upload_path(instance)
    extract_audio_metadata(instance)

