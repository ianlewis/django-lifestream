#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings
import stripper

def get_url_domain(url):
  protocol_index = url.find('://')+3 if url.find('://')!=-1 else 0
  slash_index = url.find('/', protocol_index) if url.find('/', protocol_index)!=-1 else len(url)
  
  sub_url = url[protocol_index:slash_index]
  parts = sub_url.split('.')
  
  if len(parts) > 2 and parts[0] in ('feeds','www','feedproxy','rss','gdata','api'):
    return '.'.join(parts[1:])
  else:
    return sub_url

def clean_item_content(content):
  semi_clean_content = stripper.strip_tags(content, settings.VALID_ITEM_TAGS)
  clean_content = stripper.strip_tags(content, ())
  return semi_clean_content, clean_content
