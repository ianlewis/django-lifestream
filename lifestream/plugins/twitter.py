#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from lifestream.plugins import FeedPlugin

class TwitterPlugin(FeedPlugin):
  
    feed = None
  
    def __init__(self, feed):
        self.feed = feed
  
    def name(self):
        return "Generic Feed"
  
    def post_process(self, item):
        super(TwitterPlugin,self).post_process(item)

        #Remove the username from the title data.
        if item.title:
            index = item.title.find(":")
            if index != -1:
                item.title = item.title[index+2:]

        if item.content:
            index = item.content.find(":")
            if index != -1:
                item.content = item.content[index+2:]
