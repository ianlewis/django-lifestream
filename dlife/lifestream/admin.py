#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
from django.contrib.contenttypes import generic
from django.contrib.comments.models import *

from dlife.lifestream.models import *
from dlife.util import feedparser
from dlife.util import get_url_domain

admin.site.register(Lifestream)

class FeedAdminForm(forms.ModelForm):
  class Meta:
    model = Feed
  
  def clean(self):
    """
    Checks to make sure a feed url is valid and gets the feed title
    and domain.
    """
    cleaned_data = self.cleaned_data
    feed_url = cleaned_data.get('feed_url')
    if not feed_url:
      # Feed url was not validated by the field validator
      return
    feed = feedparser.parse(feed_url)
    
    # Check if the feed was not parsed correctly.
    if feed['bozo']:
      self._errors['feed_url'] = ErrorList(["This is not a valid feed: %s" % feed['bozo_exception']])
      # This field is no longer valid. Remove from cleaned_data
      del cleaned_data['feed_url']
      return
    # Check if the feed has a title field
    feed_info = feed.get('feed')
    if not feed_info.get('title'):
      self._errors['feed_url'] = ErrorList(["This is not a valid feed: The feed is empty"])
      # This field is no longer valid. Remove from cleaned_data
      del cleaned_data['feed_url']
      return
    cleaned_data['feed_name'] = feed_info['title']
    cleaned_data['feed_domain'] = get_url_domain(feed_url)
    return cleaned_data

class FeedAdmin(admin.ModelAdmin):
  exclude         = ['feed_name', 'feed_domain']
  list_display    = ('feed_name', 'feed_domain')
  list_filter     = ('feed_domain',)
  
  form = FeedAdminForm

admin.site.register(Feed, FeedAdmin)

# class CommentAdmin(admin.ModelAdmin):
#   list_display    = ('comment_item', 'comment_name')
#   exclude         = ['comment_item',]
#   list_filter     = ('comment_user',)
#   search_fields   = ('comment_name','comment_content')
#   list_per_page   = 20

# admin.site.register(Comment, CommentAdmin)

# class CommentInline(admin.StackedInline):
#   model           = Comment
#   max_num         = 1   #TODO: Fix this
#   exclude         = ['comment_item','content_type','object_id']

class ItemAdmin(admin.ModelAdmin):
  list_display    = ('item_title', 'item_date')
  exclude         = ['item_clean_content',]
  list_filter     = ('item_feed',)
  search_fields   = ('item_title','item_clean_content')
  list_per_page   = 20
  
  # inlines         = [CommentInline,]

admin.site.register(Item, ItemAdmin)

class TagAdmin(admin.ModelAdmin):
  list_display   = ('tag_name', 'tag_count')
  ordering       = ('-tag_count',)
  search_fields  = ('tag_name',)
  list_per_page   = 20

admin.site.register(Tag, TagAdmin)