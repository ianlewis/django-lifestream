#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

import tagging

class Lifestream(models.Model):
  '''A lifestream itself.'''
  ls_title = models.CharField(_("Title"), max_length=128)
  ls_tagline = models.TextField(_("Tagline"), null=True, blank=True)
  
  ls_baseurl = models.CharField(_("Base Url"), max_length=1000)
  
  items_per_page = models.IntegerField(_("Items Per Page"), default=10)
  
  ls_user = models.ForeignKey(User)
  
  def __unicode__(self):
    return self.ls_title
  
  class Meta:
    db_table="lifestream"

class FeedManager(models.Manager):
  ''' Query only normal feeds. '''
  
  def get_feeds(self):
    return super(FeedManager, self) \
           .get_query_set().filter(feed_basic_feed=False)
  
  def get_fetchable_feeds(self):
    return self.get_feeds().filter(feed_fetchable=True)

class Feed(models.Model):
  '''A feed for gathering data.'''
  feed_lifestream = models.ForeignKey(Lifestream,verbose_name=_("Lifestream"))
  
  feed_name = models.CharField(_("Feed Name"), max_length=255)
  feed_url = models.URLField(_("Feed Url"), help_text=_("Must be a valid url"), verify_exists=True, max_length=1000)
  feed_domain = models.CharField(_("Feed Domain"), max_length=255)
  feed_fetchable = models.BooleanField(_("Fetchable"), default=True)
  
  # Used for feeds that allow users to directly add to the lifestream.
  feed_basic_feed = models.BooleanField(default=False)
  
  # The feed plugin name used to process the incoming feed data.
  feed_plugin = models.CharField(_("Plugin Name"), max_length=255, null=True, blank=True, choices=settings.PLUGINS)
  
  objects = FeedManager()
  
  def __unicode__(self):
    return self.feed_name
    
  class Meta:
    db_table="feeds"

class Item(models.Model):
  '''A feed item'''
  item_feed = models.ForeignKey(Feed, verbose_name=_("Feed"))
  item_date = models.DateTimeField(_("Date"))
  item_title = models.CharField(_("Title"), max_length=255)
  item_content = models.TextField(_("Content"), null=True, blank=True)
  item_content_type = models.CharField(_("Content Type"), max_length=255, null=True, blank=True)
  item_clean_content = models.TextField(null=True, blank=True)
  item_author = models.CharField(_("Author"), max_length=255, null=True, blank=True)
  item_permalink = models.CharField(_("Permalink"), max_length=1000)
  
  item_published = models.BooleanField(_("Published"), default=True)
  
  @permalink
  def get_absolute_url(self):
    return ('item_page', (), {
      'item_id': self.id
    })
  
  def __unicode__(self):
    return self.item_title
    
  class Meta:
    db_table="items"
    ordering=["-item_date", "item_feed"]

#tagging.register(Item)
