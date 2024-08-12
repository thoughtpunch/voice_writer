import os
import re
import shutil
import unicodedata
from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.db.models.fields.files import FileField
from typing import Optional


def get_file_fields(instance) -> list:
    file_fields = []
    for field in instance._meta.get_fields():
        if isinstance(field, FileField):
            file_fields.append(field.name)
    return file_fields


# Return a unified path for both the audio recording and the transcription
def user_upload_path(instance, full_path: Optional[bool]=False) -> str:
    if instance.user:
        class_name_lowercase = instance.__class__.__name__.lower()
        if full_path:
            base_path = settings.USER_UPLOADS_ROOT
        else:
            base_path = settings.USER_UPLOADS_PATH
        path_segments = [
            base_path,
            f"{instance.user.id}",
            class_name_lowercase,
            f"{instance.id}",
        ]
        return os.path.join(*path_segments)
    else:
        raise ValueError("Instance must have a user")


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
def move_uploads_to_user_upload_path(instance):
    for file_field in get_file_fields(instance):
        file = getattr(instance, file_field)
        if file:
            unprocessed_file_path = f"{settings.USER_UPLOADS_ROOT}/unprocessed"
            if file.path.startswith(unprocessed_file_path):
                # Define the original and new paths
                old_path = file.path
                # Sanitize the name and prep to store in new path
                base_name = os.path.basename(file.path)
                file_name, ext = os.path.splitext(base_name)
                sanitized_filename = f"{sanitize_filename(file_name)}{ext}"
                new_dir = os.path.join(
                    settings.MEDIA_ROOT,
                    user_upload_path(instance)
                )
                new_path = os.path.join(new_dir, sanitized_filename)

                # Create the new directory if it doesn't exist
                os.makedirs(new_dir, exist_ok=True)

                # Move the file
                shutil.move(old_path, new_path)

                # Update the file path in the model instance
                setattr(instance, file_field, new_path)

                # Save the original filename if needed
                if hasattr(instance, 'original_filename'):
                    instance.original_filename = base_name

                instance.save()
            else:
                return file.path
    return instance


@shared_task
def async_move_uploads_to_user_upload_path(instance_class, instance_id):
    klass = apps.get_model('voice_writer', instance_class)
    instance = klass.objects.get(id=instance_id)
    move_uploads_to_user_upload_path(instance)
