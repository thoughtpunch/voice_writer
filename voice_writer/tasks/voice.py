from celery import shared_task
from django.apps import apps


@shared_task
def async_transcribe_voice_recording(instance_id):
    try:
        klass = apps.get_model('voice_writer', 'VoiceRecording')
        instance = klass.objects.get(id=instance_id)
        instance.transcribe()  # Call the synchronous transcribe method
    except klass.DoesNotExist:
        # Handle the case where the instance doesn't exist
        pass


@shared_task
def async_generate_cover_art(instance_id):
    try:
        klass = apps.get_model('voice_writer', 'VoiceRecording')
        instance = klass.objects.get(id=instance_id)
        instance.generate_cover_art()  # Call the synchronous dalle method
    except klass.DoesNotExist:
        # Handle the case where the instance doesn't exist
        pass