#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from dlife.lifestream.models import *
from django.contrib import admin

admin.site.register(Lifestream)
admin.site.register(Feed)

class ItemAdmin(admin.ModelAdmin):
  list_display    = ('item_title', 'item_date')
  exclude         = ['item_clean_content',]
  list_filter     = ('item_feed',)
  search_fields   = ('item_title','item_clean_content')

admin.site.register(Item, ItemAdmin)

class TagAdmin(admin.ModelAdmin):
  list_display   = ('tag_name', 'tag_count')
  ordering       = ('-tag_count',)
  search_fields  = ('tag_name',)

admin.site.register(Tag, TagAdmin)