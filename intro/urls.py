from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView    

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'intro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^$', TemplateView.as_view(template_name="home/home.html")),   #placed at root http://stackoverflow.com/questions/15117835/django-1-5-index-page
    url(r'^admin/', include(admin.site.urls)),
    url(r'^23api/', include('api.urls', '23api')),
    url(r'^results$', 'members.views.results', name='results'),
    url(r'^send_intro', 'members.views.send_intro', name='send_intro'),
    url(r'^home', 'home.views.home', name='home'),
    url(r'^relatives', 'members.views.relatives', name='relatives'),
)
