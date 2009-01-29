#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

import copy

from django.conf import settings

from util import feedparser

from models import *
from tagging.models import *
import plugins

# Patch feedparser so we can get access to interesting parts of media
# extentions.
feedparser._StrictFeedParser_old = feedparser._StrictFeedParser
class DlifeFeedParser(feedparser._StrictFeedParser_old):
  
  def _start_media_content(self, attrsD):
    self.entries[-1]['media_content_attrs'] = copy.deepcopy(attrsD)
feedparser._StrictFeedParser = DlifeFeedParser

def get_mod_class(plugin):
    # Converts 'lifestream.plugins.FeedPlugin' to
    # ['lifestream.plugins', 'FeedPlugin']
    try:
        dot = plugin.rindex('.')
    except ValueError:
        return plugin, ''
    return plugin[:dot], plugin[dot+1:]

def update_feeds():
  feeds = Feed.objects.get_fetchable_feeds()
  for feed in feeds:
    try:
      feed_items = feedparser.parse(feed.feed_url)
      
      # Get the required plugin
      if feed.feed_plugin:
        plugin_mod, plugin_class = get_mod_class(feed.feed_plugin)
        if plugin_class != '':
          feed_plugin = getattr(__import__(plugin_mod, {}, {}, ['']), plugin_class)(feed)
        else:
          # TODO: log warning.
          feed_plugin = plugins.FeedPlugin(feed)
      else:
        feed_plugin = plugins.FeedPlugin(feed)
      
      included_entries = []
      for entry in feed_items['entries']:
        
          feed_plugin.pre_process(entry)
          
          if feed_plugin.include_entry(entry):
            included_entries.append(entry)
            
      feed_plugin.process(included_entries)
      
      # Update tag counts
      for eachTag in Tag.objects.all():
        eachTag.tag_count = eachTag.item_set.all().count()
        eachTag.save()
    except:
      print "Error in feed: %s" % feed
      from traceback import print_exc
      print_exc()
