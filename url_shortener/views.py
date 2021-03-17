from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def get_my_redirects(request):
    """The main page of application"""
    return Response({"message": "Hello, world!"})