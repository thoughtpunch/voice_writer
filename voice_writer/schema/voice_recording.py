import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from voice_writer.models import VoiceRecording


class VoiceRecordingType(DjangoObjectType):
    class Meta:
        model = VoiceRecording
        fields = "__all__"


class CreateVoiceRecording(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        duration = graphene.Float()
        bitrate = graphene.Int()
        file_size = graphene.Int()
        format = graphene.String()
        file = Upload(required=True)
        original_filename = graphene.String()
        keywords = graphene.JSONString()
        metadata = graphene.JSONString()

    voice_recording = graphene.Field(VoiceRecordingType)

    def mutate(self, info, user_id, title, description=None, duration=None, bitrate=None, file_size=None, format=None, file=None, original_filename=None, keywords=None, metadata=None):
        voice_recording = VoiceRecording(
            title=title,
            description=description,
            duration=duration,
            bitrate=bitrate,
            file_size=file_size,
            format=format,
            file=file,
            original_filename=original_filename,
            keywords=keywords,
            metadata=metadata,
            user_id=user_id,
        )
        voice_recording.save()
        return CreateVoiceRecording(voice_recording=voice_recording)


class UpdateVoiceRecording(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        duration = graphene.Float()
        bitrate = graphene.Int()
        file_size = graphene.Int()
        format = graphene.String()
        file = graphene.String()
        original_filename = graphene.String()
        keywords = graphene.JSONString()
        metadata = graphene.JSONString()

    voice_recording = graphene.Field(VoiceRecordingType)

    def mutate(self, info, id, title=None, description=None, duration=None, bitrate=None, file_size=None, format=None, file=None, original_filename=None, keywords=None, metadata=None):
        voice_recording = VoiceRecording.objects.get(pk=id)
        if title:
            voice_recording.title = title
        if description:
            voice_recording.description = description
        if duration is not None:
            voice_recording.duration = duration
        if bitrate is not None:
            voice_recording.bitrate = bitrate
        if file_size is not None:
            voice_recording.file_size = file_size
        if format:
            voice_recording.format = format
        if file:
            voice_recording.file = file
        if original_filename:
            voice_recording.original_filename = original_filename
        if keywords is not None:
            voice_recording.keywords = keywords
        if metadata is not None:
            voice_recording.metadata = metadata
        voice_recording.save()
        return UpdateVoiceRecording(voice_recording=voice_recording)


class DeleteVoiceRecording(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        voice_recording = VoiceRecording.objects.get(pk=id)
        voice_recording.delete()
        return DeleteVoiceRecording(ok=True)


class VoiceRecordingQuery(graphene.ObjectType):
    all_voice_recordings = graphene.List(VoiceRecordingType)

    def resolve_all_voice_recordings(root, info):
        return VoiceRecording.objects.all()


class VoiceRecordingMutation(graphene.ObjectType):
    create_voice_recording = CreateVoiceRecording.Field()
    update_voice_recording = UpdateVoiceRecording.Field()
    delete_voice_recording = DeleteVoiceRecording.Field()
