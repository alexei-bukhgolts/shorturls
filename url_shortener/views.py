from django.views.generic.base import RedirectView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from url_shortener.models import RedirectEntry
from url_shortener.serializers import RedirectEntrySerializer


class RedirectEntriesView(generics.mixins.CreateModelMixin, generics.mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = RedirectEntrySerializer

    def get_queryset(self):
        return self.request.session.create_model_instance(None).redirects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        session = self.request.session.create_model_instance(None)
        print(self.request.session.create_model_instance(None))
        serializer.save(sessionId=session)

    def post(self, request, *args, **kwargs):
        # must save session here, otherwise it won't be save to db and foreign key constrain will fail
        if not request.session.session_key:
            request.session.save()
        return self.create(request, *args, **kwargs)


class CommitRedirectView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        query_set = RedirectEntry.objects.all()
        target_url = query_set.get(shortUrl=self.kwargs["subpart"])
        return target_url.longUrl
