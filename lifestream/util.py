#:coding=utf-8:

import re

from django.conf import settings
from django.core.cache import cache

from BeautifulSoup import BeautifulSoup, Comment

class CacheStorage(object):
    """
    A class implementing python's dictionary API
    for use as a storage backend for feedcache.
    
    Uses django's cache framework for the backend
    of the cache.

    TODO: Use a cache timeout setting for the cache
    time and use the same value for feedcache.
    """
    def get(self, key, default=None):
        return cache.get(self._get_key(key), default)

    def __setitem__(self, key, value):
        cache.set(self._get_key(key), value)

    def __getitem__(self, key):
        return cache.get(self._get_key(key))

    def __delitem__(self, key):
        return cache.delete(self._get_key(key))

    def _get_key(self, key):
        return "lifestream-cache-%s" % key

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

# default settings
# VALID_TAGS is a dictionary where the key is a tag name
# and the value is a list of valid attributes.
# If the attributes list is None then all attributes are allowed.
# An empty list specifies that no attributes are allowed.
VALID_TAGS = {
    'b': (),
    'blockquote': (),
    'em': (),
    'strong': (),
    'strike': (),
    'a': ('href', 'title', 'rel'),
    'i': (),
    'br': (),
    'ul': (),
    'ol': (),
    'li': (),
    'u': (),
    'p': (),
    'h1': (),
    'h2': (),
    'h3': (),
    'h4': (),
    'table': (),
    'thead': (),
    'tbody': (),
    'tfoot': (),
    'th': (),
    'td': ('colspan',),
    'tr': ('rowspan',),
    'img': ('src', 'alt', 'title', 'width', 'height'),
    'span': (),
}

# VALID_STYLES is a list of css style names that are
# valid in style attributes.
VALID_STYLES = (
    "color",
    "font-weight",
)

def escape_entities(text):
        return re.sub(r'&(?![A-Za-z]+;)', '&amp;', text)\
                 .replace('<','&lt;')\
                 .replace('>', '&gt;')\
                 .replace('"', '&quot;')\
                 .replace("'", '&apos;')

def convert_entities(text):
    if text is None:
        return None
    entities = {
        u'&amp;': u'&',
        u'&lt;': u'<',
        u'&gt;': u'>',
        u'&quot;': u'"',
        u'&apos;': u"'",
    }
    for entity in entities:
        text = text.replace(entity, entities[entity])
    return text

def sanitize_html(htmlSource, encoding=None, type="text/html", valid_tags=None, valid_styles=None):
    """
    Clean bad html content. Currently this simply strips tags that
    are not in the VALID_TAGS setting.
    
    This function is used as a replacement for feedparser's _sanitizeHTML
    and fixes problems like unclosed tags and gives finer grained control
    over what attributes can appear in what tags.

    Returns the sanitized html content.
    """
    if valid_tags is None:
        valid_tags = getattr(settings, "LIFESTREAM_VALID_TAGS", VALID_TAGS)
    if valid_styles is None:
        valid_styles = getattr(settings, "LIFESTREAM_VALID_STYLES", VALID_STYLES)


    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    css_regex = re.compile(r' *(%s): *([^;]*);?' % '|'.join(valid_styles), re.IGNORECASE)

    # Sanitize html with BeautifulSoup
    if encoding:
        soup = BeautifulSoup(htmlSource, fromEncoding=encoding)
    else:
        soup = BeautifulSoup(htmlSource)
    
    # Remove html comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
 
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
                         if attr in valid_tags[tag.name]]
    
    # Strip disallowed css tags.
    for tag in soup.findAll(attrs={"style":re.compile(".*")}):
        style = ""
        for key,val in css_regex.findall(tag["style"]):
            style += "%s:%s;" % (key,val.strip())
        tag["style"] = style

    # Sanitize html text by changing bad text to entities.
    # BeautifulSoup will do this for href and src attributes
    # on anchors and image tags but not for text.
    for text in soup.findAll(text=True):
        text.replaceWith(escape_entities(text))
   
    # Strip disallowed tags and attributes.
    return soup.renderContents().decode('utf8') 
