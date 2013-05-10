#:coding=utf-8:

from django.views.generic import ListView, DetailView
from django.conf import settings
from django.shortcuts import get_object_or_404

from lifestream.models import Lifestream, Item

DEFAULT_PAGINATION = getattr(settings, 'LIFESTREAM_DEFAULT_PAGINATION', 20)


class MainPage(ListView):
    model = Item
    paginate_by = DEFAULT_PAGINATION

    def dispatch(self, request, lifestream_slug):
        self.lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
        return super(MainPage, self).dispatch(request=request)

    def get_queryset(self):
        return Item.objects.published_items(self.lifestream)

    def get_context_data(self, object_list):
        context = super(MainPage, self).get_context_data(
            object_list=object_list)
        context['lifestream'] = self.lifestream
        return context

main_page = MainPage.as_view()


class ItemPage(DetailView):
    pk_url_kwarg = 'item_id'

    def dispatch(self, request, lifestream_slug, item_id):
        self.lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
        return super(ItemPage, self).dispatch(request=request, item_id=item_id)

    def get_queryset(self):
        return Item.objects.published_items(self.lifestream)

    def get_context_data(self, object):
        context = super(ItemPage, self).get_context_data(object=object)
        context['lifestream'] = self.lifestream
        return context

item_page = ItemPage.as_view()


class DomainPage(ListView):
    paginate_by = DEFAULT_PAGINATION

    def dispatch(self, request, lifestream_slug, domain):
        self.lifestream = get_object_or_404(Lifestream, slug=lifestream_slug)
        self.domain = domain
        return super(DomainPage, self).dispatch(request=request)

    def get_queryset(self):
        return Item.objects.published_items(self.lifestream).filter(feed__domain=self.domain)

    def get_context_data(self, object_list):
        context = super(DomainPage, self).get_context_data(
            object_list=object_list)
        context['lifestream'] = self.lifestream
        return context

domain_page = DomainPage.as_view()
