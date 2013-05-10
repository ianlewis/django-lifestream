#:coding=utf-8:
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

DEFAULT_PLUGINS = (
  ('lifestream.plugins.FeedPlugin', 'Generic Feed'),
  ('lifestream.plugins.twitter.TwitterPlugin', 'Twitter Plugin'),
  ('lifestream.plugins.youtube.YoutubePlugin', 'Youtube Plugin'),
  ('lifestream.plugins.flickr.FlickrPlugin', 'Flickr Plugin'),
)

class Lifestream(models.Model):
    """
    A lifestream. Lifestreams can be created per user.
    """
    site = models.ForeignKey('sites.Site', verbose_name=_(u"site"), db_index=True)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"user"), db_index=True)
    slug = models.SlugField(_("slug"), help_text=_('Slug for use in urls (Autopopulated from the title).'), db_index=True)
    title = models.CharField(_("title"), max_length=255)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'lifestream.views.main_page', (), {'lifestream_slug': self.slug}


class FeedManager(models.Manager):
    ''' Query only normal feeds. '''

    def fetchable(self):
        return self.filter(fetchable=True)

class Feed(models.Model):
    '''A feed for gathering data.'''
    lifestream = models.ForeignKey(Lifestream, verbose_name=_('lifestream'), db_index=True)
    name = models.CharField(_("feed name"), max_length=255)
    url = models.URLField(_("feed url"), max_length=1000,
            help_text=_("Must be a valid url."))
    domain = models.CharField(_("feed domain"), max_length=255, db_index=True)
    permalink = models.URLField(_("permalink"), max_length=1000, blank=True, null=True,
            help_text=_("Permalink to the feed page."))
    fetchable = models.BooleanField(_("fetchable"), default=True, db_index=True)

    # The feed plugin name used to process the incoming feed data.
    plugin_class_name = models.CharField(_("plugin name"), max_length=255,
        null=True, blank=True, choices=getattr(settings, "LIFESTREAM_PLUGINS",
            getattr(settings, "PLUGINS", DEFAULT_PLUGINS)))

    objects = FeedManager()

    def __unicode__(self):
        return self.name

class ItemManager(models.Manager):
    """Manager for querying Items"""

    def published_items(self, lifestream):
        """
        Published items for a lifestream based on the slug.
        """
        return self.published().filter(feed__lifestream=lifestream)

    def published(self):
        return self.filter(published=True).order_by("-date")

class Item(models.Model):
    '''A feed item'''
    feed = models.ForeignKey(Feed, verbose_name=_("feed"), db_index=True)
    date = models.DateTimeField(_("date"), db_index=True)
    title = models.CharField(_("title"), max_length=255, help_text=_("The title of the item. Could be html."))
    content = models.TextField(_("content"), null=True, blank=True, help_text=_("Rich item content. Could be html based on the content type. This html is escaped."))
    content_type = models.CharField(_("content type"), max_length=255, null=True, blank=True)
    clean_content = models.TextField(null=True, blank=True, help_text=_("Cleaned, plain text version of the item content."))
    author = models.CharField(_("author"), max_length=255, null=True, blank=True)
    permalink = models.URLField(_("permalink"),max_length=1000, help_text=_("Permalink to the original item."))
    media_url = models.URLField(_("media url"),max_length=1000, null=True, blank=True)
    media_thumbnail_url = models.URLField(_("media thumbnail url"), max_length=1000, null=True, blank=True)
    media_player_url = models.URLField(_("media player url"), max_length=1000, null=True, blank=True)
    media_description = models.TextField(_("media description"), null=True, blank=True)
    media_description_type = models.CharField(_("media description type"), max_length=50, null=True, blank=True)

    published = models.BooleanField(_("published"), default=True, db_index=True)

    objects = ItemManager()

    @models.permalink
    def get_absolute_url(self):
        return ('lifestream.views.item_page', (), {
            'lifestream_slug': self.feed.lifestream.slug,
            'item_id': str(self.id),
        })

    def __unicode__(self):
        return self.title

    class Meta:
        ordering=["-date", "feed"]
