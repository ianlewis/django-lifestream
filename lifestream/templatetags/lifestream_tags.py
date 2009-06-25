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
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument." % bits[0])
    return LifestreamItemDetailNode(bits[1])

@register.filter
def urlize_twitter(text):
    import re
    return mark_safe(re.sub(r'@([a-zA-Z0-9_]*)', r'@<a href="http://twitter.com/\1">\1</a>', text))
