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
        duration_ms = graphene.Float()
        bitrate = graphene.Int()
        file_size = graphene.Int()
        format = graphene.String()
        file = Upload(required=True)
        keywords = graphene.JSONString()
        metadata = graphene.JSONString()

    voice_recording = graphene.Field(VoiceRecordingType)

    def mutate(self, info, user_id, title, description=None, duration_ms=None, bitrate=None, file_size=None, format=None, file=None, keywords=None, metadata=None):
        voice_recording = VoiceRecording(
            title=title,
            description=description,
            duration_ms=duration_ms,
            bitrate=bitrate,
            file_size=file_size,
            format=format,
            file=file,
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
        duration_ms = graphene.Float()
        bitrate = graphene.Int()
        file_size = graphene.Int()
        format = graphene.String()
        file = graphene.String()
        keywords = graphene.JSONString()
        metadata = graphene.JSONString()

    voice_recording = graphene.Field(VoiceRecordingType)

    def mutate(self, info, id, title=None, description=None, duration_ms=None, bitrate=None, file_size=None, format=None, file=None, keywords=None, metadata=None):
        voice_recording = VoiceRecording.objects.get(pk=id)
        if title:
            voice_recording.title = title
        if description:
            voice_recording.description = description
        if duration_ms is not None:
            voice_recording.duration_ms = duration_ms
        if bitrate is not None:
            voice_recording.bitrate = bitrate
        if file_size is not None:
            voice_recording.file_size = file_size
        if format:
            voice_recording.format = format
        if file:
            voice_recording.file = file
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
    voice_recording = graphene.Field(
        VoiceRecordingType,
        id=graphene.ID(required=True)
    )

    def resolve_all_voice_recordings(root, info):
        return VoiceRecording.objects.all()

    def resolve_voice_recording(self, info, id):
        return VoiceRecording.objects.get(pk=id)


class VoiceRecordingMutation(graphene.ObjectType):
    create_voice_recording = CreateVoiceRecording.Field()
    update_voice_recording = UpdateVoiceRecording.Field()
    delete_voice_recording = DeleteVoiceRecording.Field()
