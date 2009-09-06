#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

import copy
import re
import logging

from django.conf import settings

from util import sanitize_html
from models import *
import plugins
import types

import feedparser

logger = logging.getLogger('django-lifestream')
def write(self, s):
    self.error(s)
logger.write = types.MethodType(write, logger, logger.__class__)

# MonkeyPatch feedparser so we can get access to interesting parts of media
# extentions.
feedparser._StrictFeedParser_old = feedparser._StrictFeedParser
class LifestreamFeedParser(feedparser._StrictFeedParser_old):
  def _start_media_content(self, attrsD):
    self.entries[-1]['media_content_attrs'] = copy.deepcopy(attrsD)
  def _start_media_thumbnail(self, attrsD):
    self.entries[-1]['media_thumbnail_attrs'] = copy.deepcopy(attrsD)
  def _start_media_description(self, attrsD):
    self.push('media_description', 1)
    self.entries[-1]['media_description_attrs'] = copy.deepcopy(attrsD)
  def _start_media_player(self, attrsD):
    self.entries[-1]['media_player_attrs'] = copy.deepcopy(attrsD)
feedparser._StrictFeedParser = LifestreamFeedParser

# Change out feedparser's html sanitizer for our own based
# on BeautifulSoup and our own tag/attribute stripper.
feedparser._sanitizeHTML = sanitize_html

def get_mod_class(plugin):
    """
    Converts 'lifestream.plugins.FeedPlugin' to
    ['lifestream.plugins', 'FeedPlugin']
    """
    try:
        dot = plugin.rindex('.')
    except ValueError:
        return plugin, ''
    return plugin[:dot], plugin[dot+1:]

try:
    from feedcache import Cache
    from util import CacheStorage
    # TODO: Use a cache storage object.
    feed_cache = Cache(CacheStorage())
    def parse_feed(url):
        """
        Parses a feed. Uses feedcache if it is available
        using django's cache framework as storage for
        feedcache.
        """
        return feed_cache.fetch(url)
except ImportError:
    # Fall back to using feedparser
    def parse_feed(url):
        return feedparser.parse(url)

def update_feeds():
    feeds = Feed.objects.fetchable()
    for feed in feeds:
        try:
            feed_items = parse_feed(feed.url)
            
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
                try:
                    feed_plugin.pre_process(entry)
                    
                    if feed_plugin.include_entry(entry):
                      included_entries.append(entry)
                except:
                    from traceback import print_exc
                    logger.error(u"Error importing item from feed '%s'" % feed.url)
                    print_exc(file=logger)
                    
            for entry in included_entries:
                try:
                    i = feed_plugin.process(entry)

                    feed_plugin.post_process(i) 

                    i.save()
                    
                    # Get tags
                    if 'tagging' in settings.INSTALLED_APPS:
                        from tagging.models import Tag
                        tags = ()
                        if 'tags' in entry:
                          for tag in entry['tags']:
                            tag_name = tag.get('term')[:30]
                            Tag.objects.add_tag(i, re.sub(r"[ ,]+", "_", tag_name))
                except:
                    from traceback import print_exc
                    logger.error(u"Error importing item from feed '%s'" % feed.url)
                    print_exc(file=logger)
                 
        except:
            from traceback import print_exc
            logger.error(u"Error importing feed: %s" % feed)  
            print_exc(file=logger)
