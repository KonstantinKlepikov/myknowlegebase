---
description: Asynchronous HTTP Client/Server for asyncio and Python
tags: http asincio python
title: Aiohttp асинхронный клиент-свервер на python.
---
Asynchronous HTTP Client/Server for [[asyncio]] and Python.

`pip install aiohttp`

Ключевые фичи:

- Поддерживает как клиент, так и HTTP-сервер.
- Поддерживает как серверные веб-сокеты, так и клиентские веб-сокеты «из коробки» без использования колбеков.
- Веб-сервер имеет промежуточное программное обеспечение, сигналы и подключаемую маршрутизацию.

Client example

```python
import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

This prints:

```sh
Status: 200
Content-type: text/html; charset=utf-8
Body: <!doctype html> ...
Coming from requests ? Read why we need so many lines.
```

Server example:

```python
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)
```

Зависимости:

- Python 3.6+
- `async_timeout`
- `attrs`
- `charset-normalizer`
- `multidict`
- `yarl`
- Optional `cchardet` as faster replacement for `charset-normalizer`.
- Optional `aiodns` for fast DNS resolving. The library is highly recommended.

## [Client](https://docs.aiohttp.org/en/stable/client.html)

Клиент написан поверх [[asincio]]. Базовые функции сходны с асинхронным АПИ [[httpx]], с тем лишь исключением, что сразу реализован собственный session класс и вся работа ведется с ним.

```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())

asyncio.run(main())
```

Варианты запросов

```python
session.post('http://httpbin.org/post', data=b'data')
session.put('http://httpbin.org/put', data=b'data')
session.delete('http://httpbin.org/delete')
session.head('http://httpbin.org/get')
session.options('http://httpbin.org/get')
session.patch('http://httpbin.org/patch', data=b'data')

# can be used base urls
async with aiohttp.ClientSession('http://httpbin.org') as session:
    async with session.get('/get'):
        pass
    async with session.post('/post', data=b'data'):
        pass
    async with session.put('/put', data=b'data'):
        pass
```

Не создавайте сессию для каждого запроса. Сессия - объект реализующий логику запросов всег оприложения. В более сложных случаях может потребоваться сессия для каждого ресурса сети. В любом случае создание сессии для каждого запроса - очень плохая идея. Сессия содержит внутри пул соединений. Повторное использование соединения и поддержка активности (оба включены по умолчанию) могут повысить общую производительность.

### Передача параметров в url:

```python
params = {'key1': 'value1', 'key2': 'value2'}
async with session.get('http://httpbin.org/get',
                       params=params) as resp:
    expect = 'http://httpbin.org/get?key1=value1&key2=value2'
    assert str(resp.url) == expect

# or
params = [('key', 'value1'), ('key', 'value2')]
async with session.get('http://httpbin.org/get',
                       params=params) as r:
    expect = 'http://httpbin.org/get?key=value2&key=value1'
    assert str(r.url) == expect

# or
async with session.get('http://httpbin.org/get',
                       params='key=value+1') as r:
        assert str(r.url) == 'http://httpbin.org/get?key=value+1'
```

aiohttp внутренне выполняет канонизацию URL перед отправкой запроса.

### Responses, codes and others

```python
# text and status codes
async with session.get('https://api.github.com/events') as resp:
    print(resp.status)
    print(await resp.text())

# binary
print(await resp.read())

# json request and response
async with aiohttp.ClientSession() as session:
    async with session.post(url, json={'test': 'object'})

async with session.get('https://api.github.com/events') as resp:
    print(await resp.json())

# Streaming Response Content (for big bunch of data)
async with session.get('https://api.github.com/events') as resp:
    await resp.content.read(10)

with open(filename, 'wb') as fd:
    async for chunk in resp.content.iter_chunked(chunk_size):
        fd.write(chunk)

# streaming uploads is similar to core
with open('massive-body', 'rb') as f:
   await session.post('http://httpbin.org/post', data=f)

# multipart upload
url = 'http://httpbin.org/post'
data = FormData()
data.add_field('file',
               open('report.xls', 'rb'),
               filename='report.xls',
               content_type='application/vnd.ms-excel')

await session.post(url, data=data)

# websokets (ou must use the only websocket task for both reading
# (e.g. await ws.receive() or async for msg in ws:) and writing but may
# have multiple writer tasks which can only send data asynchronously
# (by await ws.send_str('data') for example))
async with session.ws_connect('http://example.org/ws') as ws:
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close cmd':
                await ws.close()
                break
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break

# timeouts
timeout = aiohttp.ClientTimeout(total=60)
async with aiohttp.ClientSession(timeout=timeout) as session:
    ...
```

### [Adwanced client](https://docs.aiohttp.org/en/stable/client_advanced.html)

```python
# custom headers
url = 'http://example.com/image'
payload = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00'
          b'\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
headers = {'content-type': 'image/gif'}

await session.post(url,
                   data=payload,
                   headers=headers)

# or set default headers
headers={"Authorization": "Basic bG9naW46cGFzcw=="}
async with aiohttp.ClientSession(headers=headers) as session:
    async with session.get("http://httpbin.org/headers") as r:
        json_body = await r.json()
        assert json_body['headers']['Authorization'] == \
            'Basic bG9naW46cGFzcw=='

# custom cookies
url = 'http://httpbin.org/cookies'
cookies = {'cookies_are': 'working'}
async with ClientSession(cookies=cookies) as session:
    async with session.get(url) as resp:
        assert await resp.json() == {
           "cookies": {"cookies_are": "working"}}

# or share сookies between many requests
async with aiohttp.ClientSession() as session:
    await session.get(
        'http://httpbin.org/cookies/set?my_cookie=my_value')
    filtered = session.cookie_jar.filter_cookies(
        'http://httpbin.org')
    assert filtered['my_cookie'].value == 'my_value'
    async with session.get('http://httpbin.org/cookies') as r:
        json_body = await r.json()
        assert json_body['cookies']['my_cookie'] == 'my_value'

# Response Headers and Cookies
# By RFC-like standard dict
assert resp.headers == {
    'ACCESS-CONTROL-ALLOW-ORIGIN': '*',
    'CONTENT-TYPE': 'application/json',
    'DATE': 'Tue, 15 Jul 2014 16:49:51 GMT',
    'SERVER': 'gunicorn/18.0',
    'CONTENT-LENGTH': '331',
    'CONNECTION': 'keep-alive'}

# more frendly
assert resp.headers['Content-Type'] == 'application/json'
assert resp.headers.get('content-type') == 'application/json'

# By raw
assert resp.raw_headers == (
    (b'SERVER', b'nginx'),
    (b'DATE', b'Sat, 09 Jan 2016 20:28:40 GMT'),
    (b'CONTENT-TYPE', b'text/html; charset=utf-8'),
    (b'CONTENT-LENGTH', b'12150'),
    (b'CONNECTION', b'keep-alive'))

# access to cookie
url = 'http://example.com/some/cookie/setting/url'
async with session.get(url) as resp:
    print(resp.cookies['example_cookie_name'])
```

Больше опций:

- Redirection History
- Cookie Jar
- Uploading pre-compressed data
- Disabling content type validation for JSON s
- Client Tracing
- Custom transport
- SSL control for TCP sockets
- Proxy support

## [Server](https://docs.aiohttp.org/en/stable/web.html)

[Несколько примеров реализации](http://demos.aiohttp.org/en/latest/)

### [Quikstart](https://docs.aiohttp.org/en/stable/web_quickstart.html)

```python
from aiohttp import web

# A request handler must be a coroutine that accepts
# a Request instance as its only parameter and returns
# a Response instance
async def hello(request):
    return web.Response(text="Hello, world")

# Next, create an Application instance and register
# the request handler on a particular HTTP method and path
app = web.Application()
app.add_routes([web.get('/', hello)])

# After that, run the application by run_app()
web.run_app(app)


# alternative - using route decorator
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
app.add_routes(routes)
web.run_app(app)
```

По сути реализуется логика, знакомая по разным http-фреймворкам, типа [[fastapi]]

### [Advanced usage](https://docs.aiohttp.org/en/stable/web_advanced.html) and [logging](https://docs.aiohttp.org/en/stable/logging.html)

Смотри еще:

- [документация](https://docs.aiohttp.org/en/stable/)
- [github](https://github.com/aio-libs/aiohttp)
- [aioresponses](https://github.com/pnuckowski/aioresponses) is a helper to mock/fake web requests in python aiohttp package
- [[asyncio]]
- [[trio]]
- [[requests]]
- [[httpx]]
- [[AnyIO]]
- [[http]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[asyncio]: asyncio "Asyncio"
[asincio]: ../tag/asincio "Tag: asincio"
[httpx]: httpx "httpx cинхронный и асинхронный http-клиент"
[fastapi]: fastapi "Fastapi"
[asyncio]: asyncio "Asyncio"
[trio]: trio "Trio асинхронный фреймворк"
[requests]: requests "Requests"
[httpx]: httpx "httpx cинхронный и асинхронный http-клиент"
[AnyIO]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[http]: ../lists/http "Http"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[asyncio]: asyncio "Asyncio"
[asincio]: ../tag/asincio "Tag: asincio"
[httpx]: httpx "httpx cинхронный и асинхронный http-клиент"
[fastapi]: fastapi "Fastapi"
[asyncio]: asyncio "Asyncio"
[trio]: trio "Trio асинхронный фреймворк"
[requests]: requests "Requests"
[httpx]: httpx "httpx cинхронный и асинхронный http-клиент"
[AnyIO]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[http]: ../lists/http "Http"
[//end]: # "Autogenerated link references"