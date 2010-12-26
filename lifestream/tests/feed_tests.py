#:coding=utf-8:

from base import FeedTest

from lifestream.models import *
from lifestream.feeds import update_feeds

class IanLewisFeedTest(FeedTest):
    fixtures = FeedTest.fixtures + ["ianlewis.json"]

    def test_ianlewis_rss(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=1).count(), 10)

class BitbucketFeedTest(FeedTest):
    fixtures = FeedTest.fixtures + ["bitbucket.json"]

    def test_bitbucket_atom(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=101).count(), 15)

    #TODO: test fails. feedparser broken
    def test_bitbucket_rss(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=102).count(), 15)

class YoutubeTest(FeedTest):
    fixtures = FeedTest.fixtures + ["youtube.json"]

    #TODO: test fails. feedparser broken
    def test_youtube_atom(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=201).count(), 25)

class DeliciousTest(FeedTest):
    fixtures = FeedTest.fixtures + ["delicious.json"]

    def test_delicious_top_rss(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=301).count(), 15)

    def test_delicious_user_rss(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=301).count(), 15)

class TwitterTest(FeedTest):
    fixtures = FeedTest.fixtures + ["twitter.json"]

    def test_twitter_user_rss(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=401).count(), 20)

class BloggerTest(FeedTest):
    fixtures = FeedTest.fixtures + ["blogger.json"]

    def test_blogger_blog_atom(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=501).count(), 25)

    def test_blogger_blog_rss(self):
        update_feeds()
        self.assertEqual(Item.objects.filter(feed__pk=502).count(), 25)

class RegressionFeedTest(FeedTest):
    fixtures = FeedTest.fixtures + ["regressions.json"]

    def assertNotEmpty(self, v):
        self.assertNotEqual(v, None)
        self.assertNotEqual(v, "")

    def test_content(self):
        update_feeds()
        for item in Item.objects.filter(feed__pk=10001):
            self.assertNotEmpty(item.content)
            self.assertNotEmpty(item.clean_content)
