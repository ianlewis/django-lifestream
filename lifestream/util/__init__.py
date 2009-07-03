#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.conf import settings
# TODO: make this a pip requirement
import stripper

# default settings
VALID_ITEM_TAGS = (
  'b',
  'a',
  'i',
  'br',
  'p',
  'h1',
  'h2',
  'h3',
  'h4',
  'table',
  'tbody',
  'th',
  'td',
  'tr',
  'img',
  'span',
)

def get_url_domain(url):
  """
  Get a domain from the feed url. This attempts to
  get a clean url by ignoring know subdomains used for
  serving feeds such as www, feeds, api etc.
  """
  protocol_index = url.find('://')+3 if url.find('://')!=-1 else 0
  slash_index = url.find('/', protocol_index) if url.find('/', protocol_index)!=-1 else len(url)
  
  sub_url = url[protocol_index:slash_index]
  parts = sub_url.split('.')
  
  if len(parts) > 2 and parts[0] in ('feeds','www','feedproxy','rss','gdata','api'):
    return '.'.join(parts[1:])
  else:
    return sub_url

def clean_item_content(content):
  """
  Clean bad html content. Currently this simply strips tags that
  are not in the VALID_TAGS setting.
  """
  semi_clean_content = stripper.strip_tags(content, getattr(settings, "LIFESTREAM_VALID_TAGS", VALID_TAGS))
  clean_content = stripper.strip_tags(content, ())
  return semi_clean_content, clean_content
