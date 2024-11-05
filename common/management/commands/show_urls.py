from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver

class Command(BaseCommand):
    help = "Displays all URLs in the project, including those from all apps"

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        self.print_urls(url_patterns)

    def print_urls(self, patterns, prefix=""):
        """
        Recursively prints URLs, handling nested patterns for all apps.
        """
        for pattern in patterns:
            # Check if the pattern is a URLResolver (a group of URLs)
            if isinstance(pattern, URLResolver):
                # Recursively print nested URL patterns
                self.print_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):  # Single URL pattern
                # Print full URL with the prefix path
                self.stdout.write(f"{prefix}{pattern.pattern}")
