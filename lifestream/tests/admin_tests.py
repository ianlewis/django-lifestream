#:coding=utf-8:

import threading
import logging

from django.test import TestCase as DjangoTestCase

from lifestream.tests.testserver import PORT,FeedParserTestServer,stop_server

from lifestream.admin import FeedCreationForm

class FeedCreateTest(DjangoTestCase):
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

    def tearDown(self):
        self.server = None
        stop_server(PORT)

    def test_bad_xml(self):
        form = FeedCreationForm({
            'lifestream': 1,
            'url': 'http://127.0.0.1:8097/feeds/rss/bad_xml.xml',
            'plugin_class_name': '',
        })
        self.assertTrue(form.is_valid())

    def test_no_title(self):
        form = FeedCreationForm({
            'lifestream': 1,
            'url': 'http://127.0.0.1:8097/feeds/rss/no_title.xml',
            'plugin_class_name': '',
        })
        self.assertTrue(not form.is_valid())
        self.assertTrue('url' in form.errors)
