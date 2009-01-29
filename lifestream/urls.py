from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('lifestream.views',
    url(r'^$', 'main_page', name='main_page'),
    url(r'^page/(?P<page>\d+)$', 'main_page', name='main_page_paged'),
    url(r'^item/(?P<item_id>\d+)$', 'item_page', name='item_page'),
)
