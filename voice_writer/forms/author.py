from django import forms
from voice_writer.models.author import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'  # Or list the specific fields you want to include
        exclude = ['user']  # Exclude the user field since it's set in the view