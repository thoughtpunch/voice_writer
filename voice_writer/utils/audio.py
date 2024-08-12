from mutagen import File as MutagenFile


# Extract audio metadata using the Mutagen library
def extract_audio_metadata(instance):
    if hasattr(instance, 'duration') and not instance.duration:
        audio = MutagenFile(instance.file)
        if audio and audio.info:
            instance.duration = audio.info.length
            instance.bitrate = audio.info.bitrate // 1000  # Convert to kbps
            instance.file_size = instance.file.size
            instance.format = instance.file.name.split('.')[-1].upper()
            instance.save()