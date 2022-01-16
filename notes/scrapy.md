---
description: Высокоуровневый фреймворк для web-скрапинга и краулинга на python
tags: crawlers
---
# Scrapy

Scrapy - это dысокоуровневый fcby[hjyysq фреймворк для web-скрапинга и краулинга на python

Создание проекта: `scrapy startproject proj_name`

Результат:

```shell
proj_name/
    scrapy.cfg            # deploy configuration file

    proj_name/            # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

Краулер можно создать, наслудуясь от класса `Spider` в spiders/

```python
from scrapy import Spider


class QuotesSpider(Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
```

АПИ scrapy активно использует колбеки (смотри [[python-glossary]]). `parse()` метод будет вызываться для обработки каждого запроса URL-адресов, даже если мы явно не указали Scrapy делать это. Это происходит потому, что `parse()` это колбек по умолчанию, который вызывается для запросов без явно назначенного обратного вызова.

`name` и `start_urls` это определенные в АПИ дефолтные атрибуты класса. `start_urls` это аналог вот этого:

```python
def start_requests(self):
    urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]
    for url in urls:
        yield scrapy.Request(url=url, callback=self.parse)
```

В АПИ scrapy использщуются генераторы. За счет конструкции `yield` обеспечивается большинство операций извлечения контента из запросов, а за счет колбеков - вызов, в том числе рекурсивный, необходимых операций.

В библиотеке реализован [собственный шел](https://docs.scrapy.org/en/latest/topics/shell.html#topics-shell), с помощью которого можно попробовать запросы или извлечение данных из объектов запроса, а так-же можно выполнить дебагинг. Пример ниже:

```shell
scrapy shell 'http://quotes.toscrape.com/page/1/'

2022-01-16 01:35:35 [scrapy.utils.log] INFO: Scrapy 2.5.1 started (bot: scrapybot)
2022-01-16 01:35:35 [scrapy.utils.log] INFO: Versions: lxml 4.7.1.0, libxml2 2.9.12, cssselect 1.1.0, parsel 1.6.0, w3lib 1.22.0, Twisted 21.7.0, Python 3.8.10 (default, Jun  2 2021, 10:49:15) - [GCC 10.3.0], pyOpenSSL 21.0.0 (OpenSSL 1.1.1m  14 Dec 2021), cryptography 36.0.1, Platform Linux-5.8.0-7630-generic-x86_64-with-glibc2.32
2022-01-16 01:35:35 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.epollreactor.EPollReactor
2022-01-16 01:35:35 [scrapy.crawler] INFO: Overridden settings:
{'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
 'LOGSTATS_INTERVAL': 0}
2022-01-16 01:35:35 [scrapy.extensions.telnet] INFO: Telnet Password: a6f662f302955377
2022-01-16 01:35:35 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.memusage.MemoryUsage']
2022-01-16 01:35:35 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2022-01-16 01:35:35 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2022-01-16 01:35:35 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2022-01-16 01:35:35 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2022-01-16 01:35:35 [scrapy.core.engine] INFO: Spider opened
2022-01-16 01:35:36 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
2022-01-16 01:35:36 [asyncio] DEBUG: Using selector: EpollSelector
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7ff2693c20a0>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x7ff2693c0d90>
[s]   spider     <DefaultSpider 'default' at 0x7ff269178dc0>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects 
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
2022-01-16 01:35:36 [asyncio] DEBUG: Using selector: EpollSelector
In [1]: 
```

Для разбора html используются [[css-selectors]] и [[xpath]]. При этом CSS позволяет реализовать навигацию по html, а XPath более функциональный разбор ( а именно извлечение контента). Фактически CSS транслируется в XPath.

Пример извлечения данных с помощью селекторов:

```python
from scrapy import Spider


class QuotesSpider(Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
```

Результат:

```shell
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from 
<200 http://quotes.toscrape.com/page/1/>
{'tags': ['life', 'love'], 'author': 'André Gide', 
'text': '“It is better to be hated for what you are than to be loved for what you are not.”'}
2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from 
<200 http://quotes.toscrape.com/page/1/>
{'tags': ['edison', 'failure', 'inspirational', 'paraphrased'], 'author': 'Thomas A. Edison', 
'text': "“I have not failed. I've just found 10,000 ways that won't work.”"}
```

Сохранение данных реализовано через [Item Pipline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html#topics-item-pipeline). Можно сохранять в `.json` или в базы данных, сохранять файлы или делать скриншоты. Особых огранисений нет, в основном используется для:

- очистка HTML-данных
- проверка очищенных данных (проверка того, что элементы содержат определенные поля)
- проверка на наличие дубликатов (и удаление их)
- сохранение очищенных элементов в базе данных или в виде файлов

Пример сохранения в MongoDB:

```python
import pymongo
from itemadapter import ItemAdapter

class MongoPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
```

Рекурсивный обход реализуется через колбеки. Пример:

```python
from scrapy import Spider


class AuthorSpider(Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
```

Этот паук запустится с главной страницы, он будет переходить по всем ссылкам на страницы авторов, вызывая `parse_author` для каждого из них, а также ссылки пагинации с `parse` рекурсивно. В данном примере реализован шаблон запроса по селектору `extract_with_css` а колбеки мы передаем в качестве аргументов в `response.follow_all()`.

Scrapy самостоятельно отфильтровывает повторяющиеся запросы к уже посещенным страницам (это можно настроить отдельно).

## Архитектура

![Scrapy architecture](../attachments/2022-01-16-02-10-33.png)

1. Engine получает первоначальные запросы на сканирование от Spider
2. Engine планирует запросы в Scheduler и запрашивает следующие запросы для сканирования
3. Scheduler возвращает следующие запросы движку
4. Engine отправляет запросы Downloader, проходя через ПО промежуточного слоя Downloader
5. Как только страница завершает загрузку, Downloader генерирует ответ (с этой страницей) и отправляет его в Engine, проходя через промежуточный смлой Downloader
6. Engine получает ответ от Downloader и отправляет его Spider для обработки, проходя через промежуточное слой Spider
7. Spider обрабатывает ответ и возвращает очищенные элементы и новые запросы в Engine, проходя через промежуточный слой Spider
8. Engine отправляет обработанные элементы в Item Pipelines, затем отправляет обработанные запросы планировщику и запрашивает возможные следующие запросы для сканирования.
9. Процесс повторяется (с шага 1) до тех пор, пока не закончатся запросы от Scheduler

Engine отвечает за управление потоком данных между всеми компонентами системы и инициирование событий при выполнении определенных действий

Scheduler получает запросы от движка и ставит их в очередь для передачи позже (также в движок), когда движок их запрашивает

Downloader отвечает за получение веб-страниц и передачу их движку, который, в свою очередь, передает их в Spiders

Spiders — это настраиваемые классы, написанные пользователями Scrapy для анализа ответов и извлечения из них элементов или дополнительных запросов

Item Pipelines отвечает за обработку элементов после их извлечения (или очистки) пауками. Типичные задачи включают очистку, проверку и сохранение (например, сохранение элемента в базе данных)

Промежуточный слой Downloader — это специальные перехватчики, которые находятся между движком и загрузчиком и обрабатывают запросы, когда они передаются от движка к загрузчику, и ответы, которые передаются от загрузчика к движку. Их надо использовать для следующих задач:

- обрабатывать запрос непосредственно перед его отправкой загрузчику (т. е. прямо перед тем, как Scrapy отправит запрос на веб-сайт)
- изменить полученный ответ перед передачей его пауку
- отправить новый запрос вместо передачи полученного ответа пауку
- передать ответ пауку, не загружая веб-страницу
- отбрасывать некоторые запросы

Промежуточный слой Spider — это специальные хуки, которые находятся между движком и пауками и могут обрабатывать ввод (ответы) и вывод паука (элементы и запросы). Их надо использовать для следующих задач:

- постобработка колбеков паука - изменение/добавление/удаление запросов или элементов
- постобработка start_requests
- обрабатывать исключения пауков
- вызывать errback вместо обратного вызова для некоторых запросов на основе содержимого ответа

Network для скрапи написан на [Twisted](https://twistedmatrix.com/trac/), таким образом он является асинхронным (см. [[asyncio]])

Ссылки на оригинальный материал: [один](https://docs.scrapy.org/en/latest/intro/tutorial.html), [два](https://docs.scrapy.org/en/latest/topics/architecture.html)

[Документация](https://docs.scrapy.org/en/latest/index.html)

Смотри еще:

- [[crawlers]]
- [[selenium]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-glossary]: python-glossary "Python glossary"
[css-selectors]: css-selectors "Css-selectors"
[xpath]: xpath "XPath"
[asyncio]: asyncio "Asyncio"
[crawlers]: ../lists/crawlers "Crawlers"
[selenium]: selenium "Selenium"
[//end]: # "Autogenerated link references"