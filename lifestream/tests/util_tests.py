#!/usr/bin/env python
#:coding=utf-8:

from base import HTMLSanitizationTest

from lifestream.util import * 

class TagStrippingTest(HTMLSanitizationTest):
    test_html = (
        (
            u'<b>This is a test</b>', 
            u'<b>This is a test</b>',
        ),
        (
            u'<script type="text/javascript">alert("DANGER!!");</script> Will Robinson',
            u'alert(&quot;DANGER!!&quot;); Will Robinson',
        ),
        (
            u'<a href="http://www.ianlewis.org/" rel="me" onclick="alert(\'woah!!\')">This is a test</a>',
            u'<a href="http://www.ianlewis.org/" rel="me">This is a test</a>',
        ),
        (
            u'<CRazY>Crazy Text</crazy>',
            u'Crazy Text',
        )
    )

class EntitiesTest(HTMLSanitizationTest):
    test_html = (
        (
            u'<b>Ian\'s Homepage</b>', 
            u'<b>Ian&apos;s Homepage</b>',
        ),
        (
            u'"I CaN HaZ SoMe <TeXt"', u'&quot;I CaN HaZ SoMe &lt;TeXt&gt;&quot;',
        ),
    )
