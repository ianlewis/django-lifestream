#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from dlife.lifestream.models import *
from django.contrib import admin

admin.site.register(LifeStream)
admin.site.register(User)
admin.site.register(Feed)
admin.site.register(Item)
