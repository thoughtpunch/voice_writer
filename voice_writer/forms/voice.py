from django import forms
from voice_writer.models.voice import VoiceRecording


class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['title', 'description', 'cover', 'audio_source', 'file']