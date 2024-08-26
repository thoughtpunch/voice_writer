from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.urls import path
import datetime
from voice_writer.forms.voice import VoiceRecordingCollectionForm
from .models import (
    Author,
    User,
    VoiceRecording,
    VoiceRecordingCollection,
    VoiceTranscription,
    Manuscript,
    Section,
    Document
)


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 0  # Do not display any empty forms by default
    fields = ['title', 'slug', 'file', 'duration_ms', 'format', 'is_processed', 'collection']
    readonly_fields = ['duration_ms', 'file_size', 'format', 'is_processed']
    show_change_link = True  # Allows navigating to the full change form of each recording

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        if obj and hasattr(obj, 'user'):
            # Limit the collection queryset to collections associated with the current user
            formset.form.base_fields['collection'].queryset = VoiceRecordingCollection.objects.filter(user=obj.user)

        return formset


class VoiceTranscriptionInline(admin.TabularInline):
    model = VoiceTranscription
    extra = 0  # Number of empty forms to display by default
    exclude = ['file', 'metadata']
    fields = ['transcription','keywords', 'created_at']
    readonly_fields = ['keywords', 'metadata', 'created_at', 'created_at']


# VOICE RECORDING ADMIN
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'user',
        'duration_display',
        'file_size_display',
        'format',
        'is_processed',
        'created_at'
    )
    search_fields = ('title', 'description', 'user__username', 'format')
    list_filter = ('format', 'created_at', 'user', 'is_processed')
    readonly_fields = (
        'audio_player',
        'duration_display',
        'file_size_display',
        'file_url_display',
        'bitrate_kbps',
        'format',
        'is_processed',
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
                obj.file.url
            )
        return "No audio file"
    audio_player.short_description = 'Audio Player'
    audio_player.allow_tags = True

    def file_url_display(self, obj):
        # I'm not sure why this keeps including the whole base path
        # so I'm just going to hack it out for now
        return obj.file.url
    file_url_display.description = 'Full URL'

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
        if obj.duration_ms:
            # Display duration in a more readable format
            duration = datetime.timedelta(seconds=(obj.duration_ms / 1000))
            return duration
    duration_display.short_description = 'Duration'


class VoiceRecordingCollectionAdmin(admin.ModelAdmin):
    inlines = [VoiceRecordingInline]
    list_display = (
        'title',
        'slug',
        'description',
        'cover',
        'recording_count',
        'user',
        'created_at'
    )
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('title', 'slug', 'description', 'user', 'created_at')
    readonly_fields = (
        'created_at',
        'updated_at',
        'slug',
        'recording_count',
    )
    form = VoiceRecordingCollectionForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(self.add_view), name='voicerecordingcollection_add'),
        ]
        return custom_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            form = VoiceRecordingCollectionForm(request.POST, request.FILES)
            files = request.FILES.getlist('files')

            if form.is_valid():
                voice_recording_collection = form.save(user=request.user)
                for file in files:
                    VoiceRecording.objects.create(
                        collection=voice_recording_collection,
                        user=voice_recording_collection.user,
                        file=file
                    )
                    voice_recording_collection.recording_count += 1
                    voice_recording_collection.save()
                self.message_user(request, "Voice recordings have been uploaded successfully.")
                return redirect('admin:voice_writer_voicerecordingcollection_changelist')
        else:
            form = VoiceRecordingCollectionForm()

        context = {
            **self.admin_site.each_context(request),
            'form': form,
            'opts': self.model._meta,
            'form_url': form_url,
            'add': True,
            'change': False,
        }

        return render(request, 'admin/voicerecordingcollection_add_form.html', context)


# REGISTER ADMIN MODELS
admin.site.register(Author)
admin.site.register(User)
admin.site.register(VoiceRecordingCollection, VoiceRecordingCollectionAdmin)
admin.site.register(VoiceRecording, VoiceRecordingAdmin)
admin.site.register(VoiceTranscription)
admin.site.register(Manuscript)
admin.site.register(Section)
admin.site.register(Document)