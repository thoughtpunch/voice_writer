from multiupload.fields import MultiMediaField
from django import forms
from voice_writer.models.voice import (
    VoiceRecordingCollection,
    VoiceRecording,
)


class VoiceRecordingCollectionForm(forms.ModelForm):
    files = MultiMediaField(min_num=1, media_type='audio')

    class Meta:
        model = VoiceRecordingCollection
        fields = ['user', 'title']

    def save(self, user, commit=True):
        voice_recording_collection = super().save(commit=False)
        voice_recording_collection.user = user
        if commit:
            voice_recording_collection.save()
        return voice_recording_collection


class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['file']
