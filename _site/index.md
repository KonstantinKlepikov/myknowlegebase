<p>На данном сайте собраны заметки по программированию, машинному обучению и алгоритмам, которые автор <a href="{{ site.github.owner_url }}">{{ site.github.owner_name }}</a> делал и продолжает делать в процессе обучения. Тысяча извинений за сумбурность записей, орфографию и изрядную долю копипасты. По сути это конспект. Более толковые статьи можно почитать в блоге <a href="https://konstantinklepikov.github.io/">my deep learning</a></p>
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
