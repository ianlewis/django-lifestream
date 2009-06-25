#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from lifestream.plugins import FeedPlugin

class YoutubePlugin(FeedPlugin):
  
  feed = None
  
  def __init__(self, feed):
    self.feed = feed
  
  def name(self):
    return "Youtube Feed"
  
  def pre_process(self, entry):
    super(YoutubePlugin, self).pre_process(entry)
    #Update the media player url
    if "media_player_attrs" in entry and "url" in entry["media_player_attrs"]:
        entry["media_player_attrs"]["url"] = entry["media_player_attrs"]["url"].replace("?v=", "/v/")

    # youtube includes a strange schema url in the tags
    for tag in entry["tags"]:
        tag_term = tag.get('term')
        if tag_term and \
          (tag_term.startswith("http://") or \
           tag_term.startswith("yt:")):
            entry["tags"].remove(tag)
