from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
import datetime

from .models import (
    Author,
    User,
    VoiceRecording,
    VoiceTranscription,
    Manuscript,
    Section,
    Document
)


class VoiceTranscriptionInline(admin.TabularInline):
    model = VoiceTranscription
    extra = 0  # Number of empty forms to display by default
    exclude = ['file']
    fields = ['transcription','keywords', 'metadata', 'created_at']
    readonly_fields = ['keywords', 'metadata', 'created_at', 'created_at']


# VOICE RECORDING ADMIN
class VoiceRecordingAdmin(admin.ModelAdmin):
    exclude = ('file_size', 'duration', 'bitrate', 'original_filename')
    list_display = (
        'title',
        'description',
        'audio_player',
        'user',
        'file_url_display',
        'duration_display',
        'file_size_display',
        'format',
        'created_at'
    )
    search_fields = ('title', 'description', 'user__username', 'format')
    list_filter = ('format', 'created_at', 'user')
    readonly_fields = (
        'audio_player',
        'duration_display',
        'file_size_display',
        'file_url_display',
        'bitrate',
        'format',
        'created_at',
        'updated_at'
    )
    inlines = [VoiceTranscriptionInline]

    def audio_player(self, obj):
        # I'm not sure why this keeps including the whole base path
        # so I'm just going to hack it out for now
        if obj.file:
            return format_html(
                '<audio controls>'
                '<source src="{}" type="audio/mpeg">'
                'Your browser does not support the audio element.'
                '</audio>',
                obj.relative_local_path
            )
        return "No audio file"

    def file_url_display(self, obj):
        # I'm not sure why this keeps including the whole base path
        # so I'm just going to hack it out for now
        return obj.relative_local_path
    file_url_display.description = 'Download'

    def file_size_display(self, obj):
        # Display file size in a more readable format
        if obj.file_size:
            size = obj.file_size
            for unit in ['bytes', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.2f} {unit}"
                size /= 1024
            return f"{size:.2f} TB"
    file_size_display.short_description = 'File Size'

    def duration_display(self, obj):
        if obj.duration:
            # Display duration in a more readable format
            duration = datetime.timedelta(seconds=obj.duration)
            return duration
    duration_display.short_description = 'Duration'

    audio_player.short_description = 'Audio Player'
    audio_player.allow_tags = True


# REGISTER ADMIN MODELS
admin.site.register(Author)
admin.site.register(User)
admin.site.register(VoiceRecording, VoiceRecordingAdmin)
admin.site.register(VoiceTranscription)
admin.site.register(Manuscript)
admin.site.register(Section)
admin.site.register(Document)