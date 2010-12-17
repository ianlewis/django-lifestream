#:coding=utf-8:

from django.views.generic.list_detail import object_list,object_detail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from lifestream.models import *

DEFAULT_PAGINATION = getattr(settings, 'LIFESTREAM_DEFAULT_PAGINATION', 20)

@require_http_methods(['GET', 'HEAD'])
def main_page(request, lifestream_slug):
    lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
    return object_list(request, 
        queryset = Item.objects.published_items(lifestream),
        paginate_by = DEFAULT_PAGINATION,
        extra_context = {
            'lifestream': lifestream,
        },
    )

@require_http_methods(['GET', 'HEAD', 'POST'])
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

@require_http_methods(['GET', 'HEAD'])
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

