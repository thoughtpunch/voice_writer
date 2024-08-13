import graphene
from .author import AuthorQuery
from .manuscript import ManuscriptQuery
from .section import SectionQuery
from .document import DocumentQuery
from .voice_recording import VoiceRecordingQuery
from .voice_transcription import VoiceTranscriptionQuery
from .user import UserQuery


class Query(
    AuthorQuery,
    DocumentQuery,
    SectionQuery,
    ManuscriptQuery,
    UserQuery,
    VoiceRecordingQuery,
    VoiceTranscriptionQuery,
    graphene.ObjectType
):
    pass