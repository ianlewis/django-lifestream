#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from util.decorators import allow_methods

from models import *

@allow_methods('GET')
def main_page(request, page="1"):
  item_list = Item.objects.order_by('-item_date')
  paginator = Paginator(item_list, 9) # Show 9 items per page

  # Make sure page request is an int. If not, deliver first page.
  # TODO: make a better url for this like /page/1
  try:
    page = int(page)
  except ValueError:
    page = 1

  # If page request (9999) is out of range, deliver last page of results.
  try:
    items = paginator.page(page)
  except (EmptyPage, InvalidPage):
    items = paginator.page(paginator.num_pages)
  
  return direct_to_template(request, "main.tpl", { "items": items })
  
@allow_methods('GET')
def item_page(request, item_id=None):
  try:
    item = Item.objects.get(id=item_id)
    
    return direct_to_template(request, "item.tpl", { "item": item })
  except Item.DoesNotExist:
    raise Http404