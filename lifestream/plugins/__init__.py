#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

import datetime
import dateutil.parser
import copy

from django.utils.http import urlquote
from django.db.models import Q

from util import clean_item_content
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
    date_published = (date_published - date_published.utcoffset()).replace(tzinfo=None)
    
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
      Q(item_date = entry['published']) | Q(item_permalink = entry['link'])
    ).filter(
      item_feed = self.feed
    ).count()
    
    return items_count == 0
    
  def process(self, entries):
    '''
    Process a list of entries and return a list of Item models. This
    hook could be overridden to create a single Item for a list of entries. For
    example a last.fm stream where you don't want to include all songs
    you listened to but rather a single item saying you listened to X number
    of songs.
    
    Items must be saved by this hook and tags must be updated.
    '''
    item_list = []
    for entry in entries:
      feed_contents = entry.get('content')
      if feed_contents is not None:
        content_type = feed_contents[0]['type']
        feed_content = feed_contents[0]['value']
        content, clean_content = clean_item_content(feed_content)
      else:
        content_type = None
        content = None
        clean_content = None
      
      i = Item(item_feed = self.feed,
               item_date = entry.get('published'),
               item_title = entry.get('title'),
               item_content = content,
               item_content_type = content_type,
               item_clean_content = clean_content,
               item_author = entry.get('author'),
               item_permalink = entry.get('link')
      )
      i.save()
      # Get tags
      tags = ()
      if 'tags' in entry:
        for tag in entry['tags']:
          tag_name = tag.get('term')[:30]
          Tag.objects.add_tag(i, tag_name)
      item_list.append(i)
    return item_list
