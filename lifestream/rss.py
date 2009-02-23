#!/usr/bin/env python
#:coding=utf-8:
#:mode=python:tabSize=2:indentSize=2:
#:noTabs=true:folding=explicit:collapseFolds=1:

# This file written by Ian Lewis (IanLewis@member.fsf.org)
# Copyright 2009 by Ian Lewis

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Optionally, you may find a copy of the GNU General Public License
# from http://www.fsf.org/copyleft/gpl.txt

from django.contrib.syndication.feeds import Feed as SyndicationFeed
from django.core.urlresolvers import reverse
from lifestream.models import *

class RecentItemsFeed(SyndicationFeed):
  title = "Recent Items"
  description = "Recent Lifestream Items"

  def link(obj):
    return reverse('main_page')

  def items(self):
    return Item.objects.published()[:10]
