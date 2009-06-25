#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

import datetime
import dateutil.parser
import copy

from django.utils.http import urlquote
from django.db.models import Q

from lifestream.util import clean_item_content
from lifestream.models import *
from tagging.models import *

class FeedPlugin(object):
  
  feed = None
  
  def __init__(self, feed):
    self.feed = feed
  
  def name(self):
    return "Generic Feed"
  
  def pre_process(self, entry):
    '''
    A hook is used to clean up feed entry data before it is processed.
    This hook can be used to clean up dates and/or media data
    before being processed.
    '''
    date_published = entry.get('published', entry.get('updated'))
    if not date_published:
      date_published = str(datetime.datetime.utcnow())
    date_published = dateutil.parser.parse(date_published)
    # Change the date to UTC and remove timezone info since MySQL doesn't
    # support it.
    utcoffset = date_published.utcoffset()
    if utcoffset:
        date_published = date_published - utcoffset 
    date_published = date_published.replace(tzinfo=None)
    
    entry['published'] = date_published
    
    protocol_index = entry['link'].find("://")
    if protocol_index != -1:
      entry['link'] = entry['link'][:protocol_index+3] + urlquote(entry['link'][protocol_index+3:])
    else:
      entry['link'] = urlquote(entry['link'])
  
  def include_entry(self, entry):
    '''
    Return true if this entry should be added to the lifestream. Normally
    this is a check for if the item has already been added or not.
    '''
    items_count = Item.objects.filter(
      Q(date = entry['published']) | Q(permalink = entry['link'])
    ).filter(
      feed = self.feed
    ).count()
    
    return items_count == 0
    
  def process(self, entry):
    '''
    Process a single entry and return an item model.
    '''

    feed_contents = entry.get('content')
    feed_description = entry.get('description')
    if feed_contents:
        content_type = feed_contents[0]['type']
        feed_content = feed_contents[0]['value']
        content, clean_content = clean_item_content(feed_content)
    elif feed_description:
        content_type = "text/html"
        content, clean_content = clean_item_content(feed_description)
    else:
      content_type = None
      content = None
      clean_content = None
    
    media_url = None
    media_content_attrs = entry.get('media_content_attrs')
    if media_content_attrs:
      media_url = media_content_attrs.get('url')

    thumbnail_url = None
    media_thumbnail_attrs = entry.get('media_thumbnail_attrs')
    if media_thumbnail_attrs:
      thumbnail_url = media_thumbnail_attrs.get('url')

    media_description_type = None
    media_description_attrs = entry.get('media_description_attrs')
    if media_description_attrs:
      media_description_type = media_description_attrs.get('type')
    media_player_url = None
    media_player_attrs = entry.get('media_player_attrs')
    if media_player_attrs:
      media_player_url = media_player_attrs.get('url')

    item = Item(feed = self.feed,
             date = entry.get('published'),
             title = entry.get('title'),
             content = content,
             content_type = content_type,
             clean_content = clean_content,
             author = entry.get('author'),
             permalink = entry.get('link'),
             media_url = media_url,
             media_thumbnail_url = thumbnail_url,
             media_player_url = media_player_url,
             media_description = entry.get("media_description"),
             media_description_type = media_description_type,
    )
    return item

  def post_process(self, item):
    '''
    Allows plugins to process an item model before it is saved.
    '''
    return item
