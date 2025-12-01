---
description: Извлечение данных из robots.txt в scrapy
tags: crawlers python
title: Parsing robots txt with scrapy
---
За проверку `robots.txt` в [[scrapy]] отвечает [встреонный middlewire](https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES), с самым высоким приоритетом

```python
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100, # here
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
```

Рекомендуется не влезать в эту часть, а управлять ею за счет [настройки параметров](https://docs.scrapy.org/en/latest/topics/settings.html#robotstxt-obey) и [парсера](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=robots#module-scrapy.downloadermiddlewares.robotstxt).

Исходный код обработчика `robots.txt` [находится тут](https://docs.scrapy.org/en/latest/_modules/scrapy/robotstxt.html): обработчик инициализирует класс и получает строки из `robots.txt`, после чего преобразует их в объект `RobotFileParser` из [urllib.robotparser](https://docs.python.org/3/library/urllib.robotparser.html), который хранить распарсенные данные и позволяет сравниваться с ними при проверке запрашиваемого урла в дальнейшем.

В `scrapy` реализовано несколько парсеров `robots.txt`:

- [Protego parser](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=robots#protego-parser) основан на пакете [protego](https://github.com/scrapy/protego) для парсинга в соответствии с [google спецификацией](https://developers.google.com/search/docs/advanced/robots/robots_txt)
- [RobotFileParser](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=robots#robotfileparser) совместимый с [Martijn Koster’s 1996 draft specification](https://www.robotstxt.org/norobots-rfc.txt) парсер
- [Reppy parser](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=robots#reppy-parser) python реализация парсера [reppy](https://github.com/seomoz/reppy/) для [c++ либы](https://github.com/seomoz/rep-cpp)
- [Robotexclusionrulesparser](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=robots#robotexclusionrulesparser) реализует вот [этот парсер](https://pypi.org/project/robotexclusionrulesparser/)

Два последних парсера так-же реализуют [Martijn Koster’s 1996 draft specification](https://www.robotstxt.org/norobots-rfc.txt)

Иногда нужно написать свой парсер (например когда необходимо сохзранять строки, содержащиеся в `robots.txt` или извдлекать и обрабатывать sitemap). Это можно сделать унаследовавшись от абстрактного базового класса [вот так](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=robots#implementing-support-for-a-new-parser)

Смотри еще:

- [[scrapy]]
- [[crawlers]]
- [Robots exclusion standard](https://en.wikipedia.org/wiki/Robots_exclusion_standard) (wiki)
- [Описание и настройка директивы Clean-param](https://vc.ru/seo/63058-opisanie-i-nastroyka-direktivy-clean-param) для `robots.txt`
- [google спецификацией](https://developers.google.com/search/docs/advanced/robots/robots_txt) для `robots.txt`
- [Martijn Koster’s 1996 draft specification](https://www.robotstxt.org/norobots-rfc.txt)
- [про файлы robots.txt у google](https://developers.google.com/search/docs/advanced/robots/intro?hl=ru)
- [[parsing-sitemap-with-scrapy]]
- [[urllibparse]]


[scrapy]: scrapy "Scrapy"
[crawlers]: ../lists/crawlers "Crawlers"
[parsing-sitemap-with-scrapy]: parsing-sitemap-with-scrapy "Parsing sitemap with scrapy"
[urllibparse]: urllibparse "Urllib.parse - парсинг урлов в компоненты"


[scrapy]: scrapy "Scrapy"
[scrapy]: scrapy "Scrapy"
[crawlers]: ../lists/crawlers "Crawlers"
[parsing-sitemap-with-scrapy]: parsing-sitemap-with-scrapy "Parsing sitemap with scrapy"
[urllibparse]: urllibparse "Urllib.parse - парсинг урлов в компоненты"
