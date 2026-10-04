---
description: Декораторы для асинхронных свойств async_property, async_cached_property`, AwaitLoader.
tags: python asyncio python-standart-library pip
title: async_property
---
Кратко: Python-декораторы для свойств на async-функциях. Поддерживает обычные и кешированные асинхронные свойства (Python 3.7+, MIT).

Источник: [async_property](https://github.com/ryananguiano/async_property)

## Основная идея

`@async_property` работает как обычный `@property`, но на async-функции: доступ к свойству возвращает `awaitable`.

```python
class Foo:
    @async_property
    async def remote_value(self):
        return await get_remote_value()

instance = Foo()
value = await instance.remote_value
```

### Кешированное свойство

`@async_cached_property` вызывает функцию один раз. Повторные `await` возвращают закешированное значение. Кеш защищён `asyncio.Lock`, чтобы гарантировать однократный вызов при конкурентном доступе.

```python
class Foo:
    @async_cached_property
    async def value(self):
        print('loading value')
        return 123

instance = Foo()
await instance.value  # -> prints 'loading value', returns 123
await instance.value  # -> returns 123 (без повторного вызова)

instance.value = 'abc'  # можно присвоить
del instance.value  # удалить кеш и позволить следующему await заново загрузить
```

### AwaitLoader

Если объект содержит несколько кешированных свойств, можно наследоваться от `AwaitLoader` — тогда экземпляр становится `awaitable` и при создании загружает все `@async_cached_property` параллельно. Также `AwaitLoader` вызывает `await instance.load()` если он определён.

```python
class Foo(AwaitLoader):
    async def load(self):
        print('load called')

    @async_cached_property
    async def db_lookup(self):
        return 'success'

    @async_cached_property
    async def api_call(self):
        print('calling api')
        return 'works every time'

instance = await Foo()  # вызовет load() и загрузит кешированные свойства параллельно
```

## Особенности

- Поддержка обычных и кешированных свойств.
- Кешированные свойства защищены `asyncio.Lock` — вызываются только один раз при конкурентных await.
- Поведение свойств близко к `property`: можно присваивать и удалять значения.
- Есть утилиты для массовой предварительной загрузки (`AwaitLoader`).

## Дополнительно

- [[notes/asyncio]]
- [[lists/python-standart-library]]

[notes/asyncio]: asyncio "Asyncio"
[lists/python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
