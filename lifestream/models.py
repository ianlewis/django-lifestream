#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink as model_permalink
from django.utils.translation import ugettext_lazy as _

import tagging

class Lifestream(models.Model):
  '''A lifestream itself.'''
  title = models.CharField(_("Title"), max_length=128)
  tagline = models.TextField(_("Tagline"), null=True, blank=True)
  
  baseurl = models.CharField(_("Base Url"), max_length=1000)
  
  items_per_page = models.IntegerField(_("Items Per Page"), default=10)
  
  user = models.ForeignKey(User)
  
  def __unicode__(self):
    return self.title
  
  class Meta:
    db_table="lifestream"

class FeedManager(models.Manager):
  ''' Query only normal feeds. '''
  
  def get_feeds(self):
    return super(FeedManager, self) \
           .get_query_set().filter(basic_feed=False)
  
  def get_fetchable_feeds(self):
    return self.get_feeds().filter(fetchable=True)

class Feed(models.Model):
  '''A feed for gathering data.'''
  lifestream = models.ForeignKey(Lifestream,verbose_name=_("Lifestream"))
  
  name = models.CharField(_("Feed Name"), max_length=255)
  url = models.URLField(_("Feed Url"), help_text=_("Must be a valid url"), verify_exists=True, max_length=1000)
  domain = models.CharField(_("Feed Domain"), max_length=255)
  fetchable = models.BooleanField(_("Fetchable"), default=True)
  
  # Used for feeds that allow users to directly add to the lifestream.
  basic_feed = models.BooleanField(default=False)
  
  # The feed plugin name used to process the incoming feed data.
  plugin_class_name = models.CharField(_("Plugin Name"), max_length=255, null=True, blank=True, choices=settings.PLUGINS)
  
  objects = FeedManager()
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    db_table="feeds"

class ItemManager(models.Manager):
  """Manager for querying Items"""

  def published(self):
    return self.filter(published=True).order_by("-date")

class Item(models.Model):
  '''A feed item'''
  feed = models.ForeignKey(Feed, verbose_name=_("Feed"))
  date = models.DateTimeField(_("Date"))
  title = models.CharField(_("Title"), max_length=255)
  content = models.TextField(_("Content"), null=True, blank=True)
  content_type = models.CharField(_("Content Type"), max_length=255, null=True, blank=True)
  clean_content = models.TextField(null=True, blank=True)
  author = models.CharField(_("Author"), max_length=255, null=True, blank=True)
  permalink = models.URLField(_("Permalink"),max_length=1000)
  media_url = models.URLField(_("Media URL"),max_length=1000, null=True, blank=True)
  media_thumbnail_url = models.URLField(_("Media Thumbnail URL"), max_length=1000, null=True, blank=True)
  media_description = models.TextField(_("Media Description"), null=True, blank=True)
  media_description_type = models.CharField(_("Media Description Type"), max_length=50, null=True, blank=True)

  published = models.BooleanField(_("Published"), default=True)

  objects = ItemManager()
  
  @model_permalink
  def get_absolute_url(self):
    return ('item_page', (), {
      'item_id': self.id
    })
  
  def __unicode__(self):
    return self.title
    
  class Meta:
    db_table="items"
    ordering=["-date", "feed"]

#tagging.register(Item)
