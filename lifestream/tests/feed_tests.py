#!/usr/bin/env python
#:coding=utf-8:

from base import BaseTest
from lifestream.models import *

from lifestream.feeds import update_feeds

class RssFeedTest(BaseTest):
    fixtures = ["rss.json"]

    def test_bitbucket_feed(self):
        update_feeds()
        assert Item.objects.filter(feed__pk=1).count() == 15

class AtomFeedTest(BaseTest):
    fixtures = ["atom.json"]

    #TODO: test fails. feedparser is broken
    def test_bitbucket_atom_feed(self):
        update_feeds()
        assert Item.objects.filter(feed__pk=2).count() == 15

    def test_youtube(self):
        update_feeds()
        assert Item.objects.filter(feed__pk=3).count() == 25
