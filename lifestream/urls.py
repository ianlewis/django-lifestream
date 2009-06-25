from django.conf.urls.defaults import *
from django.contrib import admin

from lifestream.rss import *

admin.autodiscover()

urlpatterns = patterns('lifestream.views',
    url(r'^$', 'main_page', name='main_page'),
    url(r'^items/view/(?P<item_id>\d+)$', 'item_page', name='item_page'),
    url(r'^items/tag/(?P<tag>.+)$', 'tag_page', name='tag_page'),
    url(r'^items/site/(?P<domain>.+)$', 'domain_page', name='domain_page'),
)

feeds = {
  'recent': RecentItemsFeed,
}

urlpatterns += patterns('',
  url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds }, name='lifestream_feeds'), 
)
