#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.utils.translation import ugettext as _
from dlife.lifestream.models import Lifestream

def basic(request):
  basic_data = {}
  url = request.path
  # user = users.get_current_user()
  # logged_in = False
  # if user:
  #   greeting['user'] = user
  #   greeting['welcome_text'] = _("Welcome, %(nick)s!") % {'nick': user.nickname()}
  #   greeting['login_url'] = users.create_logout_url("/")
  #   greeting['login_text'] = 'Sign out'
  #   logged_in = True
  # else:
  #   greeting['user'] = None
  #   greeting['welcome_text'] = _('Anonymous')
  #   greeting['login_url'] = users.create_login_url(url)
  #   greeting['login_text'] = 'Sign in or register'
  
  #There will only be a single lifestream right now.
  try:
    lifestream = Lifestream.objects.get(id=1)
  except Lifestream.DoesNotExist:
    lifestream = None
  
  return {
    'lifestream': lifestream
  }
