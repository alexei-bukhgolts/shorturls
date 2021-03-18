from rest_framework import serializers

from url_shortener.models import RedirectEntry


class RedirectEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RedirectEntry
        fields = ['created', 'shortUrl', 'longUrl', 'sessionId']
