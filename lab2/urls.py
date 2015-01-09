from django.conf.urls import patterns, url

from lab2 import views
from lab2 import oauth

urlpatterns = patterns('',
    # url(r'^$', views.home, name='home'),
    url(r'^auth', oauth.auth, name='auth'),
    # url(r'^get_content', views.get_content, name='content'),

)
