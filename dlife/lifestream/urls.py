from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'dlife.lifestream.views.main_page'),
    (r'^page/(?P<page>\d+)$', 'dlife.lifestream.views.main_page'),
    url(r'^item/(?P<item_id>\d+)$', 'dlife.lifestream.views.item_page', name='item_page'),
)
