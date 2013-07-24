import logging
import types
import socket

import feedparser

from django.conf import settings

from .util import sanitize_html

logger = logging.getLogger(__name__)


# MonkeyPatch feedparser to get the media:description type attribute and
# map the 'plain' content type properly.


def _start_media_description(self, attrsD):
    self.pushContent('media_description', attrsD, 'text/html', 1)


def _end_media_description(self):
    contentType = self.contentparams.get('type', 'text/html')
    value = self.popContent('media_description')
    context = self._getContext()
    context['media_description'] = feedparser.FeedParserDict(
        {'type': contentType})
    context['media_description']['content'] = value


def _mapContentType(self, contentType):
    contentType = feedparser._FeedParserMixin.mapContentType(self, contentType)
    if contentType == 'plain':
        contentType = 'text/plain'
    return contentType

feedparser._FeedParserMixin._start_media_description = (
    types.MethodType(
        _start_media_description,
        None, feedparser._FeedParserMixin))
feedparser._FeedParserMixin._end_media_description = (
    types.MethodType(
        _end_media_description,
        None, feedparser._FeedParserMixin))

if hasattr(feedparser, '_StrictFeedParser'):
    feedparser._StrictFeedParser.mapContentType = (
        types.MethodType(
            _mapContentType,
            None, feedparser._StrictFeedParser))

feedparser._LooseFeedParser.mapContentType = (
    types.MethodType(
        _mapContentType,
        None, feedparser._LooseFeedParser))

# Change out feedparser's html sanitizer for our own based
# on BeautifulSoup and our own tag/attribute stripper.
feedparser._sanitizeHTML = sanitize_html


try:
    from feedcache import Cache
    from util import CacheStorage
    # TODO: Use a cache storage object.
    feed_cache = Cache(CacheStorage())

    def _parse_feed(url):
        """
        Parses a feed. Uses feedcache if it is available
        using django's cache framework as storage for
        feedcache.
        """
        logger.info("Using feedcache to parse feed '%s'" % url)
        if not feedparser._XML_AVAILABLE:
            logger.warning(
                "XML parser is not available. Feedparser will use a non-strict xml parser")
        return feed_cache.fetch(url)
except ImportError:
    # Fall back to using feedparser
    def _parse_feed(url):
        logger.info("Using feedparser (no feedcache) to parse feed '%s'" % url)
        if not feedparser._XML_AVAILABLE:
            logger.warning(
                "XML parser is not available. Feedparser will use a non-strict xml parser")
        return feedparser.parse(url)


def parse_feed(url):
    old_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(
            getattr(settings, 'LIFESTREAM_FEED_TIMEOUT', 30))
        return _parse_feed(url)
    finally:
        socket.setdefaulttimeout(old_timeout)
