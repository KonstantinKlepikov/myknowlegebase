---
description: Работа с jinja2 на python
tags: templating
title: Jinja2 python
---
{% raw %}

[Документация](https://jinja.palletsprojects.com/en/3.0.x/intro/#installation)

`$ pip install Jinja2`

Dependencies

`MarkupSafe` escapes untrusted input when rendering templates to avoid injection attacks.

Jinja uses a central object called the template `Environment.` Instances of this class are used to store the configuration and global objects, and are used to load templates from the file system or other locations. Even if you are creating templates from strings by using the constructor of Template class, an environment is created automatically for you, albeit a shared one.

```python
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("yourapp"),
    autoescape=select_autoescape()
)
```

Это создает окружение шаблона с лоадером, который ищет шаблоны внутри вашего пакета #python. [Другие лоадеры тоже доступны](https://jinja.palletsprojects.com/en/3.0.x/api/#loaders).

Чтобы загрузить шаблон из окружения, можно сделать так:

```python
template = env.get_template("mytemplate.html")
```

Для отрисовки с переменными используется метод render()

```python
print(template.render(the="variables", go="here"))
```

Все [подробности об АПИ читать тут](https://jinja.palletsprojects.com/en/3.0.x/api/#basics)

[Песочница](https://jinja.palletsprojects.com/en/3.0.x/sandbox/) позволяет работать с небезопасными данными

[Native Python Types](https://jinja.palletsprojects.com/en/3.0.x/nativetypes/) позволяет работать с нативным питоньим кодом в шаблонах. Бывает полезно при создании текстовых файлов.

## [Template Designer Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)

Jinja не требует специальных форматов для шаблона (это может быть простой текстовый файл) и может генерировать любые текст-бейсед форматы - HTML, XML, CSV, LaTeX, etc. Шаблон содержит переменные и выражения, которые подменяются, когда шаблон рендерится. Кроме того, шаблон может содержать теги для контроля логики шаблона.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Webpage</title>
</head>
<body>
    <ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
    </ul>

    <h1>My Webpage</h1>
    {{ a_variable }}

    {# a comment #}
</body>
</html>
```

Разработчик может использовать любой удобный ему синтаксис: `{`% foo %`}`,  `<% foo %>` и что-то похожее. Дефолтные разделители сконфигурированы так:

- `{`% ... %`}` for Statements
- `{{` ... `}}` for Expressions to print to the template output
- `{`# ... #`}` for Comments not included in the template output

### Переменные

```html
{{ foo.bar }}
{{ foo['bar'] }}
```

### Фильтры

Переменные могут быть изменеены фильтрами. Например это `{{` listx|join(', ') `}}` эквивалентно этому `(str.join(', ', listx))`

### Тесты

Используется для проверки переменных с помощью простых выражений

```html
{% if loop.index is divisibleby 3 %}
{% if loop.index is divisibleby(3) %}
```

[Список буилт-ин тестов](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-tests)

## Коментарии

```html
{# note: commented-out template because we no longer use this
    {% for user in users %}
        ...
    {% endfor %}
#}
```

## Контроль пробелов

При рендеринге выражения jinja заменяются на переносы строки. Также может быть сконфигурировано вырезать полностью код шаблона. Этим можно управлять вручную в коде шаблона с помощью знаков + и -

```html
<div>
        {%+ if something %}yay{% endif %}
</div>

<div>
    {% if something +%}
        yay
    {% endif %}
</div>

{% for item in seq -%}
    {{ item }}
{%- endfor %}
```

В первом случае в ручную добавляем, во втором вырезаем.

```html
>valid:
{%- if foo -%}...{% endif %}
invalid:
{% - if foo - %}...{% endif %}
```

## Пропуск символов внутри кода шаблона

`{{ '{{' }}` - одинарные ковычки. Для больших секций тег raw

```html
'{'% raw %'}'
    <ul>
    {% for item in seq %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
'{'% endraw %'}'
```

## [Line Statements](https://jinja.palletsprojects.com/en/3.0.x/templates/#line-statements)

Еще один вариант синтаксиса

```html
<ul>
# for item in seq
    <li>{{ item }}</li>
# endfor
</ul>

<ul>
{% for item in seq %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

## Наследование шаблонов

base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}{% endblock %} - My Webpage</title>
    {% endblock %}
</head>
<body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2008 by <a href="http://domain.invalid/">you</a>.
        {% endblock %}
    </div>
</body>
</html>
```

Блок `{`% block %`}` определяет филлер, который будет использоваться в унаследовавших шаблонах. Пример наследника:

```HTML
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style type="text/css">
        .important { color: #336699; }
    </style>
{% endblock %}
{% block content %}
    <h1>Index</h1>
    <p class="important">
      Welcome to my awesome homepage.
    </p>
{% endblock %}
```

`{`% extends "layout/default.html" %`}` определяет от кого наследуемся и его местоположение, например в данном случае из сабдиректории.

`{`% extends layout_template %`}` так тоже можно, если шаблон добавлен в окружение.

Тег `{`% block %`}` можно использовать множество раз с одинаковым именем в одном шаблоне. Если нужно использовать блок много раз, то можно вызвать его через self

```HTML
<title>{% block title %}{% endblock %}</title>
<h1>{{ self.title() }}</h1>
{% block body %}{% endblock %}
```

Чтобы отрендерить контент филлера из блока родителя, используйте super()

```HTML
{% block sidebar %}
    <h3>Table Of Contents</h3>
    ...
    {{ super() }}
{% endblock %}
```

При этом можно двигаться по дереву наследования, если у шаблонов есть сабродители.

```tmpl
# parent.tmpl
body: {% block body %}Hi from parent.{% endblock %}

# child.tmpl
{% extends "parent.tmpl" %}
{% block body %}Hi from child. {{ super() }}{% endblock %}

# grandchild1.tmpl
{% extends "child.tmpl" %}
{% block body %}Hi from grandchild1.{% endblock %}

# grandchild2.tmpl
{% extends "child.tmpl" %}
{% block body %}Hi from grandchild2. {{ super.super() }} {% endblock %}
```

Для удобства чтения шаблонов, jinja позволяет добавлять название тега в закрывающую часть

```HTML
{% block sidebar %}
    {% block inner_sidebar %}
        ...
    {% endblock inner_sidebar %}
{% endblock sidebar %}
```

`scoped` позволяет унаследовать переменные из сабблока

```HTML
{% for item in seq %}
    <li>{% block loop_item scoped %}{{ item }}{% endblock %}</li>
{% endfor %}
```

`required` блоки играют роль абстрактных классов. Они могут содержать только пробелы и коментарии, должны быть реализованы во всех дочерних шаблонах и могут быть переопределены. Он не будет рендерен напрямую - попытка отрендерить шаблон, содержащий required поднимет ошибку... отрендерится только дочерний

page.txt

```html
{% block body required %}{% endblock %}
```

issue.txt

```html
{% extends "page.txt" %}
```

bug_report.txt

```html
{% extends "issue.txt" %}
{% block body %}Provide steps to demonstrate the bug.{% endblock %}
```

## Пропуск HTML

Вручную `{{` user.username|e `}}` будут пропущены все переменные, содержащие >, <, &, or ". Автоматически [описано тут](https://jinja.palletsprojects.com/en/3.0.x/templates/#working-with-automatic-escaping)

## [Циклы](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-control-structures)

### FOR

По списку

```HTML
<h1>Members</h1>
<ul>
{% for user in users %}
  <li>{{ user.username|e }}</li>
{% endfor %}
</ul>
```

По словарю

```HTML
<dl>
{% for key, value in my_dict.items() %}
    <dt>{{ key|e }}</dt>
    <dd>{{ value|e }}</dd>
{% endfor %}
</dl>
```

По отсортированному словарю

```HTML
<dl>
{% for key, value in my_dict | dictsort %}
    <dt>{{ key|e }}</dt>
    <dd>{{ value|e }}</dd>
{% endfor %}
</dl>
```

Внутри цикла можно использовать специальные бултин-функции

- `loop.index` The current iteration of the loop. (1 indexed)
- `loop.index0` The current iteration of the loop. (0 indexed)
- `loop.revindex` The number of iterations from the end of the loop (1 indexed)
- `loop.revindex0` The number of iterations from the end of the loop (0 indexed)
- `loop.first` True if first iteration.
- `loop.last` True if last iteration.
- `loop.length` The number of items in the sequence.
- `loop.cycle` A helper function to cycle between a list of sequences. See the explanation below.
- `loop.depth` Indicates how deep in a recursive loop the rendering currently is. Starts at level 1
- `loop.depth0` Indicates how deep in a recursive loop the rendering currently is. Starts at level 0
- `loop.previtem` The item from the previous iteration of the loop. Undefined during the first iteration.
- `loop.nextitem` The item from the following iteration of the loop. Undefined during the last iteration.
- `loop.changed(*val)` True if previously called with a different value (or not called at all).

Вот так:

```html
{% for row in rows %}
    <li class="{{ loop.cycle('odd', 'even') }}">{{ row }}</li>
{% endfor %}
```

Выйти из цикла (в отличае от python, где есть break) нельзя! Можно только фильтровать по переменным цикла

```HTML
{% for user in users if not user.hidden %}
    <li>{{ user.username|e }}</li>
{% endfor %}
```

Можно использовать дефолтный блок, если "пусто"

```HTML
<ul>
{% for user in users %}
    <li>{{ user.username|e }}</li>
{% else %}
    <li><em>no users found</em></li>
{% endfor %}
</ul>
```

Доступны рекурсии

```HTML
<ul class="sitemap">
{%- for item in sitemap recursive %}
    <li><a href="{{ item.href|e }}">{{ item.title }}</a>
    {%- if item.children -%}
        <ul class="submenu">{{ loop(item.children) }}</ul>
    {%- endif %}</li>
{%- endfor %}
</ul>
```

### IF

```HTML
{% if kenny.sick %}
    Kenny is sick.
{% elif kenny.dead %}
    You killed Kenny!  You bastard!!!
{% else %}
    Kenny looks okay --- so far
{% endif %}
```

### [Macros](https://jinja.palletsprojects.com/en/3.0.x/templates/#macros)

```HTML
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{
        value|e }}" size="{{ size }}">
{%- endmacro %}
```

затем это может быть вызвано в шаблоне.

```HTML
<p>{{ input('username') }}</p>
<p>{{ input('password', type='password') }}</p>
```

### Filters

```HTML
{% filter upper %}
    This text becomes uppercase
{% endfilter %}
```

### Assignments

Внутри кода шаблона можно назначать значения переменным

```HTML
{% set navigation = [('index.html', 'Index'), ('about.html', 'About')] %}
{% set key, value = call_something() %}
```

При этом назначенные переменные не будут видны за пределами циклов if и for!!!

Допустимо присваивать блоки (так-же поддерживаются и фильтры)

```html
{% set navigation %}
    <li><a href="/">Index</a>
    <li><a href="/downloads">Downloads</a>
{% endset %}
```

### included

Ипользуется для включения шаблолна со всеми переменными. Можно игнорировать пропуски, чтобы не райзить ошибки.

```HTML
{% include 'header.html' %}
    Body
{% include 'footer.html' %}
```

```HTML
{% include "sidebar.html" ignore missing %}
{% include "sidebar.html" ignore missing with context %}
{% include "sidebar.html" ignore missing without context %}
```

```HTML
{% include ['page_detailed.html', 'page.html'] %}
{% include ['special_sidebar.html', 'sidebar.html'] ignore missing %}
```

### [Import](https://jinja.palletsprojects.com/en/3.0.x/templates/#import)

Поддерживаются импорты внутри макросов и импорты from ... import ... as ...

```HTML
{% from 'forms.html' import input with context %}
{% include 'header.html' without context %}
```

## Выражения

### Литералы

"Hello World"

42 / 123_456

*The ‘_’ character can be used to separate groups for legibility.

42.23 / 42.1e2 / 123_456.789

['list', 'of', 'objects']

```HTML
<ul>
{% for href, caption in [('index.html', 'Index'), ('about.html', 'About'),
                         ('downloads.html', 'Downloads')] %}
    <li><a href="{{ href }}">{{ caption }}</a></li>
{% endfor %}
</ul>
```

('tuple', 'of', 'values')

{'dict': 'of', 'key': 'and', 'value': 'pairs'}

true / false / none *different with #python - lower letters

### Математика

```html
+ - / // % * **
```

{{ 11 % 7 }}

### Сравнения

`==` `!=` `>` `>=` `<=` `<`

### Логика

and or nit (expr) *группа параметров выражения

Можно использовать для for, if

The `is` and `in` operators support negation using an infix notation, too: foo is not bar and foo not in bar instead of not foo is bar and not foo in bar. All other expressions require a prefix notation: not (foo and bar)

Другие опреаторы

`in` Perform a sequence / mapping containment test. Returns true if the left operand is contained in the right. {{ 1 in [1, 2, 3] }} would, for example, return true.

`is` Performs a test.

`|` (pipe, vertical bar) Applies a filter.

`~` (tilde)
Converts all operands into strings and concatenates them.

`{{ "Hello " ~ name ~ "!" }}` would return (assuming name is set to 'John') Hello John!.

`()` Call a callable: {{ post.render() }}. Inside of the parentheses you can use positional arguments and keyword arguments like in Python:

{{ post.render(user, full=true) }}.

`. / []` Get an attribute of an object.

### If

Можно так

`{`% extends layout_template if layout_template is defined else 'default.html' %`}`

\<do something> if \<something is true> else \<do something else>

### Методы python

```html
{{ page.title.capitalize() }}
{{ f.bar(value) }}
{{ "Hello, %s!" % name }}
{{ "Hello, {}!".format(name) }}
```

Доступно

- abs()
- float()
- lower()
- round()
- tojson()
- attr()
- forceescape()
- map()
- safe()
- trim()
- batch()
- format()
- max()
- select()
- truncate()
- capitalize()
- groupby()
- min()\
- selectattr()
- unique()
- center()
- indent()
- pprint()
- slice()
- upper()
- default()
- int()
- random()
- sort()
- urlencode()
- dictsort()
- join()
- reject()
- string()
- urlize()
- escape()
- last()
- rejectattr()
- striptags()
- wordcount()
- filesizeformat()
- length()
- replace()
- sum()
- wordwrap()
- first()
- list()
- reverse()
- title()
- xmlattr()

[Подробнее](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-builtin-filters)

### Буилд-ин тестирующие ф-и

- boolean()
- even()
- in()
- mapping()
- sequence()
- callable()
- false()
- integer()
- ne()
- string()
- defined()
- filter()
- iterable()
- none()
- test()
- divisibleby()
- float()
- le()
- number()
- true()
- eq()
- ge()
- lower()
- odd()
- undefined()
- escaped()
- gt()
- lt()
- sameas()
- upper()

[Подробнее](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-builtin-tests)

### [Глобальные функции](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-global-functions)

Доступны в глобальном контексте, не только в циклах.

## Дополнения

- [разметка переводимого текста](https://jinja.palletsprojects.com/en/3.0.x/extensions/#i18n-extension)
- [loop control](https://jinja.palletsprojects.com/en/3.0.x/extensions/#loopcontrols-extension) - брейки и континью в циклах

```HTML
{% for user in users %}
    {%- if loop.index is even %}{% continue %}{% endif %}
    ...
{% endfor %}

{% for user in users %}
    {%- if loop.index >= 10 %}{% break %}{% endif %}
{%- endfor %}
```

- [Debug Extension](https://jinja.palletsprojects.com/en/3.0.x/templates/#debug-statement)
- [With Statement](https://jinja.palletsprojects.com/en/3.0.x/templates/#with-statement)
- [Autoescape Overrides](https://jinja.palletsprojects.com/en/3.0.x/templates/#autoescape-overrides)

Дополнения можно написать самостоятельно. [Пример](https://jinja.palletsprojects.com/en/3.0.x/extensions/#module-jinja2.ext)

## [Немного трюков jinja](https://jinja.palletsprojects.com/en/3.0.x/tricks/#null-default-fallback)

## [faq](https://jinja.palletsprojects.com/en/3.0.x/tricks/#null-default-fallback)

{% endraw %}

[[шаблонизаторы]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[шаблонизаторы]: ..%2Flists%2F%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80%D1%8B "Шаблонизаторы"
[//end]: # "Autogenerated link references"