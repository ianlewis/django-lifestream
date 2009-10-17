#!/usr/bin/env python
#:coding=utf-8:

import urllib
import threading
import logging

from django.test import TestCase as DjangoTestCase

from testserver import PORT,FeedParserTestServer,stop_server

from lifestream.util import *

class FeedTest(DjangoTestCase):
    base_url = "http://127.0.0.1:%s/%s"
    fixtures = ["base.json"]

    def setUp(self):
        # Disable logging to the console
        logging.disable(logging.CRITICAL+1)

        self.cond = threading.Condition()
        self.server = FeedParserTestServer(self.cond) 
        self.cond.acquire()
        self.server.start()

        # Wait until the server is ready
        while not self.server.ready:
            # Collect left over servers so they release their
            # sockets
            import gc
            gc.collect()
            self.cond.wait()

        self.cond.release()

    def get_url(self, path):
        return self.base_url % (PORT, path)

    def tearDown(self):
        self.server = None
        stop_server(PORT)

class HTMLSanitizationTest(DjangoTestCase):
    valid_tags = VALID_TAGS
    valid_styles = VALID_STYLES
    test_html = () 

    def test_html_sanitization(self):
        for html in self.test_html:
            sanitized_html = sanitize_html(html[0], valid_tags=self.valid_tags)
            self.assertEqual(sanitized_html, html[1])

class EntityConversionTest(DjangoTestCase):
    test_html = ()

    def test_convert_entities(self):
        for html in self.test_html:
            converted = convert_entities(html[0])
            self.assertEqual(converted, html[1])
