{% extends "base.tpl" %}
{% block title %}{{lifestream.ls_title}}{% endblock %}
{% block content %}
<table>
  <tbody>
    <tr>
     {% for item in items.object_list %}
      <td>
        <h2>{{ item.item_title }}</h2>
        {{ item.item_content }}
      </td>
      {% endfor %}
    </tr>
  <tbody>
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