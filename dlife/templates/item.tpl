{% extends "base.tpl" %}
{% load truncate_chars %}
{% load humanize %}
{% load comments %}

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
</p>

{% get_comment_list for item as comment_list %}
{% for comment in comment_list %}
<p>
<h4>{{ comment.submit_date }} {% if comment.user_url %}<a href="{{ comment.user_url }}">{% endif %}{{ comment.user_name }}{% if comment.user_url %}</a>{% endif %}</h4>
{{ comment.comment }}
</p>
{% endfor %}

{% render_comment_form for item %}

{% endblock %}