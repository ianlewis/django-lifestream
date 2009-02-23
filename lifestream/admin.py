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
  list_display    = ('title',)
  exclude         = ['user',]
  list_per_page   = 20
  
  model = Lifestream
  
  def save_model(self, request, obj, form, change):
    obj.user = request.user
    obj.save()
    if not change:
      # Create a new feed that is not editable
      # so that the user can use it when adding
      # items directly to the lifestream.
      basic_feed = Feed()
      basic_feed.lifestream = obj
      basic_feed.name = obj.title
      
      #Feed url is ignored
      basic_feed.url = "http://localhost"
      basic_feed.domain = "Local"
      basic_feed.fetchable = False
      basic_feed.basic_feed = True
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
    feed_url = cleaned_data.get('url')
    if not feed_url:
      # Feed url was not validated by the field validator
      return
    feed = feedparser.parse(feed_url)
    
    # Check if the feed was not parsed correctly.
    if feed['bozo']:
      self._errors['url'] = ErrorList(["This is not a valid feed: %s" % feed['bozo_exception']])
      print feed['bozo_exception']
      # This field is no longer valid. Remove from cleaned_data
      del cleaned_data['url']
      return
    # Check if the feed has a title field
    feed_info = feed.get('feed')
    if not feed_info.get('title'):
      self._errors['url'] = ErrorList(["This is not a valid feed: The feed is empty"])
      # This field is no longer valid. Remove from cleaned_data
      del cleaned_data['url']
      return
    cleaned_data['name'] = feed_info['title']
    cleaned_data['domain'] = get_url_domain(feed_url)
    return cleaned_data

class FeedAdmin(admin.ModelAdmin):
  exclude         = ['name', 'domain', 'basic_feed']
  list_display    = ('name', 'domain')
  list_filter     = ('domain',)
  
  form = FeedAdminForm
  
  model = Feed
  
  def queryset(self, request):
    return self.model.objects.get_feeds()

admin.site.register(Feed, FeedAdmin)

class ItemAdmin(admin.ModelAdmin):
  list_display    = ('title', 'date','published')
  exclude         = ['clean_content',]
  list_filter     = ('feed',)
  search_fields   = ('title','clean_content')
  list_per_page   = 20
  
  model = Item
  
  def save_model(self, request, obj, form, change):
    obj.item_content, obj.item_clean_content = clean_item_content(obj.item_content)
    obj.save()
    
admin.site.register(Item, ItemAdmin)
