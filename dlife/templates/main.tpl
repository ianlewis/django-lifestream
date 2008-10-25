{% extends "base.tpl" %}
{% load truncate_chars %}
{% block title %}{{lifestream.ls_title}}{% endblock %}
{% block content %}
<table>
  {% if items.object_list %}
  <tbody>
    {% for item in items.object_list %}
    <tr>
      <td>
        <h2><a href="{{item.item_permalink}}">{{ item.item_title }}</a></h2>
        {{item.item_date}}
        <p>{{ item.item_clean_content|truncate_chars:100 }}</p>
      </td>
    </tr>
    {% endfor %}
  <tbody>
  {% endif %}
</table>
<br/>
<div class="pagination">
  <span class="step-links">
    {% if items.has_previous %}
      <a href="?page={{ contacts.previous_page_number }}">Previous</a>
    {% endif %}

    <span class="current">
      Page {{ items.number }} of {{ items.paginator.num_pages }}.
    </span>

    {% if items.has_next %}
      <a href="?page={{ items.next_page_number }}">Next</a>
    {% endif %}
  </span>
</div>
{% endblock %}