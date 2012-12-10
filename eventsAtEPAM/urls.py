from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from eventsAtEPAM import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.index, name='index'),
    url(r'^(?P<event_id>\d+)/$', views.detail, name='detail'),
    url(r'^create/$', views.create_event, name='create'),
    url(r'^edit/(?P<event_id>\d+)/$', views.edit_event, name='edit'),
    url(r'^export/(?P<event_id>\d+)/$', views.export_event, name='export'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/', redirect_to, {'url': '/'}),
    url(r'^admin/', include(admin.site.urls)),
    
)