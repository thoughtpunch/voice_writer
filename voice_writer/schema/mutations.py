import graphene
from .author import AuthorMutation
from .manuscript import ManuscriptMutation
from .section import SectionMutation
from .document import DocumentMutation
from .voice_recording import VoiceRecordingMutation
from .voice_transcription import VoiceTranscriptionMutation
from .user import UserMutation


class Mutation(
    AuthorMutation,
    DocumentMutation,
    SectionMutation,
    ManuscriptMutation,
    UserMutation,
    VoiceRecordingMutation,
    VoiceTranscriptionMutation,
    graphene.ObjectType
):
    pass