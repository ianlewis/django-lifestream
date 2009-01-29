#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.contrib import admin
from django import forms
from django.forms.util import ErrorList
from django.contrib.contenttypes import generic

from lifestream.models import *
from lifestream.util import feedparser
from lifestream.util import get_url_domain
from lifestream.util import clean_item_content

class LifestreamAdmin(admin.ModelAdmin):
  list_display    = ('ls_title',)
  exclude         = ['ls_user',]
  list_per_page   = 20
  
  model = Lifestream
  
  def save_model(self, request, obj, form, change):
    obj.ls_user = request.user
    obj.save()
    if not change:
      # Create a new feed that is not editable
      # so that the user can use it when adding
      # items directly to the lifestream.
      basic_feed = Feed()
      basic_feed.feed_lifestream = obj
      basic_feed.feed_name = obj.ls_title
      
      #This is ignored
      basic_feed.feed_url = "http://localhost"
      basic_feed.feed_domain = "Local"
      basic_feed.feed_fetchable = False
      basic_feed.feed_basic_feed = True
      basic_feed.save()

admin.site.register(Lifestream, LifestreamAdmin)

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
      print feed['bozo_exception']
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
  exclude         = ['feed_name', 'feed_domain', 'feed_basic_feed']
  list_display    = ('feed_name', 'feed_domain')
  list_filter     = ('feed_domain',)
  
  form = FeedAdminForm
  
  model = Feed
  
  def queryset(self, request):
    return self.model.objects.get_feeds()

admin.site.register(Feed, FeedAdmin)

class ItemAdmin(admin.ModelAdmin):
  list_display    = ('item_title', 'item_date','item_published')
  exclude         = ['item_clean_content',]
  list_filter     = ('item_feed',)
  search_fields   = ('item_title','item_clean_content')
  list_per_page   = 20
  
  model = Item
  
  def save_model(self, request, obj, form, change):
    obj.item_content, obj.item_clean_content = clean_item_content(obj.item_content)
    obj.save()
    
admin.site.register(Item, ItemAdmin)
