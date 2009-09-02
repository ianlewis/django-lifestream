#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from datetime import datetime,timedelta

from django.utils.safestring import mark_safe
from django.template import Node, Library, TemplateDoesNotExist, TemplateSyntaxError, Variable
from django.template.loader import render_to_string

register = Library()

@register.simple_tag
def item_class(item):
    """
    A template tag that is used to identify the data
    item by domain. This is used to get the item's template
    name when rendering. It can also be used for css classes.
    """
    return item.feed.domain.replace(".", "-") 

class LifestreamItemNode(Node):
    def __init__(self, item_var):
        self.item_var = Variable(item_var)

    def render(self, context):
        item = self.item_var.resolve(context)
        context["object"] = item
        try:
            template_name = "lifestream/sites/%s.html" % item_class(item)
            return render_to_string(template_name, context)
        except TemplateDoesNotExist, e:
            template_name = "lifestream/sites/basic.html"
            return render_to_string(template_name, context)

@register.tag
def render_item(parser, token):
    """
    Renders an item in an item list based on the item's type
    (feed domain).
    This tag first checks if there is a template in
    lifestream/sites with the name of the feed domain
    ('.' characters are replaced by '-' characters)
    e.g. 'twitter-com.html'

    If the template doesn't exist it falls back on the default
    basic_detail.html
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument." % bits[0])
    return LifestreamItemNode(bits[1])

class LifestreamItemDetailNode(Node):
    def __init__(self, item_var):
        self.item_var = Variable(item_var)

    def render(self, context):
        item = self.item_var.resolve(context)
        context["object"] = item
        try:
            template_name = "lifestream/sites/%s_detail.html" % item_class(item)
            return render_to_string(template_name, context)
        except TemplateDoesNotExist, e:
            template_name = "lifestream/sites/basic_detail.html"
            return render_to_string(template_name, context)

@register.tag
def render_item_detail(parser, token):
    """
    Renders an item's detail html for an item detail page
    based on the item's type (feed domain).
    This tag first checks if there is a template in
    lifestream/sites with the name of the feed domain
    ('.' characters are replaced by '-' characters) and ending
    _.html. e.g. 'twitter-com_detail.html'

    If the template doesn't exist it falls back on the default
    basic_detail.html
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument." % bits[0])
    return LifestreamItemDetailNode(bits[1])
