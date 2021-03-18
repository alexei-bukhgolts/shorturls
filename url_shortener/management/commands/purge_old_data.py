# https://stackoverflow.com/questions/41162313/auto-delete-data-which-is-older-than-10-days-in-django
from django.core.management.base import BaseCommand
from url_shortener.models import RedirectEntry
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Delete old redirect entries'

    def handle(self, *args, **options):
        RedirectEntry.objects.filter(created__lte=datetime.now()-timedelta(days=10)).delete()
        self.stdout.write('Deleted objects older than 10 days')