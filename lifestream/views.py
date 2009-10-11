#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.views.generic.list_detail import object_list,object_detail
from django.conf import settings
from django.shortcuts import get_object_or_404

from lifestream.util.decorators import allow_methods

from lifestream.models import *

DEFAULT_PAGINATION = getattr(settings, 'LIFESTREAM_DEFAULT_PAGINATION', 20)

@allow_methods('GET')
def main_page(request, lifestream_slug):
    lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
    return object_list(request, 
        queryset = Item.objects.published_items(lifestream),
        paginate_by = DEFAULT_PAGINATION,
        extra_context = {
            'lifestream': lifestream,
        },
    )

@allow_methods('GET', 'POST')
def item_page(request, lifestream_slug, item_id):
    lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
    return object_detail(
        request,
        queryset=Item.objects.published_items(lifestream),
        object_id=item_id,    
        extra_context = {
            'lifestream': lifestream,
        },
    )

@allow_methods('GET')
def domain_page(request, lifestream_slug, domain):
    lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
    return object_list(
        request,
        queryset=Item.objects.published_items(lifestream).filter(feed__domain=domain),
        paginate_by = DEFAULT_PAGINATION,
        extra_context = {
            'lifestream': lifestream,
        },
    )

