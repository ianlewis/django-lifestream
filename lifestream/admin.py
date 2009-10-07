#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.contrib import admin
from django import forms
from django import template
from django.forms.util import ErrorList
from django.contrib.contenttypes import generic
from django.shortcuts import render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from lifestream.models import *
from lifestream.util import get_url_domain

import feedparser

class FeedCreationForm(forms.ModelForm):
    class Meta:
        model = Feed
        exclude = ['name', 'domain', 'fetchable']
  
    def clean(self):
        """
        Checks to make sure a feed url is valid and gets the feed title
        and domain.
        """
        feed_url = self.cleaned_data.get('url')
        if not feed_url:
            # Feed url was not validated by the field validator
            return
        feed = feedparser.parse(feed_url)
    
        # Check if the feed was not parsed correctly.
        if feed['bozo']:
            import logging

            self._errors['url'] = ErrorList(["This is not a valid feed: %s" % feed['bozo_exception']])
            logging.error(feed['bozo_exception'])
            # This field is no longer valid. Remove from cleaned_data
            del self.cleaned_data['url']
            return
        # Check if the feed has a title field
        feed_info = feed.get('feed')
        if not feed_info.get('title'):
            self._errors['url'] = ErrorList(["This is not a valid feed: The feed is empty"])
            # This field is no longer valid. Remove from cleaned_data
            del self.cleaned_data['url']
            return
        self.cleaned_data['name'] = feed_info['title']
        self.instance.name = self.cleaned_data['name']
        self.cleaned_data['domain'] = get_url_domain(feed_url)
        self.instance.domain = self.cleaned_data['domain']
        return self.cleaned_data

class FeedAdmin(admin.ModelAdmin):
    list_display    = ('name', 'domain', 'fetchable')
    list_filter     = ('domain',)
  
    add_form = FeedCreationForm
    model = Feed
  
    def add_view(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied
        if request.method == 'POST':
            form = self.add_form(request.POST)
            if form.is_valid():
                new_feed = form.save()
                msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': 'user', 'obj': new_feed}
                self.log_addition(request, new_feed)
                if "_addanother" in request.POST:
                    request.user.message_set.create(message=msg)
                    return HttpResponseRedirect(request.path)
                elif '_popup' in request.REQUEST:
                    return self.response_add(request, new_feed)
                else:
                    request.user.message_set.create(message=msg + ' ' + ugettext("You may edit it again below."))
                    # TODO: use reversed url
                    return HttpResponseRedirect('../%s/' % new_feed.id)
        else:
            form = self.add_form()
        return render_to_response('admin/lifestream/feed/add_form.html', {
            'title': _('Add feed'),
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_add_permission': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_file_field': False,
            'has_absolute_url': False,
            'auto_populated_fields': (),
            'opts': self.model._meta,
            'save_as': False,
            #'username_help_text': self.model._meta.get_field('username').help_text,
            'root_path': self.admin_site.root_path,
            'app_label': self.model._meta.app_label,            
        }, context_instance=template.RequestContext(request))

    def queryset(self, request):
        return self.model.objects.feeds()

admin.site.register(Feed, FeedAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display    = ('title', 'date','published')
    exclude         = ['clean_content',]
    list_filter     = ('feed',)
    search_fields   = ('title','clean_content')
    list_per_page   = 20
  
    model = Item
  
    def save_model(self, request, obj, form, change):
        obj.clean_content = strip_tags(obj.content)
        obj.save()

    def admin_update_feeds(self, request):
        from lifestream.feeds import update_feeds
        #TODO: Add better error handling
        update_feeds()
        return HttpResponseRedirect(
            reverse("admin:lifestream_item_changelist")
        )

    def get_urls(self):
        from django.conf.urls.defaults import *
        urls = super(ItemAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'update_feeds',
                self.admin_site.admin_view(self.admin_update_feeds),
                name='admin_update_feeds',
            ),
        )
        return my_urls + urls

admin.site.register(Item, ItemAdmin)
