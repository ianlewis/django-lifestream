from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'dlife.lifestream.views.main_page'),
    (r'^page/(?P<page>\d+)$', 'dlife.lifestream.views.main_page'),
    (r'^item/(?P<item_id>\d+)$', 'dlife.lifestream.views.item_page'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
