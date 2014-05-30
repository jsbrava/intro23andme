from django.conf.urls import patterns, url, include
from api.views import callback, logout, profiles, user, login

urlpatterns = patterns('', 
    url(r'^callback/$', callback),
    url(r'^logout/$', logout),
    url(r'^login/$', login, name="login"),
    url(r'^profiles/$', profiles),
    url(r'^user/$', user),
)