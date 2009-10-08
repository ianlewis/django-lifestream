#!/usr/bin/env python
#:coding=utf-8:

import re
import os
from threading import *

import httplib
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

ROOT_PATH = os.path.dirname(__file__)

PORT = 8097 # not really configurable, must match hardcoded port in tests

class FeedParserTestRequestHandler(SimpleHTTPRequestHandler):
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

    def do_QUIT(self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

class StoppableHttpServer(HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()

class FeedParserTestServer(Thread):
    """HTTP Server that runs in a thread and handles a predetermined number of requests"""
    TIMEOUT=10
  
    def __init__(self, cond=None):
        Thread.__init__(self)
        self.ready = False 
        self.cond = cond
    
    def run(self):
        self.cond.acquire()
        timeout=0 
        self.httpd = None
        while self.httpd is None:
            try:
                self.httpd = StoppableHttpServer(('', PORT), FeedParserTestRequestHandler)
            except Exception, e:
                import socket,errno,time
                if isinstance(e, socket.error) and errno.errorcode[e.args[0]] == 'EADDRINUSE' and timeout < self.TIMEOUT:
                    timeout+=1
                    time.sleep(1) 
                else:
                    self.cond.notifyAll()
                    self.cond.release()
                    self.ready = True
                    raise e
        self.ready = True 
        if self.cond:
            self.cond.notifyAll()
            self.cond.release()
        self.httpd.serve_forever()

def stop_server(port):
    """send QUIT request to http server running on localhost:<port>"""
    conn = httplib.HTTPConnection("127.0.0.1:%d" % port)
    conn.request("QUIT", "/")
    conn.getresponse()
