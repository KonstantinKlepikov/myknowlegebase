<div>
    <h2>Articles</h2>
    {% assign pages_list = site.pages | sort: 'title' %}
    {% for page in pages_list %}
        {% include allpages_block.html %}
    {% endfor %}
</div>

<div>
    <h2>Daily notes</h2>
    {% for post in site.posts %}
        {% include allposts_block.html %}
    {% endfor %}
</div>
