#:coding=utf-8:

from lifestream.plugins import FeedPlugin

class FlickrPlugin(FeedPlugin):
    
    feed = None
    
    def __init__(self, feed):
        self.feed = feed
    
    def name(self):
        return "Flickr Feed"
    
    def pre_process(self, entry):
        super(FlickrPlugin, self).pre_process(entry)
        
        # Get the good resized image and put it in the media url
        # This is done by taking the thumbnail image url and removing
        # the "_s". No joke.
        if ("media_thumbnail_attrs" in entry and
                "url" in entry["media_thumbnail_attrs"]):
            entry["media_content_attrs"]["url"] = (
                entry["media_thumbnail_attrs"]["url"].replace("_s", ""))
