#!/usr/bin/env python
#:coding=utf-8:

import urllib
import threading
import logging

from django.test import TransactionTestCase as DjangoTestCase

from testserver import PORT,FeedParserTestServer,stop_server

class BaseTest(DjangoTestCase):
    base_url = "http://127.0.0.1:%s/%s"

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
