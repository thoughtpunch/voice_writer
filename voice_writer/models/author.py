from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from common.models import BaseModel


class Author(BaseModel):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
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
    portrait = models.FileField(
        upload_to=f"{settings.USER_UPLOADS_PATH}/images",
        blank=True,
        null=True
    )

    @property
    def name(self):
        name_segments = [
            self.first_name,
            self.middle_name,
            self.last_name
        ]
        return " ".join(name_segments)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(pre_save, sender=Author)
def pre_save_author(sender, instance, **kwargs):
    # Set slug if not set
    if instance.id and not instance.slug:
        first_octet = str(instance.id).split('-')[0]
        instance.slug = f"{slugify(instance.name).replace('-', '_')}_{first_octet}"