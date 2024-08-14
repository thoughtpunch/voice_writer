# voice_writer/schema/voice_transcription.py
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from voice_writer.models import VoiceTranscription


class VoiceTranscriptionType(DjangoObjectType):
    class Meta:
        model = VoiceTranscription
        fields = "__all__"


class CreateVoiceTranscription(graphene.Mutation):
    class Arguments:
        recording_id = graphene.ID(required=True)
        provider = graphene.String(required=True)
        transcription = graphene.String(required=True)
        file = Upload(required=True)
        keywords = graphene.JSONString()
        metadata = graphene.JSONString()

    voice_transcription = graphene.Field(VoiceTranscriptionType)

    def mutate(self, info, recording_id, provider, transcription, file=None, keywords=None, metadata=None):
        voice_transcription = VoiceTranscription(
            recording_id=recording_id,
            provider=provider,
            transcription=transcription,
            file=file,
            keywords=keywords,
            metadata=metadata,
        )
        voice_transcription.save()
        return CreateVoiceTranscription(voice_transcription=voice_transcription)


class UpdateVoiceTranscription(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        provider = graphene.String()
        transcription = graphene.String()
        file = graphene.String()
        keywords = graphene.JSONString()
        metadata = graphene.JSONString()

    voice_transcription = graphene.Field(VoiceTranscriptionType)

    def mutate(self, info, id, provider=None, transcription=None, file=None, keywords=None, metadata=None):
        voice_transcription = VoiceTranscription.objects.get(pk=id)
        if provider:
            voice_transcription.provider = provider
        if transcription:
            voice_transcription.transcription = transcription
        if file:
            voice_transcription.file = file
        if keywords is not None:
            voice_transcription.keywords = keywords
        if metadata is not None:
            voice_transcription.metadata = metadata
        voice_transcription.save()
        return UpdateVoiceTranscription(voice_transcription=voice_transcription)


class DeleteVoiceTranscription(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        voice_transcription = VoiceTranscription.objects.get(pk=id)
        voice_transcription.delete()
        return DeleteVoiceTranscription(ok=True)


class VoiceTranscriptionQuery(graphene.ObjectType):
    all_voice_transcriptions = graphene.List(VoiceTranscriptionType)
    voice_transcription = graphene.Field(
        VoiceTranscriptionType,
        id=graphene.ID(required=True)
    )

    def resolve_all_voice_transcriptions(root, info):
        return VoiceTranscription.objects.all()

    def resolve_voice_transcription(self, info, id):
        return VoiceTranscription.objects.get(pk=id)


class VoiceTranscriptionMutation(graphene.ObjectType):
    create_voice_transcription = CreateVoiceTranscription.Field()
    update_voice_transcription = UpdateVoiceTranscription.Field()
    delete_voice_transcription = DeleteVoiceTranscription.Field()
