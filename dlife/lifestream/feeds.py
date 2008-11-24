#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings

from dlife.util import feedparser

from models import *
from plugins import FeedPlugin

# Patch feedparser so we can get access to interesting parts of media
# extentions.
feedparser._StrictFeedParser_old = feedparser._StrictFeedParser
class DlifeFeedParser(feedparser._StrictFeedParser_old):
  
  def _start_media_content(self, attrsD):
    self.entries[-1]['media_content_attrs'] = copy.deepcopy(attrsD)
feedparser._StrictFeedParser = DlifeFeedParser

def update_feeds():
  feeds = Feed.objects.get_fetchable_feeds()
  for feed in feeds:
    try:
      feed_items = feedparser.parse(feed.feed_url)
      
      if feed.feed_plugin_name:
        feed_plugin = settings.PLUGINS_DICT[self.feed_plugin_name](feed)
      else:
        feed_plugin = FeedPlugin(feed)
      
      included_entries = []
      for entry in feed_items['entries']:
        
          feed_plugin.pre_process(entry)
          
          if feed_plugin.include_entry(entry):
            included_entries.append(entry)
            
      feed_plugin.process(included_entries)
        
    except:
      from traceback import print_exc
      print_exc()
