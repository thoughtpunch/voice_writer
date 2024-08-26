from typing import List, Any
from django.utils.datastructures import MultiValueDict
from django import forms
from django.core.exceptions import ValidationError
from voice_writer.models.voice import (
    VoiceRecordingCollection,
    VoiceRecording,
)


class MultiFileField(forms.FileField):
    def to_python(self, data: Any) -> List[Any]:
        # Convert incoming data to a list
        if not data:
            return []
        if isinstance(data, list):
            return data
        return [data]

    def validate(self, data: List[Any]) -> None:
        """Check that the list contains valid files."""
        super().validate(data)
        for item in data:
            if not hasattr(item, 'content_type'):
                raise ValidationError('Invalid file.')

    def clean(self, data: Any, initial: Any = None) -> List[Any]:
        cleaned_data = super().clean(data, initial)
        if isinstance(cleaned_data, MultiValueDict):
            cleaned_data = cleaned_data.getlist(self.name)
        return cleaned_data


class VoiceRecordingCollectionForm(forms.ModelForm):
    files = MultiFileField()

    class Meta:
        model = VoiceRecordingCollection
        fields = ['title']

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
