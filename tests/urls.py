# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin

from django_busybody.urls import urlpatterns as django_busybody_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include((django_busybody_urls, 'django_busybody'), namespace='django_busybody')),
]
