#!/usr/bin/env python
#:coding=utf-8:

import urllib

from django.test import TransactionTestCase as DjangoTestCase

from testserver import PORT,FeedParserTestServer

class BaseTest(DjangoTestCase):
    base_url = "http://127.0.0.1:%s/%s"

    def setUp(self):
        self.server = FeedParserTestServer(1) 
        self.server.start()

    def get_url(self, path):
        return self.base_url % (PORT, path)

    def tearDown(self):
        if self.server.requests:
            self.server.requests = 0
            urllib.urlopen(self.get_url('/feeds/rss/bitbucket.xml')).read()
        self.server.join(0)
