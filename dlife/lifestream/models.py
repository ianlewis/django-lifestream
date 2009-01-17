#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

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
  feed_url = models.URLField(_("Feed Url"), verify_exists=True, max_length=1000)
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

class Tag(models.Model):
  '''item tag'''
  tag_name = models.CharField(_("Tag Name"), max_length=30)
  tag_slug = models.SlugField(_("Slug"), primary_key=True)
  tag_count = models.IntegerField(_("Count"))
  
  tag_visible = models.BooleanField(default=True)
  
  def __unicode__(self):
    return self.tag_name
  
  class Meta:
    db_table="tags"
    ordering=["-tag_visible", "-tag_count"]

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
  
  #Tag string used to save tags using django-tagging
  item_tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), null=True, blank=True, db_table="item_tags")
  
  item_published = models.BooleanField(_("Published"), default=True)
  
  _comment_count = None
  def _get_comment_count(self):
    if self._comment_count is None:
      self._comment_count = Comment.objects.filter(item=self).count()
    return self._comment_count
  comment_count = property(_get_comment_count)
  
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

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class Comment(models.Model):
  '''
  A feed comment.
  '''
  item = models.ForeignKey(Item, verbose_name=_("Feed"))
  user_name = models.CharField(_(u"User's Name"), max_length=50)
  user_email = models.EmailField(_(u"User's Email Address"))
  user_url = models.URLField(_(u"User's URL"), blank=True)
  date = models.DateTimeField(_("Date/Time Submitted"), auto_now_add=True)
  content = models.TextField(_("Comment"), max_length=COMMENT_MAX_LENGTH)
  
  def __unicode__(self):
    return str(self.id)
  
  class Meta:
    db_table="comments"
    ordering=["-date", "item"]
