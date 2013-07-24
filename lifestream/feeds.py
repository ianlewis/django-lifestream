#:coding=utf-8:
import re
import logging


from .models import *

logger = logging.getLogger(__name__)


def log_exception(msg):
    import traceback
    import sys
    tb = ''.join(traceback.format_exception(sys.exc_info()[0],
                                            sys.exc_info()[1], sys.exc_info()[2]))
    logger.exception(msg + "\n" + tb)


def update_feeds(queryset=None):
    feeds = queryset or Feed.objects.fetchable()
    for feed in feeds:
        try:
            feed_plugin = feed.get_plugin()
            feed_items = feed_plugin.parse_feed()

            if "bozo_exception" in feed_items:
                msg = u"Error occurred during parsing of feed '%s'\n" % feed.url
                logger.warning("%s%s" % (msg, feed_items["bozo_exception"]))

            included_entries = []
            for entry in feed_items['entries']:
                try:
                    feed_plugin.pre_process(entry)

                    if feed_plugin.include_entry(entry):
                        included_entries.append(entry)
                except:
                    log_exception(
                        u"Error importing item from feed '%s'" % feed.url)

            for entry in included_entries:
                try:
                    i = feed_plugin.process(entry)

                    feed_plugin.post_process(i)

                    i.save()

                    # Get tags
                    if 'tagging' in settings.INSTALLED_APPS:
                        from tagging.models import Tag
                        tags = ()
                        if 'tags' in entry:
                            for tag in entry['tags']:
                                tag_name = tag.get('term')[:30]
                                Tag.objects.add_tag(
                                    i, re.sub(r"[ ,]+", "_", tag_name))
                except:
                    log_exception(
                        u"Error importing item from feed '%s'" % feed.url)

        except:
            log_exception(u"Error importing feed: %s" % feed)
