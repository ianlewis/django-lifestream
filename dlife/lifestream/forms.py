#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

import time

from django import forms
from django.conf import settings
from django.forms.util import ErrorDict
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

from dlife.lifestream.models import COMMENT_MAX_LENGTH

class SecurityForm(forms.Form):
  """
  A form that has some extry security features such a hash to
  prevent Cross Site Request Forgery as well as checks against
  old timestamps and 
  """
  honeypot      = forms.CharField(required=False,
                                  label=_('If you enter anything in this field '\
                                          'your comment will be treated as spam'))
  timestamp     = forms.IntegerField(widget=forms.HiddenInput)
  security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)

  def __init__(self, data=None, initial=None):
    if initial is None:
      initial = {}
    initial.update(self.generate_security_data())
    super(SecurityForm, self).__init__(data=data, initial=initial)
  
  def security_errors(self):
    """Return just those errors associated with security"""
    errors = ErrorDict()
    for f in ["honeypot", "timestamp", "security_hash"]:
      if f in self.errors:
        errors[f] = self.errors[f]
    return errors

  def clean_honeypot(self):
    """Check that nothing's been entered into the honeypot."""
    value = self.cleaned_data["honeypot"]
    if value:
      raise forms.ValidationError(self.fields["honeypot"].label)
    return value

  def get_security_hash_dict(self):
    return {
      'timestamp' : self.data.get("timestamp", "")
    }

  def clean_security_hash(self):
    """Check the security hash."""
    security_hash_dict = self.get_security_hash_dict()
    expected_hash = self.generate_security_hash(**security_hash_dict)
    actual_hash = self.cleaned_data["security_hash"]
    if expected_hash != actual_hash:
      raise forms.ValidationError("Security hash check failed.")
    return actual_hash

  def clean_timestamp(self):
    """Make sure the timestamp isn't too far (> 2 hours) in the past."""
    ts = self.cleaned_data["timestamp"]
    if time.time() - ts > (2 * 60 * 60):
      raise forms.ValidationError("Timestamp check failed")
    return ts

  def generate_security_data(self):
    """Generate a dict of security data for "initial" data."""
    timestamp = int(time.time())
    security_dict =   {
      'timestamp'     : str(timestamp),
      'security_hash' : self.initial_security_hash(timestamp),
    }
    return security_dict

  def initial_security_hash(self, timestamp):
    """
    Generate the initial security hash from self.content_object
    and a (unix) timestamp.
    """

    initial_security_dict = {
      'timestamp' : str(timestamp),
    }
    return self.generate_security_hash(**initial_security_dict)

  def generate_security_hash(self, timestamp):
    """Generate a (SHA1) security hash from the provided info."""
    info = (timestamp, settings.SECRET_KEY)
    return sha_constructor("".join(info)).hexdigest()
    
class CommentForm(SecurityForm):
  user_name   = forms.CharField(_("User Name"))
  user_email  = forms.EmailField(label=_("Email Address"))
  user_url    = forms.URLField(label=_("URL"), required=False)
  content     = forms.CharField(_("Comment"), widget=forms.Textarea)