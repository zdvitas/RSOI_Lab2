from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^', include('Lab1.urls')),
    url(r'^', include('lab2.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
