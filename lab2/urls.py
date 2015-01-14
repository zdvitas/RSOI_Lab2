from django.conf.urls import patterns, url
from django.shortcuts import render
from lab2 import views
from lab2 import oauth

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^auth', oauth.auth, name='auth'),
    url(r'^token', oauth.access_token),
    url(r'^refresh_token', oauth.refresh_token),
    url(r'^info', views.info),   # Done
    url(r'^user/me', views.user_me),
    url(r'^user/(?P<id>\d+)/$', views.user_id),
    url(r'^user/(?P<id>\d+)/(?P<pc_id>\d+)/$', views.pc_soft_list),


)
