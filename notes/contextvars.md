---
description: Контекстные переменные в python
tags: python-standart-library python
title: Contextvars
---
Позволяет создавать, сохранять, изменять и передавать контекстные переменные между контекстами. Контекстные менеджеры, у которых есть состояния, должны использовать `contexztvars` вместо класса `local` из [[threading]]. Чаще всего можно встретить в асинхронных операциях [[asyncio]]. Появилось в python3.7

```python
import asyncio
import contextvars

client_addr_var = contextvars.ContextVar('client_addr')

def render_goodbye():
    # The address of the currently handled client can be accessed
    # without passing it explicitly to this function.

    client_addr = client_addr_var.get()
    return f'Good bye, client @ {client_addr}\n'.encode()

async def handle_request(reader, writer):
    addr = writer.transport.get_extra_info('socket').getpeername()
    client_addr_var.set(addr)

    # In any code that we call is now possible to get
    # client's address by calling 'client_addr_var.get()'.

    while True:
        line = await reader.readline()
        print(line)
        if not line.strip():
            break
        writer.write(line)

    writer.write(render_goodbye())
    writer.close()

async def main():
    srv = await asyncio.start_server(
        handle_request, '127.0.0.1', 8081)

    async with srv:
        await srv.serve_forever()

asyncio.run(main())
```

[Ссылка на документацию](https://docs.python.org/3/library/contextvars.html#module-contextvars)

[[python-standart-library]]

Смотри еще:

- [[asyncio]]
- [[threading]]


[threading]: threading "Threading"
[asyncio]: asyncio "Asyncio"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
