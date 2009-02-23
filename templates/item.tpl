{% extends "base.tpl" %}
{% load truncate_chars %}
{% load humanize %}
{% load i18n %}

{% block title %}{{lifestream.title}}{% endblock %}
{% block content %}
<h2><a href="{{item.permalink}}">{{ item.title }}</a></h2>
{{item.date}}
<p>
  {% if item.content %}
    {% ifequal item.content_type "text/plain"  %}
      {{ item.content|linebreaks }}
    {% else %}
      {% ifequal item.content_type "text/html"  %}
        {{ item.content|safe }}
      {% else %}
        {{ item.content }}
      {% endifequal %}
    {% endifequal %}
  {% else %}
    &nbsp;
  {% endif %}
  {% ifequal item.feed.feed_domain "api.flickr.com" %}
    <img src="{{ item.media_url }}" width="500" alt="{{ item.media_description|striptags }}" />
  {% endifequal %}
</p>

{% endblock %}
