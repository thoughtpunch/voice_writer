from django.urls import path
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from voice_writer.schema import schema
from voice_writer.views.base import index
from voice_writer.views.voice import (
    create_voice_recording,
    voice_recording_list,
    edit_voice_recording,
)
from voice_writer.views.author import author_profile, update_author

# HTML
urlpatterns = [
    path('', index, name='index'),
    path('recordings/', voice_recording_list, name='voice_recording_list'),
    path('recordings/edit/<uuid:id>/', edit_voice_recording, name='edit_voice_recording'),
    path('recordings/new/', create_voice_recording, name='create_voice_recording'),
    path('author/', author_profile, name='author_profile'),
    path('author/', update_author, name='update_author'),
]


# GRAPHENE GRAPHQL
urlpatterns += [
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                graphiql=True,
                schema=schema
            )
        )
    ),
]

# GRAPHENE FILE UPLOAD
urlpatterns += [
    path(
        "graphql/",
        FileUploadGraphQLView.as_view(
            graphiql=True,
            schema=schema
        )
    ),
]