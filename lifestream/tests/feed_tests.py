#!/usr/bin/env python
#:coding=utf-8:

from base import BaseTest
from lifestream.models import *

from lifestream.feeds import update_feeds

class RssFeedTest(BaseTest):
    fixtures = ["rss.json"]

    def test_bitbucket_feed(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=1).count(), 15)

    #TODO: test fails.
    def test_ianlewis_feed(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=2).count(), 10)

class AtomFeedTest(BaseTest):
    fixtures = ["atom.json"]

    #TODO: test fails.
    def test_bitbucket_atom_feed(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=100).count(), 15)

    def test_youtube(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=101).count(), 25)

class RegressionTest(BaseTest):
    fixtures = ["regressions.json"]

    def assertNotEmpty(self, v):
        self.assertNotEqual(v, None)
        self.assertNotEqual(v, "")

    def test_content(self):
        update_feeds()
        for item in Item.objects.filter(feed__pk=1):
            self.assertNotEmpty(item.content)
            self.assertNotEmpty(item.clean_content)
