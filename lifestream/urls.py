#:coding=utf-8:

from django.conf.urls.defaults import *
from django.contrib import admin

from lifestream.rss import *

admin.autodiscover()

urlpatterns = patterns('lifestream.views',
    url(r'^(?P<lifestream_slug>[-\w]+)/$', 'main_page', name='lifestream_main_page'),
    url(r'^(?P<lifestream_slug>[-\w]+)/items/view/(?P<item_id>\d+)/$', 'item_page', name='lifestream_item_page'),
    url(r'^(?P<lifestream_slug>[-\w]+)/items/site/(?P<domain>.+)/$', 'domain_page', name='lifestream_domain_page'),
)

feeds = {
    'recent': RecentItemsFeed,
}

urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds }, name='lifestream_feeds'), 
)
