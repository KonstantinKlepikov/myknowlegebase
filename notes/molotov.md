---
description: Приложение для нагрузочного тестирования http-ресурса
tags: tests pip python
title: Molotov
---
Асинхронный (смотри [[asyncio]]) тестировщик нагрузки для http

```python
"""
This Molotov script has 2 scenario
"""
from molotov import scenario

_API = "http://localhost:8080"

@scenario(weight=40)
async def scenario_one(session):
    async with session.get(_API) as resp:
        res = await resp.json()
        assert res["result"] == "OK"
        assert resp.status == 200

@scenario(weight=60)
async def scenario_two(session):
    async with session.get(_API) as resp:
        assert resp.status == 200
```

- [Документация](https://molotov.readthedocs.io/en/stable/)
- [[тестирование]]
- [[notes/linux]]


[asyncio]: asyncio "Asyncio"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
[notes/linux]: linux "Linux"
