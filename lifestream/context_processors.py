#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.utils.translation import ugettext as _
from lifestream.models import Lifestream

def basic(request):
  return {
    'lifestream': request.lifestream
  }
