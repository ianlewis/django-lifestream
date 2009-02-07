{% extends "base.tpl" %}
{% load truncate_chars %}
{% load humanize %}
{% load i18n %}

{% block title %}{{lifestream.ls_title}}{% endblock %}
{% block content %}
<h2><a href="{{item.item_permalink}}">{{ item.item_title }}</a></h2>
{{item.item_date}}
<p>
  {% if item.item_content %}
    {% ifequal item.item_content_type "text/plain"  %}
      {{ item.item_content|linebreaks }}
    {% else %}
      {% ifequal item.item_content_type "text/html"  %}
        {{ item.item_content|safe }}
      {% else %}
        {{ item.item_content }}
      {% endifequal %}
    {% endifequal %}
  {% else %}
    &nbsp;
  {% endif %}
  {% ifequal item.item_feed.feed_domain "api.flickr.com" %}
    <img src="{{ item.item_media_url }}" width="500" alt="{{ item.media_description|striptags }}" />
  {% endifequal %}
</p>

{% endblock %}
