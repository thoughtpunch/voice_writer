from django.urls import path
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from voice_writer.schema import schema
from voice_writer.views import load_summary, index

urlpatterns = []

# HTMX
urlpatterns += [
    path('', index, name='index'),
    path('load-summary/', load_summary, name='load_summary'),
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