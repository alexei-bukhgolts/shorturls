"""url_shortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.static import serve

from url_shortener.views import RedirectEntriesView, CommitRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/my_redirects', RedirectEntriesView.as_view()),
    path('<str:subpart>', CommitRedirectView.as_view())
]

if settings.DEBUG:
    #  We serve the main page of our app here. It should be done using nginx in production.
    urlpatterns += [
        path('', serve, {'document_root': settings.STATIC_ROOT, 'path': 'index.html'}),
    ]
