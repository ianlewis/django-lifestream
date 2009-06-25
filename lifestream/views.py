#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list,object_detail
from django.core.urlresolvers import reverse
from django.conf import settings

from lifestream.util.decorators import allow_methods

from lifestream.models import *

@allow_methods('GET')
def main_page(request):
  return object_list(request, 
      queryset = Item.objects.published(), 
      template_name = "lifestream/main.html",
  )

@allow_methods('GET')
def tag_page(request, tag):
    from tagging.views import tagged_object_list
    return tagged_object_list(
        request,
        queryset_or_model=Item.objects.published(),
        tag=tag,
    )

@allow_methods('GET')
def domain_page(request, domain):
    return object_list(
        request,
        queryset=Item.objects.published().filter(feed__domain=domain),
    )

@allow_methods('GET', 'POST')
def item_page(request, item_id):
  return object_detail(
        request,
        queryset=Item.objects.published(),
        object_id=item_id,    
    )
