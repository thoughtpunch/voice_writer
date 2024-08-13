from rest_framework import viewsets
from django.apps import apps
from .serializers import serializers_dict

models = apps.get_models()

viewsets_dict = {}

for model in models:
    viewset_class = type(
        f"{model.__name__}ViewSet",
        (viewsets.ModelViewSet,),
        {
            "queryset": model.objects.all(),
            "serializer_class": serializers_dict[model.__name__],
        }
    )
    viewsets_dict[model.__name__] = viewset_class

