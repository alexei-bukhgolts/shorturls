from django.db import models
from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator


class RedirectEntry(models.Model):
    """This model represents one redirection entry bound to user session using ForeignKey"""
    shortUrlValidator = RegexValidator(r"^[A-Za-z0-9_.\-~]+$",
                                       message="You must only use alphanumerical characters, underscores, and hyphens")

    created = models.DateTimeField(auto_now_add=True)
    shortUrl = models.CharField(unique=True, max_length=30, blank=False, validators=[shortUrlValidator])
    longUrl = models.URLField()
    sessionId = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, related_name="redirects")
    # It is unclear what to use in on_delete because different types of behavior can be expected

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['shortUrl'])
        ]
