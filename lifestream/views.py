#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.conf import settings

from lifestream.util.decorators import allow_methods

from lifestream.models import *

ITEMS_PER_PAGE = getattr(settings,"LIFESTREAM_ITEMS_PER_PAGE",10)

@allow_methods('GET')
def main_page(request, page="1"):
  item_list = Item.objects.published()
  paginator = Paginator(item_list, ITEMS_PER_PAGE)

  # Make sure page request is an int. If not, deliver first page.
  try:
    page = int(page)
  except ValueError:
    page = 1

  # If page request (9999) is out of range, deliver last page of results.
  try:
    items = paginator.page(page)
  except (EmptyPage, InvalidPage):
    items = paginator.page(paginator.num_pages)
  
  return direct_to_template(request, "lifestream/main.html", { "items": items })
  
@allow_methods('GET', 'POST')
def item_page(request, item_id=None):
  try:
    item = Item.objects.get(id=item_id,published=True)
  except Item.DoesNotExist:
    raise Http404
  
  return direct_to_template(request, "lifestream/item.html", { 
    "item": item,
  })
  
