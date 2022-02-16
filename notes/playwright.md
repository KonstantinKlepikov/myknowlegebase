---
description: Пакет для сквозного тестирования web-приложений
tags: crawlers
---
# Playwright

Playwright enables reliable end-to-end testing for modern web apps

Предоставляет два API - синхронный и асинхронный. Смотри [intro](https://playwright.dev/python/docs/intro)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://playwright.dev")
    print(page.title())
    browser.close()
```

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

Браузер запускается в headless режиме по дефолту. Как изменить [смотри тут](https://playwright.dev/python/docs/debug)

Важные особенности:

- необходимо использовать `page.wait_for_timeout(5000)` вместо `time.sleep(5)` и лучше вообще не ждать таймаута, но иногда это полезно для отладки. Это связано с тем, что playwright реализует асинхронные операции, и при использовании time.sleep(5) они не могут быть обработаны правильно.
- API Playwright не является потокобезопасным. Cледует создать экземпляр playwright для каждого потока.

Инструменты пакета:

- [inspector](https://playwright.dev/python/docs/inspector) это инструмент с графическим интерфейсом, который помогает создавать и отлаживать сценарии Playwright
- [Trace Viewer](https://playwright.dev/python/docs/trace-viewer) это инструмент с графическим интерфейсом, который помогает исследовать логи playwright после запуска сценария. Открывайте трассировки локально или в браузере на странице trace.playwright.dev
- [Test Generator](https://playwright.dev/python/docs/codegen) граф.интерфейс для генерации тестов на основе пользовательского приложения
- [Debugging tools](https://playwright.dev/python/docs/debug) playwright сценарии работают с существующими инструментами отладки, такими как отладчики Node.js и инструменты разработчика браузера. Playwright также представляет свои функции отладки для автоматизации браузера
- [Pytest plugin](https://playwright.dev/python/docs/test-runners)

## Функционал

### Autowaiting

Playwright позволяет выполнять ряд проверок работоспособности элементов, прежде чем предпринимает действия, чтобы убедиться, что эти действия приведут к ожидемым последствиям. Он автоматически ожидает прохождения всех соответствующих проверок и только после этого выполняет запрошенное действие. Если требуемые проверки не проходят в течение заданного времени ожидания, действие завершается с ошибкой `TimeoutError`.

Список доступных экшенов [тут](https://playwright.dev/python/docs/actionability)

### [API testing](https://playwright.dev/python/docs/api-testing)

- Test your server API.
- Prepare server side state before visiting the web application in a test.
- Validate server side post-conditions after running some actions in the browser.

### [Assertions](https://playwright.dev/python/docs/assertions)

Это API, предоставляющий различные элементы полученного контента для проверок в тестах

### [Authentication](https://playwright.dev/python/docs/auth)

Апи для автоматизации сценариев регистрации/авторизации

### [Browser Contexts](https://playwright.dev/python/docs/browser-contexts)

Поддерживаются изолированные контексты для бразуера. Каждый контекст существует только в рамках одной сесси. Можно реализовать несколько контекстов одновременно

### [Command line tools](https://playwright.dev/python/docs/cli)

### [Dialogs](https://playwright.dev/python/docs/dialogs)

Интерфейс для взаимодействия с диалоговыми окнами приложения

### [Downloads](https://playwright.dev/python/docs/downloads)

АПИ для загрузки файлов

### [Emulation](https://playwright.dev/python/docs/emulation)

Playwright позволяет переопределять различные параметры устройства, на котором запущен браузер:

- размер области просмотра
- коэффициент масштабирования устройства
- локаль поддержки сенсорного экрана
- геолокацию цветовой схемы часового пояса

### [Evaluating JavaScrip](https://playwright.dev/python/docs/evaluating)

Сценарии Playwright запускаются в изолированной среде Playwright. Скрипты страницы запускаются в среде страницы браузера. Эти среды не пересекаются, они работают на разных виртуальных машинах в разных процессах и даже потенциально на разных компьютерах.

API `page.evaluate(expression, **kwargs)` может запускать функцию JavaScript в контексте веб-страницы и возвращать результаты в среду Playwright. Глобальные переменные браузера, такие как окно и документ, могут использоваться в оценке.

### [Events](https://playwright.dev/python/docs/events)

- Waiting for event
- Adding/removing event listener
- Adding one-off listeners

### Playwright supports [custom selector engines](https://playwright.dev/python/docs/extensibility)

### [Frames](https://playwright.dev/python/docs/frames)

### [Handles](https://playwright.dev/python/docs/handles)

Можно создать дескрипторы для элементов страницы DOM или любых других объектов внутри страницы. Эти дескрипторы находятся в процессе Playwright, тогда как настоящие объекты находятся в браузере.

- JSHandle для ссылки на любые объекты JavaScript на странице.
- ElementHandle для ссылки на элементы DOM на странице, Можно ыполнять действия над элементами и утверждать их свойства.

### [Input](https://playwright.dev/python/docs/input)

- Text input
- Checkboxes and radio buttons
- Select options
- Mouse click
- Type characters
- Keys and shortcuts
- Upload files
- Focus element

### [Locators](https://playwright.dev/python/docs/locators)

### [Navigations](https://playwright.dev/python/docs/navigations)

Playwright может переходить по URL-адресам и обрабатывать переходы, вызванные взаимодействием со страницей.

### [Network](https://playwright.dev/python/docs/network)

- HTTP Authentication
- HTTP Proxy
- Network events
- Handle requests
- Modify requests
- Abort requests
- WebSockets

### [Pages](https://playwright.dev/python/docs/pages)

- Pages
- Multiple pages
- Handling new pages
- Handling popups

### [Page Object Models](https://playwright.dev/python/docs/pom)

Большие наборы тестов могут быть структурированы для упрощения разработки и обслуживания. Объектные модели страниц — один из таких подходов к структурированию набора тестов.

### [Screenshots](https://playwright.dev/python/docs/screenshots)

### [Selectors](https://playwright.dev/python/docs/selectors)

- Text selector
- CSS selector
- Selecting visible elements
- Selecting elements that contain other elements
- Selecting elements matching one of the conditions
- Selecting elements in Shadow DOM
- Selecting elements based on layout
- [[xpath]] selectors
- N-th element selector
- React selectors
- Vue selectors
- id, data-testid, data-test-id, data-test selectors
- Pick n-th match from the query result
- Chaining selectors

### [Logs](https://playwright.dev/python/docs/verification)

### [Videos](https://playwright.dev/python/docs/videos)

## scrapy-playwright

Playwright integration for [[scrapy]]. [На гитхабе](https://github.com/scrapy-plugins/scrapy-playwright)

Предоставляет Scrapy Download Handler, который выполняет запросы с помощью Playwright для Python. Его можно использовать для рендеринга страниц с JavaScript. Этот пакет не конфликтует с обычными рабочими процессами Scrapy, такими как планирование запросов или обработка элементов.

Ставится так:

1. `pip install scrapy-playwright`
2. заменить дефолтные хендлеры в `settings.py`

    ```python
    DOWNLOAD_HANDLERS = {
        "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    }
    ```

3. Установить [[asyncio]] [Twisted reactor](https://docs.scrapy.org/en/latest/topics/asyncio.html#installing-the-asyncio-reactor)

    ```python
    TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    ```

    Опция является экспериментальной для текущей (на момент написания заметки) реалитзации [[scrapy]]. Если используются `CrawlerRunner` надо дополнительно включить асинко вручную через `install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')`

Поддерживаемые опции:

- `PLAYWRIGHT_BROWSER_TYPE` (type str, default chromium) - chromium, firefox, webkit
- `PLAYWRIGHT_LAUNCH_OPTIONS` (type dict, default {}) лаунчопции браузера. [Подробнее тут](https://playwright.dev/python/docs/api/class-browsertype#)
- `PLAYWRIGHT_CONTEXTS` (type dict[str, dict], default {}) Словарь, который определяет контексты браузера, которые будут созданы при запуске. Если не определен - создается контекст по умолчанию.
- `PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT` (type Optional[float], default None) Время ожидания, используемое при запросе страниц Playwright. Если `None` или не установлено, будет использоваться значение по умолчанию (30000 мс)
- `PLAYWRIGHT_PROCESS_REQUEST_HEADERS` (type str, default scrapy_playwright.headers.use_scrapy_headers). Путь к функции сопрограммы, которая обрабатывает заголовки для данного запроса и возвращает словарь с заголовками, которые будут использоваться (в зависимости от браузера также будут отправлены дополнительные заголовки по умолчанию).

    Функция должна возвращать словарь и принимать следуюшие аргументы:
      - browser_type: str
      - playwright_request: playwright.async_api.Request
      - scrapy_headers: scrapy.http.headers.Headers

    Значение по умолчанию (`scrapy_playwright.headers.use_scrapy_headers`) пытается эмулировать поведение Scrapy для запросов навигации, т. е. переопределяет заголовки их значениями из запроса Scrapy. Для ненавигационных запросов (например, изображений, таблиц стилей, скриптов и т. д.) для согласованности переопределяется только заголовок User-Agent. Доступна еще одна функция: `scrapy_playwright.headers.use_playwright_headers`, которая вернет заголовки из запроса Playwright без каких-либо изменений.

Использование (через meta):

```python
import scrapy

class AwesomeSpider(scrapy.Spider):
    name = "awesome"

    def start_requests(self):
        # GET request
        yield scrapy.Request("https://httpbin.org/get", meta={"playwright": True})
        # POST request
        yield scrapy.FormRequest(
            url="https://httpbin.org/post",
            formdata={"foo": "bar"},
            meta={"playwright": True},
        )

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        yield {"url": response.url}
```

По умолчанию исходящие запросы включают User-Agent, установленный Scrapy (либо с настройками `USER_AGENT`, либо с настройками `DEFAULT_REQUEST_HEADERS`, либо с помощью атрибута `Request.headers`). Это может привести к неожиданной реакции некоторых сайтов, например, если пользовательский агент не соответствует работающему браузеру. Если вы предпочитаете, чтобы пользовательский агент отправлялся по умолчанию конкретным браузером, который вы используете, установите для пользовательского агента Scrapy значение `None`.

Указание значения, отличного от `False`, для метаключа `playwright_include_page` для запроса приведет к тому, что соответствующий объект `playwright.async_api.Page` будет доступен в метаключе `playwright_page` в обратном вызове запроса. Чтобы иметь возможность ожидать сопрограммы для предоставленного объекта `Page`, **обратный вызов должен быть определен как функция сопрограммы**.

```python
import scrapy
import playwright

class AwesomeSpiderWithPage(scrapy.Spider):
    name = "page"

    def start_requests(self):
        yield scrapy.Request(
            url="https://example.org",
            meta={"playwright": True, "playwright_include_page": True},
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        title = await page.title()  # "Example Domain"
        await page.close()
        return {"title": title}
```

- Во избежание проблем с памятью рекомендуется вручную закрыть страницу, ожидая сопрограмму `Page.close`.
- Любые сетевые операции, возникающие в результате ожидания сопрограммы для объекта `Page` (goto, go_back и т. д.), будут выполняться непосредственно Playwright, минуя рабочий процесс запроса Scrapy (планировщик, промежуточное ПО и т. д.).

Еще доступно:

- [Proxy support](https://github.com/scrapy-plugins/scrapy-playwright#proxy-support)
- [Multiple browser contexts](https://github.com/scrapy-plugins/scrapy-playwright#multiple-browser-contexts)
- [Page coroutines](https://github.com/scrapy-plugins/scrapy-playwright#page-coroutines)
- [Page events](https://github.com/scrapy-plugins/scrapy-playwright#page-events)

Смотри еще:

- [документация для python](https://playwright.dev/python/docs/intro). [На гитхаб](https://github.com/microsoft/playwright-python)
- [API reference](https://playwright.dev/python/docs/api/class-playwright)
- scrapy-playwright со [[scrapy]]
- [[crawlers]]
- [[splash]]
- [[selenium]]
- [[xpath]]
- [[asyncio]]
- [[тестирование]]

На playwright [построен браузер](https://github.com/MarketSquare/robotframework-browser) [robotframework](https://robotframework.org/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[xpath]: xpath "XPath в scrapy"
[scrapy]: scrapy "Scrapy"
[asyncio]: asyncio "Asyncio"
[crawlers]: ../lists/crawlers "Crawlers"
[splash]: splash "Splash"
[selenium]: selenium "Selenium"
[тестирование]: ../lists/тестирование "Основные принципы тестровния"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[xpath]: xpath "XPath в scrapy"
[scrapy]: scrapy "Scrapy"
[asyncio]: asyncio "Asyncio"
[scrapy]: scrapy "Scrapy"
[scrapy]: scrapy "Scrapy"
[crawlers]: ../lists/crawlers "Crawlers"
[splash]: splash "Splash"
[selenium]: selenium "Selenium"
[xpath]: xpath "XPath в scrapy"
[asyncio]: asyncio "Asyncio"
[тестирование]: ../lists/тестирование "Основные принципы тестровния"
[//end]: # "Autogenerated link references"