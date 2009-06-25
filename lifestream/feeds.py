#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

import copy
import logging

from django.conf import settings

from util import feedparser
from models import *
from tagging.models import *
import plugins
import re

# MonkeyPatch feedparser so we can get access to interesting parts of media
# extentions.
feedparser._StrictFeedParser_old = feedparser._StrictFeedParser
class DlifeFeedParser(feedparser._StrictFeedParser_old):
  def _start_media_content(self, attrsD):
    self.entries[-1]['media_content_attrs'] = copy.deepcopy(attrsD)
  def _start_media_thumbnail(self, attrsD):
    self.entries[-1]['media_thumbnail_attrs'] = copy.deepcopy(attrsD)
  def _start_media_description(self, attrsD):
    self.push('media_description', 1)
    self.entries[-1]['media_description_attrs'] = copy.deepcopy(attrsD)
  def _start_media_player(self, attrsD):
    self.entries[-1]['media_player_attrs'] = copy.deepcopy(attrsD)
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
  feeds = Feed.objects.fetchable()
  for feed in feeds:
    try:
      feed_items = feedparser.parse(feed.url)
      
      # Get the required plugin
      if feed.plugin_class_name:
        plugin_mod, plugin_class = get_mod_class(feed.plugin_class_name)
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
            
      for entry in included_entries:
        i = feed_plugin.process(entry)

        feed_plugin.post_process(i) 

        i.save()
        # Get tags
        tags = ()
        if 'tags' in entry:
          for tag in entry['tags']:
            tag_name = tag.get('term')[:30]
            Tag.objects.add_tag(i, re.sub(r"[ ,]+", "_", tag_name))
    except:
      #TODO: Make this work with standard python logging
      print "Error in feed: %s" % feed
      from traceback import print_exc
      print_exc()
