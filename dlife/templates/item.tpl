{% extends "base.tpl" %}
{% load truncate_chars %}
{% block title %}{{lifestream.ls_title}}{% endblock %}
{% block content %}
<h2><a href="{{item.item_permalink}}">{{ item.item_title }}</a></h2>
{{item.item_date}}
<p>
  {% if item.item_content %}
    {{ item.item_content|safe }}
  {% else %}
    &nbsp;
  {% endif %}
</p>
{% endblock %}