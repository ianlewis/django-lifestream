#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.contrib.admin.views.decorators import staff_member_required
from dlife.lifestream.feeds import update_feeds
from django.http import HttpResponseRedirect

@staff_member_required
def admin_update_feeds(request):
  update_feeds()
  # TODO: fix this redirect
  return HttpResponseRedirect("/admin/lifestream/item/")