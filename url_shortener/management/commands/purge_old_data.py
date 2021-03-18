# https://stackoverflow.com/questions/41162313/auto-delete-data-which-is-older-than-10-days-in-django
from django.core.management.base import BaseCommand
from url_shortener.models import RedirectEntry
from datetime import datetime, timedelta

from url_shortener.settings import ENTRY_DB_TTL_DAYS


class Command(BaseCommand):
    help = 'Delete old redirect entries'

    def handle(self, *args, **options):
        RedirectEntry.objects.filter(created__lte=datetime.now()-timedelta(days=ENTRY_DB_TTL_DAYS)).delete()
        self.stdout.write(f'Deleted objects older than {ENTRY_DB_TTL_DAYS} days')
