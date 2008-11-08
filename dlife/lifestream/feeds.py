#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from dlife.util import stripper
from dlife.util import feedparser
from django.utils.http import urlquote
from django.db.models import Q

from models import *

import datetime
import dateutil.parser

def update_feeds():
  feeds = Feed.objects.filter(feed_deleted=False)
  for feed in feeds:
    try:
      feed_items = feedparser.parse(feed.feed_url)
      for entry in feed_items['entries']:
        
        # Get the date published
        date_published = entry.get('published', entry.get('updated'))
        if not date_published:
          date_published = str(datetime.datetime.utcnow())
        
        # urlquote messes up the protocol part of a url so if
        # don't mess with the protocol
        protocol_index = entry['link'][0:7].find("://")
        if protocol_index != -1:
          permalink = entry['link'][:protocol_index+3] + urlquote(entry['link'][protocol_index+3:])
        else:
          permalink = urlquote(entry['link'])
        
        # Parse to an actual datetime object
        date_published = dateutil.parser.parse(date_published)
        # Change the date to UTC and remove timezone info since MySQL doesn't
        # support it
        date_published = (date_published - date_published.utcoffset()).replace(tzinfo=None)
        
        # Find out if we have already imported this entry
        items_count = Item.objects.filter(
          Q(item_date = date_published) | Q(item_permalink = permalink)
        ).filter(
          item_feed = feed
        ).count()
        
        # Only save the item if no others matching it are found.
        if items_count == 0:
          
          # Get the content string value from feed item content
          feed_contents = entry.get('content')
          if feed_contents is not None:
            content_type = feed_contents[0]['type']
            feed_content = feed_contents[0]['value']
            content = stripper.strip_tags(feed_content)
            clean_content = stripper.strip_tags(feed_content, ())
          else:
            content = None
            clean_content = None
          
          i = Item(item_feed = feed,
                   item_date = date_published,
                   item_title = entry.get('title'),
                   item_content = content,
                   item_content_type = content_type,
                   item_clean_content = clean_content,
                   item_author = entry.get('author'),
                   item_permalink = permalink
                   )
          i.save()
          # Get tags
          tags = ()
          if 'tags' in entry:
            for tag in entry['tags']:
              tag_name = tag.get('term')[:30]
              slug = urlquote(tag_name.lower())
              try:
                tagobj = Tag.objects.get(tag_slug=slug)
                tagobj.tag_count += 1
              except Tag.DoesNotExist:
                #Add the tag object
                tagobj = Tag(tag_name = tag_name,
                             tag_slug = slug,
                             tag_count = 1)
              
              tagobj.save()
              i.item_tags.add(tagobj)
            
    except Exception, e:
      print e