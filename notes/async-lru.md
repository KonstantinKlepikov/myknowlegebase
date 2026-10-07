---
description: async-lru — LRU cache для асинхронных функций в asyncio
tags: python asyncio caching
title: async-lru
---
## async-lru

[async-lru](https://github.com/aio-libs/async-lru) — это библиотека для кэширования результатов асинхронных функций. По смыслу она похожа на стандартный `functools.lru_cache`, но рассчитана на `asyncio`: она умеет кешировать `awaitable`-результаты и не допускает гонок при одновременных вызовах одного и того же ключа.

Главная особенность: если несколько задач одновременно обращаются к одной и той же функции с одинаковыми аргументами, то реально будет выполнен только один вызов. Все остальные `await` получат тот же результат после завершения вычисления.

Это особенно полезно для:

- HTTP-запросов к внешним API;
- чтения данных из Redis/DB/Postgres;
- повторных вычислений на одних и тех же аргументах;
- уменьшения thundering herd при массовом параллельном доступе.

## Базовый пример

```python
import asyncio
from async_lru import alru_cache


@alru_cache(maxsize=128)
async def fetch_user(user_id: int):
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"user-{user_id}"}


async def main():
    first = await fetch_user(42)
    second = await fetch_user(42)

    print(first)
    print(second)
    print(fetch_user.cache_info())
    await fetch_user.cache_close()


asyncio.run(main())
```

Что происходит здесь:

- `@alru_cache(maxsize=128)` добавляет LRU-кэш для async-функции;
- одинаковые аргументы возвращают данные из кэша;
- разовое вычисление результата делится между всеми конкурентными вызовами;
- `cache_info()` показывает статистику: hits, misses, currsize, maxsize.

## Почему это важно

Обычный кэш для async-функций часто пишут руками через словарь и `asyncio.Lock`, но это быстро превращается в ошибочный и сложный код. `async-lru` решает типичную проблему: "несколько задач одновременно могут начать одно и то же expensive-вычисление".

Без защиты такой сценарий приводит к повторным запросам к API, лишним вычислениям и лавине параллельных вызовов. `async-lru` как раз устраняет этот эффект, сохраняя семантику LRU-кэша.

## TTL и expiration

Библиотека поддерживает TTL (time-to-live) для кэшированных значений. Это удобно, если данные быстро устаревают и хочется периодически обновлять их без полного сброса кэша.

```python
from async_lru import alru_cache


@alru_cache(ttl=5)
async def get_config(name: str):
    return name.upper()
```

Для более мягкого обновления можно использовать `jitter`:

```python
@alru_cache(ttl=3600, jitter=1800)
async def fetch_data(key):
    ...
```

Тогда TTL каждого элемента будет случайно "размазаны" по диапазону, что помогает избегать массовой синхронной просушки кэша.

## Инвалидация и проверка содержимого

Библиотека умеет явно очищать элементы кэша.

```python
@alru_cache(ttl=5)
async def func(arg1, arg2):
    return arg1 + arg2

func.cache_invalidate(1, arg2=2)
```

Также есть проверка, есть ли конкретный ключ в кэше:

```python
await func(1, arg2=2)
print(func.cache_contains(1, arg2=2))  # True
```

И методы для очистки всего кэша:

```python
func.cache_clear()
```

## Кастомные ключи

По умолчанию ключ строится из аргументов функции так же, как `functools.lru_cache`. Но иногда часть аргументов не должна участвовать в ключе. Для этого есть параметр `key`.

```python
from async_lru import alru_cache


@alru_cache(key=lambda db, query: query)
async def query_db(db, query):
    return await db.execute(query)
```

Это удобно, когда один и тот же запрос должен кэшироваться независимо от того, какой именно объект соединения использовался.

## Ограничения и важные детали

У `async-lru` есть важное ограничение: кэш привязан к конкретному event loop. Если один и тот же декорированный объект начать использовать в другом event loop, библиотека выбросит `RuntimeError`.

Это нормально для типичных asyncio-приложений, где один loop на приложение, но важно помнить:

- если сервис работает на нескольких loop, нужно создавать отдельные кэш-экземпляры;
- важно не смешивать одни и те же cached-функции между потоками или loop.

Также библиотека строит ключ только из явных аргументов. Если результат зависит от `contextvars`, request-scoped state, текущего пользователя, tenant id или глобальных переменных, то это нужно явно включать в аргументы функции или использовать отдельный кэш для каждого security-domain.

## Когда использовать async-lru

Используйте `async-lru`, когда:

- у вас async-функция делает expensive I/O или вычисления;
- один и тот же запрос может повторяться много раз;
- важно не только кэшировать результаты, но и дедуплицировать concurrent calls;
- нужен простой LRU-подход без написания кастомного кэша.

Типичные сценарии:

- кеширование response body из API;
- мемоизация запросов к базе и сервисам;
- уменьшение повторной нагрузки при burst-traffic.

## Сравнение с functools.lru_cache

`functools.lru_cache` хорошо работает для sync-функций, но не подходит для async-кода. `async-lru` же:

- работает с `async def`;
- обеспечивают совместный результат для concurrent requests;
- поддерживает TTL и явную инвалидацию;
- сохраняет идеи LRU и `cache_info` в привычной форме.

## Дополнительно

- [[notes/asyncio]]
- [[notes/async_property]]
- [[lists/python-standart-library]]

## Источник

- [async-lru на GitHub](https://github.com/aio-libs/async-lru)

## AI-warning

✨ Данная статья сгенерирована с помощью ChatGPT 5.0 mini. Текст проверен человеком.

[notes/asyncio]: asyncio "Asyncio"
[notes/async_property]: async_property "Async property"
[lists/python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
