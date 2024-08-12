import os
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from voice_writer.utils.file import (
    async_move_uploads_to_user_upload_path
)

class Author(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Basic Information
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    pen_name = models.CharField(max_length=50, blank=True, null=True)
    pronouns = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    show_date_of_birth = models.BooleanField(default=False)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    # Biographical Information
    biography = models.TextField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)

    # Literary Career
    notable_works = models.TextField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    influences = models.TextField(blank=True, null=True)

    # Portrait/Avatar
    portrait = models.ImageField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/unprocessed/images",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=Author)
def post_save_signal_handler(sender, instance, created, **kwargs):
    if created:
        async_move_uploads_to_user_upload_path(
            instance.__class__.__name__,
            instance.id
        )
