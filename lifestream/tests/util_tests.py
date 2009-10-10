#!/usr/bin/env python
#:coding=utf-8:

from django.test import TransactionTestCase as DjangoTestCase

from lifestream.util import * 

class TagStrippingTest(DjangoTestCase):
    valid_tags = VALID_TAGS
    test_html = (
        (u'<b>This is a test</b>', u'<b>This is a test</b>'),
        (u'<script type="text/javascript">alert("DANGER!!");</script> Will Robinson', u'alert(&quot;DANGER!!&quot;); Will Robinson'),
        (u'<a href="http://www.ianlewis.org/" rel="me" onclick="alert(\'woah!!\')">This is a test</a>', u'<a href="http://www.ianlewis.org/" rel="me">This is a test</a>'),
    )

    def test_tag_stripping(self):
        for html in self.test_html:
            stripped_html = sanitize_html(html[0], valid_tags=self.valid_tags)
            self.assertEqual(stripped_html, html[1])

    
