from django.conf.urls.defaults import *
from django.contrib import admin

from lifestream.rss import *

admin.autodiscover()

urlpatterns = patterns('lifestream.views',
    url(r'^$', 'main_page', name='main_page'),
    url(r'^page/(?P<page>\d+)$', 'main_page', name='main_page_paged'),
    url(r'^item/(?P<item_id>\d+)$', 'item_page', name='item_page'),
)

feeds = {
  'recent': RecentItemsFeed,
}

urlpatterns += patterns('',
  url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds }, name='lifestream_feeds'), 
)
