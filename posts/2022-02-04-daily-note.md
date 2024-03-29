---
title: Работа в selenium с firefox
description: Несколько заметок о том, как запускать firefox в selenium
category: post
---
## How to make Firefox headless programmatically in [[selenium]] with Python

```python
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class WebDriver:
    """Selenium webdriver context manager
    """
    def __init__(self, driver: webdriver.Firefox):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


service = webdriver.firefox.service.Service(
    os.path.abspath('./src/geckodriver'),
    port=8081,
    )

options = Options()
options.add_argument("--headless")
options.add_argument('window-size=2500x1440')

with WebDriver(webdriver.Firefox(service=service, options=options)) as driver:
    # do something
```

[источник на оверфло](https://stackoverflow.com/questions/46753393/how-to-make-firefox-headless-programmatically-in-selenium-with-python)

## Unexpected keyword argument 'firefox_options' error

```python
TypeError: WebDriver.__init__() got an unexpected keyword argument 'firefox_options' error using firefox_options as arguments in Selenium Python
```

Параметр firefox_options для депрекейтет начиная с Selenium 3.8.0. Вместо этого надо использовать `selenium.webdriver.firefox.options.Options` (смотри пример выше)

## Несколько тематических статей по [[selenium]]

- [Web Scraping with Selenium in Python](https://www.zenrows.com/blog/web-scraping-with-selenium-in-python#getting-started). В статье разбирается ожидание загрузки элементов, клик по эоементам, кастомные заголовки и блокирование запросов.
- [Mastering Web Scraping in Python: Avoid Detection Like a Ninja](https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#behavioral-patterns) в статье пример кастомных заголовков

Смотри еще:

- [[selenium]]
- [[crawlers]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[selenium]: ../notes/selenium "Selenium"
[crawlers]: ../lists/crawlers "Crawlers"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[selenium]: ../notes/selenium "Selenium"
[selenium]: ../notes/selenium "Selenium"
[selenium]: ../notes/selenium "Selenium"
[crawlers]: ../lists/crawlers "Crawlers"
[//end]: # "Autogenerated link references"