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
</p>

{% for comment in item_comments %}
<p>
<h4>{{ comment.date }} {% if comment.user_url %}<a href="{{ comment.user_url }}">{% endif %}{{ comment.user_name }}{% if comment.user_url %}</a>{% endif %}</h4>
{{ comment.content }}
</p>
{% endfor %}

<div class="comment-form">
<form action="{{ comment_form.action }}" method="{{ comment_form.method }}">
{% for field in comment_form %}
  {% if field.is_hidden %}
    {{ field }}
  {% else %}
    {% ifequal field.name "honeypot" %}
      <div style="display:none;"><input type="text" name="honeypot" id="id_honeypot" /></div>
    {% else %}
      <div class="form-row">
        <p>{{ field.label_tag }}</p>
        {% if field.errors %}<p>{{ field.errors }}</p>{% endif %}
        <p>{{ field }}</p>
      </div>
    {% endifequal %}
  {% endif %}
{% endfor %}
<p class="comment-submit"><input type="submit" name="submit" class="submit-post" value="{% trans "Post" %}" /></p>
</form>
</div>

{% endblock %}