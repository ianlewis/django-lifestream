#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from dlife.lifestream.plugins import FeedPlugin

class TwitterPlugin(FeedPlugin):
  
  feed = None
  
  def __init__(self, feed):
    self.feed = feed
  
  def name(self):
    return "Generic Feed"
  
  def pre_process(self, entry):
    super(TwitterPlugin, self).pre_process(entry)
    
    #Remove the username from the title data.
    index = entry['title'].find(":")
    if index != -1:
      entry['title'] = entry['title'][index+2:]
      
    #TODO: change @user replies to links
    #TODO: linkify urls