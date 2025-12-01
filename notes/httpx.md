---
description: Sync and async HTTP 1/2 Client for Python3
tags: http asyncio python
title: httpx cинхронный и асинхронный http-клиент
---
HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

`pip install httpx`

```python
>>> import httpx
>>> r = httpx.get('https://www.example.org/')
>>> r
<Response [200 OK]>
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=UTF-8'
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

## Фичи

- Широко совместимый с [[requests]] API.
- Стандартный синхронный интерфейс, но с поддержкой асинхронности.
- Поддержка HTTP/1.1 и HTTP/2.
- Возможность делать запросы непосредственно к приложениям WSGI или приложениям ASGI
- Везде строгие тайм-ауты.
- Полностью анотирован.
- 100% покрытие тестами.

Плюс все стандартные возможности запросов:

- Международные домены и URL-адреса
- Keep-Alive и пул соединений
- Сеансы с сохраняемостью файлов cookie
- Проверка SSL в браузер-стиле
- Basic/Digest аутентификация
- Элегантные Key/Value cookie
- Автоматическая декомпрессия
- Автоматическое декодирование контента
- Тело ответа в Unicode
- Загрузка multipart file
- Поддержка прокси-серверов HTTP(S)
- Тайм-ауты подключения
- Потоковые загрузки
- Поддержка .netrc
- Разделенные (chunked) запросы

## Зависимости

- `httpcore` - The underlying transport implementation for httpx.
- `h11` - HTTP/1.1 support.
- `certifi` - SSL certificates.
- `rfc3986` - URL parsing & normalization.
- `idna` - Internationalized domain name support.
- `sniffio` - Async library autodetection.

Дополнительно:

- `h2` - HTTP/2 support. (Optional, with `httpx[http2]`)
- `socksio` - SOCKS proxy support. (Optional, with `httpx[socks]`)
- `rich` - Rich terminal support. (Optional, with `httpx[cli]`)
- `click` - Command line client support. (Optional, with `httpx[cli]`)
- `brotli` or `brotlicffi` - Decoding for "brotli" compressed responses. (Optional, with `httpx[brotli]`)

## [BasicUsage](https://www.python-httpx.org/quickstart/)

```python
>>> import httpx

>>> r = httpx.get('https://httpbin.org/get')
>>> r
<Response [200 OK]>

>>> r = httpx.put('https://httpbin.org/put', data={'key': 'value'})
>>> r = httpx.delete('https://httpbin.org/delete')
>>> r = httpx.head('https://httpbin.org/get')
>>> r = httpx.options('https://httpbin.org/get')

# To include URL query parameters in the request,
# use the params keyword
>>> params = {'key1': 'value1', 'key2': 'value2'}
>>> r = httpx.get('https://httpbin.org/get', params=params)

>>> r.url
URL('https://httpbin.org/get?key2=value2&key1=value1')

# list of items as a value
>>> params = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = httpx.get('https://httpbin.org/get', params=params)
>>> r.url
URL('https://httpbin.org/get?key1=value1&key2=value2&key2=value3')

# HTTPX will automatically handle decoding the response
# content into Unicode text
>>> r = httpx.get('https://www.example.org/')
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'

>>> r.encoding
'UTF-8'

# response may not contain an explicit encoding, in which case
# HTTPX will attempt to automatically determine an encoding to use
>>> r.encoding
None
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'

# verride
>>> r.encoding = 'ISO-8859-1'

# binary content
>>> r.content
b'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'

# json content
>>> r = httpx.get('https://api.github.com/events')
>>> r.json()
[{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...' ...  }}]

# custom headers
>>> url = 'https://httpbin.org/headers'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> r = httpx.get(url, headers=headers)

# Sending Form Encoded Data example

>>> data = {'key1': 'value1', 'key2': ['value1', 'value2']}
>>> r = httpx.post("https://httpbin.org/post", data=data)
>>> print(r.text)
{
  ...
  "form": {
    "key2": "value2",
    "key1": [
      "value1",
      "value2"
    ],
  },
  ...
}

# send json encoded data
>>> data = {'integer': 123, 'boolean': True, 'list': ['a', 'b', 'c']}
>>> r = httpx.post("https://httpbin.org/post", json=data)
>>> print(r.text)
{
  ...
  "json": {
    "boolean": true,
    "integer": 123,
    "list": [
      "a",
      "b",
      "c"
    ]
  },
  ...
}

# Sending Multipart File Uploads
>>> files = {'upload-file': open('report.xls', 'rb')}
>>> r = httpx.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {
    "upload-file": "<... binary content ...>"
  },
  ...
}

# Sending Binary Request Data
>>> content = b'Hello, world'
>>> r = httpx.post("https://httpbin.org/post", content=content)

# Responses
>>> r = httpx.get('https://httpbin.org/get')
>>> r.status_code
200

>>> r.status_code == httpx.codes.OK
True

# We can raise an exception for any responses which are not a 2xx success code
>>> not_found = httpx.get('https://httpbin.org/status/404')
>>> not_found.status_code
404
>>> not_found.raise_for_status()
Traceback (most recent call last):
  File "/Users/tomchristie/GitHub/encode/httpcore/httpx/models.py", line 837, in raise_for_status
    raise HTTPStatusError(message, response=self)
httpx._exceptions.HTTPStatusError: 404 Client Error: Not Found for url: https://httpbin.org/status/404
For more information check: https://httpstatuses.com/404

>>> r.headers
Headers({
    'content-encoding': 'gzip',
    'transfer-encoding': 'chunked',
    'connection': 'close',
    'server': 'nginx/1.0.4',
    'x-runtime': '148ms',
    'etag': '"e1ca502697e5c9317743dc078f67693f"',
    'content-type': 'application/json'
})

>>> r.headers['Content-Type']
'application/json'

>>> r.headers.get('content-type')
'application/json'

# For large downloads you may want to use streaming responses that do not load the entire response body into memory at once.

# binary
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for data in r.iter_bytes():
...         print(data)

# text
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for text in r.iter_text():
...         print(text)

# or text line by line
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for line in r.iter_lines():
...         print(line)

# or raw without decoding
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for chunk in r.iter_raw():
...         print(chunk)

# Cookies
>>> r = httpx.get('https://httpbin.org/cookies/set?chocolate=chip')
>>> r.cookies['chocolate']
'chip'

>>> r = httpx.get('https://httpbin.org/cookies', cookies=cookies)
>>> r.json()
{'cookies': {'peanut': 'butter'}}

>>> cookies = httpx.Cookies()
>>> cookies.set('cookie_on_domain', 'hello, there!', domain='httpbin.org')
>>> cookies.set('cookie_off_domain', 'nope.', domain='example.org')
>>> r = httpx.get('http://httpbin.org/cookies', cookies=cookies)
>>> r.json()
{'cookies': {'cookie_on_domain': 'hello, there!'}}

# Redirection and hystory
>>> r = httpx.get('http://github.com/')
>>> r.status_code
301
>>> r.history
[]
>>> r.next_request
<Request('GET', 'https://github.com/')>

# You can modify the default redirection handling with
# the follow_redirects parameter
>>> r = httpx.get('http://github.com/', follow_redirects=True)
>>> r.url
URL('https://github.com/')
>>> r.status_code
200
>>> r.history
[<Response [301 Moved Permanently]>]

# Timeouts (default 5s)
>>> httpx.get('https://github.com/', timeout=0.001)
>>> httpx.get('https://github.com/', timeout=None)

# HTTPX supports Basic and Digest HTTP authentication.

# Basic
>>> httpx.get("https://example.com", auth=("my_user", "password123"))

# Digest
>>> auth = httpx.DigestAuth("my_user", "password123")
>>> httpx.get("https://example.com", auth=auth)
<Response [200 OK]>

# Exceptions
try:
    response = httpx.get("https://www.example.com/")
except httpx.RequestError as exc:
    print(f"An error occurred while requesting {exc.request.url!r}.")
```

## [Advanced usage](https://www.python-httpx.org/advanced/)

Если вы делаете что-то большее, чем эксперименты, одноразовые сценарии или прототипы, вам следует использовать экземпляр Client.

Когда вы делаете запросы с помощью API верхнего уровня, как описано в кратком руководстве, HTTPX должен устанавливать новое соединение для каждого отдельного запроса (соединения не используются повторно). По мере увеличения количества запросов к хосту это быстро становится неэффективным.

С другой стороны, экземпляр клиента использует пул HTTP-соединений. Это означает, что когда вы делаете несколько запросов к одному и тому же хосту, клиент будет повторно использовать базовое TCP-соединение вместо того, чтобы заново создавать его для каждого отдельного запроса.

Это может привести к значительному повышению производительности по сравнению с использованием API верхнего уровня, в том числе:

- Уменьшенние задержки между запросами
- Снижение загрузки ЦП и количества обращений round-tips.
- Снижение загруженности сети.

Экземпляры клиента также поддерживают функции, недоступные в API верхнего уровня, например:

- Сохранение файлов cookie между запросами.
- Применение конфигурации ко всем исходящим запросам.
- Отправка запросов через HTTP-прокси.
- Использование HTTP/2.

```python
>>> with httpx.Client() as client:
...     r = client.get('https://example.com')
...
>>> r
<Response [200 OK]>
```

Общая конфигурация для запросов (внимательно изучи поведение при мерже глобального конфига и внутри контекста - для разных полей запроса поведение отличается):

```python
>>> url = 'http://httpbin.org/headers'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> with httpx.Client(headers=headers) as client:
...     r = client.get(url)
...
>>> r.json()['headers']['User-Agent']
'my-app/0.0.1'
```

Достыпны собственные опции конфигурации клиента, к примеру `base_url`

```python
>>> with httpx.Client(base_url='http://httpbin.org') as client:
...     r = client.get('/headers')
...
>>> r.request.url
URL('http://httpbin.org/headers')
```

### Calling into Python Web Apps

Вы можете настроить клиент httpx для прямого вызова веб-приложения Python с использованием протокола WSGI.

Это особенно полезно для двух основных вариантов использования:

- Использование httpx в качестве клиента внутри тестовых случаев.
- Макетирование внешних сервисов во время тестов или в средах разработки/постановки.

```python
from flask import Flask
import httpx


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

with httpx.Client(app=app, base_url="http://testserver") as client:
    r = client.get("/")
    assert r.status_code == 200
```

### Request instances

Для максимального контроля над тем, что отправляется по сети, HTTPX поддерживает создание явных экземпляров запроса:

```python
headers = {"X-Api-Key": "...", "X-Client-ID": "ABC123"}

with httpx.Client(headers=headers) as client:
    request = client.build_request("GET", "https://api.example.com")

    print(request.headers["X-Client-ID"])  # "ABC123"

    # Don't send the API key for this particular request.
    del request.headers["X-Api-Key"]

    response = client.send(request)
    ...
```

HTTPX позволяет регистрировать «перехватчики событий» у клиента, которые вызываются каждый раз, когда происходит определенный тип события.

```python
def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = httpx.Client(event_hooks={'request': [log_request], 'response': [log_response]})
```

### HTTP Proxying

![procy](../attachments/2023-02-14-19-26-41.png)

```python
with httpx.Client(proxies="http://localhost:8030") as client:
    ...

# or
proxies = {
    "http://": "http://localhost:8030",
    "https://": "http://localhost:8031",
}

with httpx.Client(proxies=proxies) as client:
    ...
```

Подробнее в [разделе о маршрутизации](https://www.python-httpx.org/advanced/#routing).

Помимо HTTP-прокси, http также поддерживает прокси, использующие протокол SOCKS. Это необязательная функция, перед использованием которой необходимо установить дополнительную стороннюю библиотеку.

### Pool limit

Вы можете управлять размером пула соединений, используя аргумент `limit` в клиенте. Он принимает экземпляры `httpx.Limits`, которые определяют:

- `max_keepalive_connections`, количество допустимых соединений `keep-alive` или `None`, чтобы всегда разрешать (по умолчанию 20)
- `max_connections`, максимальное количество допустимых подключений или `None` без ограничений (по умолчанию 100)
- `keepalive_expiry`, ограничение по времени для неактивных соединений проверки активности в секундах или `None` для отсутствия ограничений (по умолчанию 5 с)

```python
limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
client = httpx.Client(limits=limits)
```

### Больше опций

- отображение процесса загрузки с помощью [[tqdm]]
- `.netrc` поддержка
- конфигурирование таймаутов
- Multipart file encoding
- Customizing authentication (собственная схема аутентификации, к примеру субкласс `httpx.Auth`)
- SSL certificates
- Custom Transports (пользовательский транспортный объект, который будет использоваться для отправки запросов)

## [Async Support](https://www.python-httpx.org/async/)

HTTPX предлагает стандартный синхронный API по умолчанию, но также дает вам возможность использовать асинхронный клиент, если вам это нужно.

Async — это модель параллелизма, которая намного эффективнее многопоточности и может обеспечить значительные преимущества в производительности и позволить использовать долговременные сетевые подключения, такие как WebSockets. Если вы работаете с асинхронной веб-платформой, вам также может понадобиться асинхронный клиент для отправки исходящих HTTP-запросов.

```python
>>> async with httpx.AsyncClient() as client:
...     r = await client.get('https://www.example.com/')
...
>>> r
<Response [200 OK]>
```

Доступные методы:

- `AsyncClient.get(url, ...)`
- `AsyncClient.options(url, ...)`
- `AsyncClient.head(url, ...)`
- `AsyncClient.post(url, ...)`
- `AsyncClient.put(url, ...)`
- `AsyncClient.patch(url, ...)`
- `AsyncClient.delete(url, ...)`
- `AsyncClient.request(method, url, ...)`
- `AsyncClient.send(request, ...)`

```python
# opening client witn acync context manager
async with httpx.AsyncClient() as client:
    ...

# alternative
client = httpx.AsyncClient()
...
await client.aclose()

# in a stream
>>> client = httpx.AsyncClient()
>>> async with client.stream('GET', 'https://www.example.com/') as response:
...     async for chunk in response.aiter_bytes():
```

HTTPX поддерживает [[asyncio]] или [[trio]] в качестве асинхронной среды. Он автоматически определит, какой из них использовать в качестве бэкэнда для операций сокетов и примитивов параллелизма.

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

asyncio.run(main())
```

```python
import httpx
import trio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

trio.run(main)
```

Можно использовать [[AnyIO]], который поддерживает обе либы.

```python
import httpx
import anyio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

anyio.run(main, backend='trio')
```

### Вызов веб-приложений Python

Точно так же, как `httpx.Client` позволяет напрямую обращаться к веб-приложениям WSGI, класс `httpx.AsyncClient` позволяет напрямую обращаться к веб-приложениям ASGI, что полезно для тестов.

```python
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def hello(request):
    return HTMLResponse("Hello World!")


app = Starlette(routes=[Route("/", hello)])


>>> import httpx
>>> async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
...     r = await client.get("/")
...     assert r.status_code == 200
...     assert r.text == "Hello World!"
```

## [HTTP2 support](https://www.python-httpx.org/http2/)

Смотри еще:

- [документация](https://www.python-httpx.org/)
- [github](https://github.com/aio-libs/aiohttp)
- [[asyncio]]
- [[trio]]
- [[requests]]
- [[aiohttp]]
- [[AnyIO]]
- [[http]]


[requests]: requests "Requests"
[tqdm]: tqdm "Tqdm"
[asyncio]: asyncio "Asyncio"
[trio]: trio "Trio асинхронный фреймворк"
[AnyIO]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[http]: ../lists/http "Http"


[requests]: requests "Requests"
[tqdm]: tqdm "Tqdm"
[asyncio]: asyncio "Asyncio"
[trio]: trio "Trio асинхронный фреймворк"
[AnyIO]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[asyncio]: asyncio "Asyncio"
[trio]: trio "Trio асинхронный фреймворк"
[requests]: requests "Requests"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[AnyIO]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[http]: ../lists/http "Http"
