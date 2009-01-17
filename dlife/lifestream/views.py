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

from dlife.util.decorators import allow_methods

from dlife.lifestream.models import *
from dlife.lifestream.forms import *

@allow_methods('GET')
def main_page(request, page="1"):
  item_list = Item.objects.order_by('-item_date')
  paginator = Paginator(item_list, request.lifestream.items_per_page) 

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
  
@allow_methods('GET', 'POST')
def item_page(request, item_id=None):
  try:
    item = Item.objects.get(id=item_id)
  except Item.DoesNotExist:
    raise Http404
  
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      Comment.objects.create(item=item,
        user_name = form.cleaned_data['user_name'],
        user_email = form.cleaned_data['user_email'],
        user_url = form.cleaned_data['user_url'],
        content = form.cleaned_data['content'],
      )
      return HttpResponseRedirect(reverse('item_page', kwargs={'item_id':item.id}))
  else:
    form = CommentForm()
    
  comments = Comment.objects.filter(item=item)
  form.action = reverse('item_page', kwargs={'item_id':item.id})
  form.method = 'POST'
  
  return direct_to_template(request, "item.tpl", { 
    "item": item,
    "item_comments": comments,
    "comment_form": form,
  })
  