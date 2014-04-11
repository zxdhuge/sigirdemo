from django.conf.urls.defaults import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', index),
	(r'^more/$', more),
	(r'^ajax_get_one_blog/$', ajax_get_one_blog),
	(r'^slide/$', slide),
	(r'^clicked/$', clicked),

	(r'^search/$', search),

	(r'^test/$', test),
	(r'^(?P<path>.*)/$', 'django.views.static.serve', {'document_root': '/home/zxdhuge/django/sigirdemo/static/'}),
    # Examples:
    # url(r'^$', 'sigirdemo.views.home', name='home'),
    # url(r'^sigirdemo/', include('sigirdemo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
