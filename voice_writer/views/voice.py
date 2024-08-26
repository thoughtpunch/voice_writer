from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from voice_writer.models.voice import (
    VoiceRecording,
    VoiceRecordingCollection,
)
from voice_writer.forms.voice import (
    VoiceRecordingForm,
    VoiceRecordingCollectionForm,
)


@login_required
def upload_voice_recordings(request):
    if request.method == 'POST':
        form = VoiceRecordingCollectionForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')

        if form.is_valid():
            voice_recording_collection = form.save(user=request.user)
            for file in files:
                VoiceRecording.objects.create(collection=voice_recording_collection, file=file)
            return redirect('collection_detail', pk=voice_recording_collection.pk)  # Redirect to a success page

    else:
        form = VoiceRecordingCollectionForm()

    return render(request, 'upload_voice_recordings.html', {'form': form})


@login_required
def create_voice_recording(request):
    pass
    if request.method == 'POST':
        pass
        # form = VoiceRecordingForm(request.POST, request.FILES)
        # if form.is_valid():
        #     voice_recording = form.save(commit=False)
        #     voice_recording.user = request.user
        #     voice_recording.save()
        #     return redirect('voice_recording_list')
    else:
        pass
        # form = VoiceRecordingForm()
    return render(request, 'voice_writer/voice/new.html', {'form': form})


@login_required
def edit_voice_recording(request, id):
    # Fetch the VoiceRecording object for the given ID and logged-in user
    recording = get_object_or_404(VoiceRecording, id=id, user=request.user)

    if request.method == 'POST':
        # Handle form submission
        form = VoiceRecordingForm(request.POST, request.FILES, instance=recording)
        if form.is_valid():
            form.save()
            return redirect('voice_recording_list')  # Redirect to the recordings list after saving
    else:
        # Display the form for editing
        form = VoiceRecordingForm(instance=recording)

    return render(request, 'voice_writer/voice/edit.html', {
        'form': form,
        'recording': recording
    })


@login_required
def voice_recording_list(request):
    recordings = VoiceRecording.objects.filter(user=request.user)
    return render(request, 'voice_writer/voice/list.html', {'recordings': recordings})

