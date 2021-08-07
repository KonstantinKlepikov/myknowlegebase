<div>
    {% assign pages_list = site.pages | sort: 'title' %}
    {% for page in pages_list %}
    {% include allpages_block.html %}
    {% endfor %}
</div>
