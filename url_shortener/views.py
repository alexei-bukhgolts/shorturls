from django.views.generic.base import RedirectView
from django.core.cache import cache
from django.http import HttpResponseNotFound
from rest_framework import generics

from url_shortener.models import RedirectEntry
from url_shortener.serializers import RedirectEntrySerializer


class RedirectEntriesView(generics.mixins.CreateModelMixin, generics.mixins.ListModelMixin, generics.GenericAPIView):
    """API view which allows the user to GET their redirects and POST new redirect"""
    serializer_class = RedirectEntrySerializer

    def get_queryset(self):
        """All redirects related to the current session"""
        return self.request.session.create_model_instance(None).redirects.all()

    def get(self, request, *args, **kwargs):
        """GET all redirects belonging to the user's session"""
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Method that saves RedirectEntry to the db. Overridden to save session id in addition to form data"""
        session = self.request.session.create_model_instance(None)
        serializer.save(sessionId=session)

    def post(self, request, *args, **kwargs):
        """Add new RedirectionEntry using this method"""
        # must save session here, otherwise it won't be save to db and foreign key constrain will fail
        if not request.session.session_key:
            request.session.save()
        return self.create(request, *args, **kwargs)


class CommitRedirectView(RedirectView):
    """View whose only purpose is to redirect the user to target url"""
    permanent = False
    query_string = False

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        print(url)
        if url is None:
            # Unknown subpart
            return HttpResponseNotFound("404 NOT FOUND")
        return super(CommitRedirectView, self).get(request, *args, **kwargs)
        # This calls get_redirect_url() again but it is cached so it should not matter too much

    def get_redirect_url(self, *args, **kwargs):
        """Gets full url for redirection using cached db"""
        subpart = self.kwargs["subpart"]
        target_url = cache.get(subpart)
        if target_url is not None:
            # Cached URL found
            return target_url
        query_set = RedirectEntry.objects.all()
        redirect_entry = query_set.filter(shortUrl=subpart).first()
        # query_set.get() raises an exception and first() returns None which is more concise
        target_url = redirect_entry.longUrl if redirect_entry else None
        if target_url is not None:
            cache.set(subpart, target_url)
        return target_url

