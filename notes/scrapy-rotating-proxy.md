---
description: Дополнение scrapy для ротации прокси
tags: crawlers
title: Scrapy rotating proxy
---
[Usage](https://github.com/TeamHG-Memex/scrapy-rotating-proxies#usage)

```python
# in spider settings
ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt'

DOWNLOADER_MIDDLEWARES = {
    # ...
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # ...
}
```

[customisation](https://github.com/TeamHG-Memex/scrapy-rotating-proxies#customization): использование своих политик по проверке адресов вместо базового алгоритма rotating-proxy.

Настройки:

- `ROTATING_PROXY_LIST` - a list of proxies to choose from;
- `ROTATING_PROXY_LIST_PATH` - path to a file with a list of proxies;
- `ROTATING_PROXY_LOGSTATS_INTERVAL` - stats logging interval in seconds, 30 by default;
- `ROTATING_PROXY_CLOSE_SPIDER` - When True, spider is stopped if there are no alive proxies. If False (default), then when there is no alive proxies all dead proxies are re-checked.
- `ROTATING_PROXY_PAGE_RETRY_TIMES` - a number of times to retry downloading a page using a different proxy. After this amount of retries failure is considered a page failure, not a proxy failure. Think of it this way: every improperly detected ban cost you ROTATING_PROXY_PAGE_RETRY_TIMES alive proxies. Default: 5. It is possible to change this option per-request using max_proxies_to_try request.meta key - for example, you can use a higher value for certain pages if you're sure they should work.
- `ROTATING_PROXY_BACKOFF_BASE` - base backoff time, in seconds. Default is 300 (i.e. 5 min).
- `ROTATING_PROXY_BACKOFF_CAP` - backoff time cap, in seconds. Default is 3600 (i.e. 60 min).
- ROTATING_PROXY_BAN_POLICY - path to a ban detection policy. Default is 'rotating_proxies.policy.BanDetectionPolicy'.

Еще ссылки:

- [документация](https://github.com/TeamHG-Memex/scrapy-rotating-proxies)
- [[scrapy]]
- [[crawlers]]
- прокси можно [взять тут](https://github.com/scrapy-plugins/scrapy-zyte-smartproxy) (дорого)
- [how to rotate user-agent for request](https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/)





[scrapy]: scrapy "Scrapy"
[crawlers]: ../lists/crawlers "Crawlers"