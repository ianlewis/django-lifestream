#!/usr/bin/env python
#:coding=utf-8:

import re
import os
import SimpleHTTPServer, BaseHTTPServer
from threading import *

ROOT_PATH = os.path.dirname(__file__)

PORT = 8097 # not really configurable, must match hardcoded port in tests

class FeedParserTestRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  headers_re = re.compile(r"^Header:\s+([^:]+):(.+)$", re.MULTILINE)
  
  def send_head(self):
    """Send custom headers defined in test case

    Example:
    <!--
    Header:   Content-type: application/atom+xml
    Header:   X-Foo: bar
    -->
    """
    #path = self.translate_path(self.path)
    #path = os.path.join(ROOT_PATH, self.path)

    # For some reason os.path.join doesn't work.
    path = "%s/%s" % (ROOT_PATH, self.path)
    headers = dict(self.headers_re.findall(open(path).read()))
    f = open(path, 'rb')
    headers.setdefault('Status', 200)
    self.send_response(int(headers['Status']))
    headers.setdefault('Content-type', self.guess_type(path))
    self.send_header("Content-type", headers['Content-type'])
    self.send_header("Content-Length", str(os.fstat(f.fileno())[6]))
    for k, v in headers.items():
      if k not in ('Status', 'Content-type'):
        self.send_header(k, v)
    self.end_headers()
    return f

  def log_request(self, *args):
    pass

class FeedParserTestServer(Thread):
  """HTTP Server that runs in a thread and handles a predetermined number of requests"""
  
  def __init__(self, requests):
    Thread.__init__(self)
    self.requests = requests
    self.ready = 0
    
  def run(self):
    self.httpd = BaseHTTPServer.HTTPServer(('', PORT), FeedParserTestRequestHandler)
    self.ready = 1
    while self.requests:
      self.httpd.handle_request()
      self.requests -= 1
