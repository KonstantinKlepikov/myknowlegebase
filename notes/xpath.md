---
description: Язык выражений XQuery и Xpath в библиотеке scrapy
tags: crawlers
---
# XPath в scrapy

XPath — это язык выражений, который позволяет обрабатывать значения, соответствующие модели данных, определенной в XQuery и модели данных Xpath

[Ссылка на спецификацию](https://www.w3.org/TR/xpath/all/)

В [[scrapy]] используются два подхода - [[css-selectors]] и собственно xpath. Собственно обертка для обоих реализована через библиотеку [parsel](https://parsel.readthedocs.io/en/latest/index.html).

Данная статья будет связана с работай в xpath в [[scrapy]] на базе parsel.

[[scrapy]] оперирует селекторами, потому что они «выбирают» определенные части HTML-документа, заданные выражениями XPath или CSS. XPath — это язык для выбора узлов в XML-документах, который также можно использовать с HTML.

Типичный подход выглядит так:

```python
>>> response.xpath('//span/text()').get()
'good'
>>> response.css('span::text').get()
'good'
```

Селекторы scrapy реализованы через инстанцы класса [scrapy.selector.Selector](https://docs.scrapy.org/en/latest/topics/selectors.html#scrapy.selector.Selector) (или, когда нужно обработать список селекторов `scrapy.selector.SelectorList`). Практического смысла конструировать селекторы в ручную нет, так как объект `response` доступен через колбеки и имеет соответствующие методы `.css()` и `.xpath()`. Но, в любом случае можно и вручную

```python
>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse
>>> response = HtmlResponse(url='http://example.com', body=body)
>>> Selector(response=response).xpath('//span/text()').get()
'good'
```

**Классы предоставляют следующие методы:**

`xpath(xpath, namespaces=None, **kwargs)` находит узлы, соответствующие запросу xpath, и возвращает результат в виде экземпляра `SelectorList` со всеми сведенными элементами. Элементы возвращенного списка также реализуют интерфейс `Selector`.

- `query` - это строка с синтаксисом xpath запроса
- `namespaces` позволяет использовать собственные пространства имен (параметр не регистрируется для будущих вызовов - надо использовать особый метод для регистрации)
- `**kwargs` - дополнительные аргумсенты, котоыре могут быть переданы в выражение xpath во так

```python
>>> selector.xpath('//a[href=$url]', url="http://www.example.com")
```

`css(query)` применяет селектор CSS и возвращает экземпляр `SelectorList`

`get()` возвращает единственную строку, соответствующую запросу или `None`

```python
>>> response.css('title::text').get()
'Example website'
```

`attrib` возвращает словарь атрибутов для элемента

```python
>>> response.css('img').attrib['src']
'image1_thumb.jpg'
```

`re(regex, replace_entities=True)` применить регулярное выражение и вернуть список стрко с совпадениями. Или первое встреченное вот так: `re_first(regex, default=None, replace_entities=True)`

`register_namespace(prefix, uri)` позволяет зарегистрировать нестандартное пространство имен (это бывает важно, если реализуются узлы, не предусмотренные стандартной спецификацией). `remove_namespaces()` удаляет пространство имен.

`__bool__()` вернет `True` если в селекторе есть хоть что-то. Иначе `False`

`getall()` возвращает список соответствий запросу или пустой список

```python
>>> response.css('img').xpath('@src').getall()
['image1_thumb.jpg',
 'image2_thumb.jpg',
 'image3_thumb.jpg',
 'image4_thumb.jpg',
 'image5_thumb.jpg']
 ```

 Кроме того [поддерживаются методы](https://docs.scrapy.org/en/latest/topics/selectors.html#extract-and-extract-first) `extract()` и `extract_first()`, однако они устарели и предпочтительно использовать `get()` и `getall()`

 Пример использования xpath и селекторов в scrapy [смотри тут](https://docs.scrapy.org/en/latest/topics/selectors.html#id1)

```python
>>> sel = Selector(html_response)

>>> sel.xpath("//h1").getall()         # this includes the h1 tag
>>> sel.xpath("//h1/text()").getall()  # this excludes the h1 tag

>>> for node in sel.xpath("//p"):
...     print(node.attrib['class'])
```

Можно сотавлять [вложенные селекторы](https://docs.scrapy.org/en/latest/topics/selectors.html#nesting-selectors), так как `xpath()` и `css()` возвращают списки селекторов.

Выбор атрибутов осуществляется через нотацию `@`

```python
>>> response.xpath("//a/@href").getall()
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

Выбор css-селекторов через `::`

```python
>>> response.css('a::attr(href)').getall()
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

Кроме того можно использовать свойство `attrib` самого селектора

```python
>>> [a.attrib['href'] for a in response.css('a')]
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
```

Использование регулярок так-же не является сложной задачей:

```python
>>> response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')
['My image 1',
 'My image 2',
 'My image 3',
 'My image 4',
 'My image 5']
```

## [Особенности работы с xpath](https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths)

### Все селекторы на оснвое xpath отсчитываются от корня документа. Это надо иметь ввиду, когда извлекаются объекты с помощью вложенных селекторов

плохо

```python
divs = response.xpath('//div')
for p in divs.xpath('//p'):  # this is wrong - gets all <p> from the whole document
    print(p.get())
```

лучше

```python
for p in divs.xpath('.//p'):  # extracts all <p> inside
    print(p.get())
```

или

```python
for p in divs.xpath('p'):
    print(p.get())
```

### Выбирать элемент по классу можно разными способами, т.к. в [может быть много разных классов](https://docs.scrapy.org/en/latest/topics/selectors.html#when-querying-by-class-consider-using-css)

Можно использовать цепь селекторов

```python
from scrapy import Selector
sel = Selector(
    text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>'
    )
sel.css('.shout').xpath('./time/@datetime').getall()
['2014-07-23 19:00']
```

### [Beware of the difference](https://docs.scrapy.org/en/latest/topics/selectors.html#beware-of-the-difference-between-node-1-and-node-1) between //node\[1] and (//node)\[1]

### [Using text nodes in a condition](https://docs.scrapy.org/en/latest/topics/selectors.html#using-text-nodes-in-a-condition)

### [Variables in XPath expressions](https://docs.scrapy.org/en/latest/topics/selectors.html#variables-in-xpath-expressions)

### [Removing namespaces](https://docs.scrapy.org/en/latest/topics/selectors.html#removing-namespaces)

`Selector.remove_namespaces()` позволяет избавиться от пространства имен, чтобы оперировать более простыми понятиями

### [Using EXSLT extensions](https://docs.scrapy.org/en/latest/topics/selectors.html#using-exslt-extensions)

**Больше подробностей прои работу с xpath и селекторами можно найти смотри тут**:

- [подробное руководство по использованию селекторов и xpath в parsel](https://parsel.readthedocs.io/en/latest/usage.html#learning-css-and-xpath)
- [XPath/CSS Equivalents in Wikibooks](https://en.wikibooks.org/wiki/XPath/CSS_Equivalents)
- [Xpath cheatsheet](https://devhints.io/xpath)
- [XPath Tutorial](https://www.w3schools.com/xml/xpath_intro.asp) w3s

Еще ссылки:

- [[crawlers]]
- [[scrapy]]
- [[css-selectors]]
- [[2022-02-12-daily-note]] парсинг sitemap, фильтрацияи и способы обхода в scrapy
- [parsel](https://parsel.readthedocs.io/en/latest/index.html)

[//begin]: # "Autogenerated link references for markdown compatibility"
[scrapy]: scrapy "Scrapy"
[css-selectors]: css-selectors "Css-selectors"
[crawlers]: ../lists/crawlers "Crawlers"
[2022-02-12-daily-note]: ../posts/2022-02-12-daily-note "Y"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[scrapy]: scrapy "Scrapy"
[css-selectors]: css-selectors "Css-selectors"
[scrapy]: scrapy "Scrapy"
[scrapy]: scrapy "Scrapy"
[crawlers]: ../lists/crawlers "Crawlers"
[scrapy]: scrapy "Scrapy"
[css-selectors]: css-selectors "Css-selectors"
[2022-02-12-daily-note]: ../posts/2022-02-12-daily-note "Несколько вопросов о реализации пауков в scrapy"
[//end]: # "Autogenerated link references"