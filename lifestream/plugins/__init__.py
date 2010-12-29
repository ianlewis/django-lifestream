#:coding=utf-8:

import datetime
import dateutil.parser
import copy

from django.utils.encoding import iri_to_uri,force_unicode
from django.db.models import Q
from django.utils.html import strip_tags

from lifestream.models import *
from lifestream.util import convert_entities

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
        
        if 'link' in entry:
            protocol_index = entry['link'].find("://")
            if protocol_index != -1:
                entry['link'] = entry['link'][:protocol_index+3] + iri_to_uri(entry['link'][protocol_index+3:])
            else:
                entry['link'] = iri_to_uri(entry['link'])
    
    def include_entry(self, entry):
        '''
        Return true if this entry should be added to the lifestream. Normally
        this is a check for if the item has already been added or not.
        '''
        if "link" not in entry:
            return False
  
        #TODO: Use a more performance friendly way of finding out if
        #      the item has already been processed.Maybe use some sort
        #      of hashing algorithm?
        # Only fetch one record since it's faster.
        items_count = Item.objects.filter(
            Q(date = entry['published']) | Q(permalink = entry['link'])
        ).filter(
            feed = self.feed
        )[:1].count()
        
        return items_count == 0
      
    def process(self, entry):
        '''
        Process a single entry and return an item model.
        '''
    
        feed_contents = entry.get('content')
        feed_description = entry.get('description')
        if feed_contents:
            content_type = feed_contents[0]['type']
            content = force_unicode(feed_contents[0]['value'])
            clean_content = convert_entities(strip_tags(content))
        elif feed_description:
            content_type = "text/html"
            content = force_unicode(feed_description)
            clean_content = convert_entities(strip_tags(content))
        else:
            content_type = None
            content = None
            clean_content = None
    
        # Make sure the title is clean too.
        title = convert_entities(strip_tags(force_unicode(entry.get('title'))))
        
        media_url = None
        media_content_attrs = entry.get('media_content', [])
        for content in media_content_attrs:
            media_url = content.get('url')
            if media_url:
                break
    
        thumbnail_url = None
        media_thumbnail_attrs = entry.get('media_thumbnail', [])
        for thumbnail in media_thumbnail_attrs:
            thumbnail_url = thumbnail.get('url')
            if thumbnail_url:
                break
    
        media_description_type = None
        media_description_content = None
        media_description = entry.get('media_description')
        if media_description:
            media_description_type = media_description.get('type')

            media_description_content = media_description.get('content')
            if media_description_content:
                media_description_content = force_unicode(media_description_content)

        media_player_url = None
        media_player_attrs = entry.get('media_player')
        if media_player_attrs:
            media_player_url = media_player_attrs.get('url')
    
        item = Item(
            feed = self.feed,
            date = entry.get('published'),
            title = title,
            content = content,
            content_type = content_type,
            clean_content = clean_content,
            author = entry.get('author'),
            permalink = entry.get('link'),
            media_url = media_url,
            media_thumbnail_url = thumbnail_url,
            media_player_url = media_player_url,
            media_description = media_description_content,
            media_description_type = media_description_type,
        )
        return item
  
    def post_process(self, item):
        '''
        Allows plugins to process an item model before it is saved.
        '''
        pass 
