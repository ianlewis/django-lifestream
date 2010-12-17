#:coding=utf-8:

# This file written by Ian Lewis (IanLewis@member.fsf.org)
# Copyright 2009 by Ian Lewis

from django.contrib.syndication.feeds import Feed as SyndicationFeed
from django.core.urlresolvers import reverse
from django.conf import settings

from lifestream.models import *

class RecentItemsFeed(SyndicationFeed):
    title = "Recent Items"
    description = "Recent Lifestream Items"

    def link(self, obj):
        return reverse('lifestream_main_page', kwargs={
            'lifestream_slug': obj.slug,
        })

    def get_object(self, bits):
        return Lifestream.objects.get(slug=bits[0])

    def items(self, obj):
        return Item.objects.published()\
                           .filter(feed__lifestream=obj)[:10]

    def item_pubdate(self, item):
        return item.date

    def item_categories(self, item):
        def item_categories(self, item):
            if 'tagging' in settings.INSTALLED_APPS:
                return [tag.name for tag in item.tag_set]
            else:
                return []
