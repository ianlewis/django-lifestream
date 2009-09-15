#!/usr/bin/env python
#:coding=utf-8:

from base import BaseTest
from lifestream.models import *
from lifestream.feeds import update_feeds

class GoodFeedTest(BaseTest):
    fixtures = ["rss.json"]

    def test_good_feed(self):
        update_feeds() 
        assert Item.objects.filter(feed__pk=1).count() == 15
