#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

#Code taken from
#http://code.activestate.com/recipes/52281/

import HTMLParser, string

class StrippingParser(HTMLParser.HTMLParser):

    # These are the HTML tags that we will leave intact
    # This spec is a dictionary of tag names to
    # a list of attributes that may remain in the tag
    # If the list is None, then all attributes are ok.
    valid_tags = {
        'b': (),
        'a': ('href', 'title'),
        'i': (),
        'br': (),
        'p': (),
    }

    from htmlentitydefs import entitydefs # replace entitydefs from sgmllib
    
    def __init__(self, valid_tags=None):
        HTMLParser.HTMLParser.__init__(self)
        self.result = ""
        self.endTagList = []
        if valid_tags is not None:
            self.valid_tags = valid_tags
        
    def handle_data(self, data):
        if data:
            self.result = self.result + data

    def handle_charref(self, name):
        self.result = "%s&#%s;" % (self.result, name)
        
    def handle_entityref(self, name):
        if self.entitydefs.has_key(name): 
            x = ';'
        else:
            # this breaks unstandard entities that end with ';'
            x = ''
        self.result = "%s&%s%s" % (self.result, name, x)
    
    def handle_starttag(self, tag, attrs):
        """ Delete all tags except for legal ones """
        if tag in self.valid_tags:
            self.result = self.result + '<' + tag
            for k, v in attrs:
                valid_attrs = self.valid_tags[tag]

                # Drop disallowed attributes.
                # Make sure we don't include some javascript hrefs
                if (valid_attrs is None or k in valid_attrs) and \
                   string.lower(k[0:2]) != 'on' and string.lower(v[0:10]) != 'javascript':
                    self.result = '%s %s="%s"' % (self.result, k, v)
            endTag = '</%s>' % tag
            self.endTagList.insert(0,endTag)    
            self.result = self.result + '>'
                
    def handle_endtag(self, tag):
        if tag in self.valid_tags:
            self.result = "%s</%s>" % (self.result, tag)
            remTag = '</%s>' % tag
            self.endTagList.remove(remTag)

    def cleanup(self):
        """ Append missing closing tags """
        for j in range(len(self.endTagList)):
                self.result = self.result + self.endTagList[j]    
        

def strip_tags(s, valid_tags=None):
    """ Strip illegal HTML tags from string s """
    parser = StrippingParser(valid_tags)
    parser.feed(s)
    parser.close()
    parser.cleanup()
    return parser.result
