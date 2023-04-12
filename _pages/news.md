---
layout: page
permalink: /news/
title: News
description:
nav: false
nav_order: 3
---
 
  <div class="news">
    {% if site.news != blank -%} 
    {%- assign news_size = site.news | size -%}
    <div class="table-responsive" {% if site.news_scrollable and news_size > 3 %}style="max-height: 2000vw"{% endif %}>
      <table class="table table-sm table-borderless">
      {%- assign news = site.news | reverse -%}
      {% if site.news_limit %}
      {% assign news_limit = site.news_limit %}
      {% else %}
      {% assign news_limit = news_size %}
      {% endif %}
      {% for item in news limit: 1000 %} 
        <tr>
          <th scope="row">{{ item.date | date: "%b %-d, %Y" }}</th>
          <td style="text-align:justify">
            {% if item.inline -%} 
              {{ item.content | remove: '<p>' | remove: '</p>' | emojify }}
            {%- else -%} 
              <a class="news-title" href="{{ item.url | relative_url }}">{{ item.title }}</a>
            {%- endif %} 
          </td>
        </tr>
      {%- endfor %} 
      </table>
    </div>
  {%- else -%} 
    <p>No news so far...</p>
  {%- endif %} 
  </div>
