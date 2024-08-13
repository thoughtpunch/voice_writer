
# serializers.py
from rest_framework import serializers
from django.apps import apps

# Get all models from your app
models = apps.get_models()

# Dynamically create serializers for all models
serializers_dict = {}

for model in models:
    class Meta:
        model = model
        fields = '__all__'

    serializer_class = type(f"{model.__name__}Serializer", (serializers.ModelSerializer,), {"Meta": Meta})
    serializers_dict[model.__name__] = serializer_class