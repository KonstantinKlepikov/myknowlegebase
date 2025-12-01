---
title: Несколько вопросов о реализации пауков в scrapy
description: Парсинг sitemap, фильтрацияи и способы обхода в scrapy
category: post
---
## Паук с парсингом sitemap и других страниц в [[scrapy]]

Самый простой сопособ получить такого паука - сделать дочерний класс из двух готовых.

```python
class WebCrawler(SitemapSpider, CrawlSpider):
    name = "flipkart"
    allowed_domains = ['flipkart.com']
    sitemap_urls = ['http://www.flipkart.com/robots.txt']
    sitemap_rules = [(regex('/(.*?)/p/(.*?)'), 'parse_product')]
    start_urls = ['http://www.flipkart.com/']
    rules = [
            Rule(LinkExtractor(
                allow=['/(.*?)/product-reviews/(.*?)']
                ), 'parse_reviews'),
            Rule(LinkExtractor(
                restrict_xpaths='//div[@class="fk-navigation fk-text-center tmargin10"]'
                ), follow=True)
            ]

    def parse_product(self, response):
        loader = FlipkartItemLoader(response=response)
        loader.add_value('pid', 'value of pid')
        loader.add_xpath('name', 'xpath to name')
        yield loader.load_item()

    def parse_reviews(self, response):
        loader = ReviewItemLoader(response=response)
        loader.add_value('pid','value of pid')
        loader.add_xpath('review_title', 'xpath to review title')
        loader.add_xpath('review_text', 'xpath to review text')
        yield loader.load_item()
```

[Пример со стековерфло](https://stackoverflow.com/questions/28797762/multiple-inheritance-in-scrapy-spiders)

Тут придется решить ряд проблем:

1. Основной интерфейс наследуется от [scrapy.spiders](https://docs.scrapy.org/en/latest/_modules/scrapy/spiders.html#Spider), обход по правилам от [scrapy.spiders.crawl](https://docs.scrapy.org/en/latest/_modules/scrapy/spiders/crawl.html#CrawlSpider), а парсинг сайтмапа от [scrapy.spiders.sitemap](https://docs.scrapy.org/en/latest/_modules/scrapy/spiders/sitemap.html#SitemapSpider) (последние два производные от первого)
2. Оба класса имеют разную реализациюб методов. К тому же sitemap сам по себе не поддерживате обход в глубину/ширину
3. возможно потребуется применить другой метод запроса страницы вместо [scrapy Request](https://docs.scrapy.org/en/latest/topics/request-response.html) - в этом случае надо переопределить метод `start_requests` из базового класа, прописав в нем правильно способ обработки стартовых урлов, добавив урлы из сайтмапа. Вот так он выглядит в дефолтном варианте:

    ```python
        def start_requests(self):
            cls = self.__class__
            if not self.start_urls and hasattr(self, 'start_url'):
                raise AttributeError(
                    "Crawling could not start: 'start_urls' not found "
                    "or empty (but found 'start_url' attribute instead, "
                    "did you miss an 's'?)")
            if method_is_overridden(cls, Spider, 'make_requests_from_url'):
                warnings.warn(
                    "Spider.make_requests_from_url method is deprecated; it "
                    "won't be called in future Scrapy releases. Please "
                    "override Spider.start_requests method instead "
                    f"(see {cls.__module__}.{cls.__name__}).",
                )
                for url in self.start_urls:
                    yield self.make_requests_from_url(url)
            else:
                for url in self.start_urls:
                    yield Request(url, dont_filter=True)
    ```

4. Переопределить способ обработки урлов и сайтмапа можно в методе `_parse_sitemap` класса sitemap. Здесь надо иметь ввиду, что класс `crawl` отправляет все обработанные на старте урлы в дефолтнгый метод `parse` или методs, определенный в rules. Есть смысл убрать прямые ссылки на колбеки и в обрабочике sitemap
5. Класс sitemap не поддерживает rules, поэтому для него придется как минимум сохранить атрибуты класса, задающие параметры обхода, такие как sitemap_urls, sitemap_rules, sitemap_follow, sitemap_alternate_links.
6. rules будет скомпилирован при создании инстанса и механизм его довольно сложный

Как реализовать правила показано [в этом примере](https://docs.scrapy.org/en/latest/topics/spiders.html#crawlspider-example). Здесь [находится описание апи](https://docs.scrapy.org/en/latest/topics/link-extractors.html?highlight=LinkExtractor#scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor) для динкэкстрактора.

## How does adding dont_filter=True argument in [[scrapy]]

В Scrapy, если установлен start_urls и опреден метод start_requests(), паук автоматически запрашивает URL-адреса и передает респонсы методу анализа, который является методом по умолчанию, используемым для анализа запросов.

Теперь можно получать отсюда новые запросы, которые снова будут анализироваться Scrapy. Scrapy имеет встроенный фильтр, который блокирует повторяющиеся запросы. То есть, если Scrapy уже просканировал сайт и проанализировал респонс, даже если будет отправлен другой запрос с таким же URL-адресом, scrapy не обработает его.

Чтобы избежать эту проблему в Request можно установить `dont_filter=True`, однако надо быть внимательным - это может провоцировать циклические обходы.

[Источник](https://stackoverflow.com/questions/38951878/how-does-adding-dont-filter-true-argument-in-scrapy-request-make-my-parsing-meth)

## Does Scrapy crawl in breadth-first or depth-first order

Дефолтно реализован стек (LIFO), иными словами обход осуществляется по Deep First Search. Если нужно реализовать BFS, то это можно сделать в сеттингсах вот так:

```python
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'
```

Пока ожидающие запросы находятся ниже настроенных значений CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN или CONCURRENT_REQUESTS_PER_IP, эти запросы отправляются одновременно. В результате первые несколько запросов сканирования редко следуют желаемому порядку. Снижение этих параметров до 1 обеспечивает желаемый порядок, но значительно замедляет сканирование в целом.

[Источник](https://doc.scrapy.org/en/latest/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order)

## scrapy "Missing scheme in request url"

Проблема в относительных ссылках. Восстановить ссылку можно с помощью `urlib.urljoin` или встроенног ометода scrapy Request

```python
next_url = response.urljoin(href)
```

[источник](https://stackoverflow.com/a/34979757/15966204)

## How to use not contains() in [[xpath]]

```shell
//production[not(contains(category,'Business'))]
```

[источник](https://stackoverflow.com/questions/11024080/how-to-use-not-contains-in-xpath)

## [[xpath]] with multiple contains on different elements

```shell
//person[contains(firstname, 'Kerr') and contains(lastname, 'och')]
```

[источник](https://stackoverflow.com/questions/18547410/xpath-with-multiple-contains-on-different-elements/18547533)

Смотри еще:

- [[crawlers]]
- [[scrapy]]
- [[xpath]]


[scrapy]: ../notes/scrapy "Scrapy"
[xpath]: ../notes/xpath "XPath в scrapy"
[crawlers]: ../lists/crawlers "Crawlers"


[scrapy]: ../notes/scrapy "Scrapy"
[scrapy]: ../notes/scrapy "Scrapy"
[xpath]: ../notes/xpath "XPath в scrapy"
[xpath]: ../notes/xpath "XPath в scrapy"
[crawlers]: ../lists/crawlers "Crawlers"
[scrapy]: ../notes/scrapy "Scrapy"
[xpath]: ../notes/xpath "XPath в scrapy"
