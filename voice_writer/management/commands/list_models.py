from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'List all models and their fields'

    def handle(self, *args, **kwargs):
        for model in apps.get_models():
            self.stdout.write(f"Model: {model.__name__}")
            for field in model._meta.get_fields():
                self.stdout.write(f"  - Field: {field.name} ({field.get_internal_type()})")
            self.stdout.write("\n")