---
layout: page
title: Все посты
permalink: /allposts/
---

<div class="container mx-auto px-2 py-1">
{% for post in site.posts %}
    {% include allposts_block.html %}
{% endfor %}
</div>
{% include tagcloud.html %}