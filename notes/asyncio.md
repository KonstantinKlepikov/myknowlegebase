---
description: Модуль acyncio в python
tags: python-standart-library
---
# Asyncio

Модель асинхронности в python строится на концепции сопрограмм. Сопрограмма ([coroutine](https://docs.python.org/3/glossary.html#term-coroutine)) передает управление вызвавшему ее коду без потери своего состояния. Первоначально апи ассинхронных функций был реализован на [генераторах с декораторами](https://docs.python.org/3/library/asyncio-task.html#asyncio-generator-based-coro). В python3.8 такой подход уже депрекейтед. Пример такого кода:

```python
import asyncio

@asyncio.coroutine
def outer():
    result1 = yield from phase1()
    result2 = yield from phase2(result1)
    return (result1, result2)

@asyncio.coroutine
def phase1():
    return 'result1'

@asyncio.coroutine
def phase2(arg):
    return 'result2 derived from {}'.format(arg)

event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
finally:
    event_loop.close()
```

Основной рабочей структурой `asyncio` является цикл событий, в котормо регистрируются сопрограммы и который управляет событиями ввода/вывода и контекстом. Реализацию цикла можно выбрать для конкретного приложения или использовать дефолтную. Реализации специфичны к операционной системе. Приложение коммуницирует с циклом, регистрирует функции и позволяет циклу выполнять вызовы, если доступны ресурсы. Код приложения должен уступать управление, если в контексте цикла для него нет работы.

Кроме сопрограмм реализованы `Future` и `Task` (фьючерсы и таски), а так-же объекты предоставляющие апи параллельной обработки по аналогии с [[threading]].

`asyncio` как модуль оформился в python3.5. Были добавлены синтаксические конструкции `async` и `await`, которые реализуют непосредственный интерфейс асинхронного программирования. `async` перед `def` определяет новую сопрограмму. Ключевое слово `await` используется для ожидания результата сопрограммы, фьючерса или таска (в текущий момент в библиотеке реализовано три awaitable объекта), после чего происходит передача циклу событий.

`asyncio` реализует два АПИ: низкоуровневый и высокоруовневый. [Выкоуровневый](https://docs.python.org/3/library/asyncio-api-index.html) - это запуск сопрограмм, создание тасков, очередей, сабропроцессов и потоков, а так-же синхронизация в цикле (реализована в стиле `threading`). [Низакоуровневый](https://docs.python.org/3/library/asyncio-llapi-index.html) - доступ к объектам цикла и управление циклом.

## Как запускаются сопрограммы

Высокоуровнево реализовано три подхода.

[Первый подход](https://docs.python.org/3/library/asyncio-task.html#asyncio.run) - через `asynco.run()`. Непосредственный вызов сопрограммы возвращает инициализированный объект сопрограммы, который сам по себе ничего не делает и ожидает включения в цикл событий. Функция `asynco.run()` запускает новый цикл и заботится о завершении цикла, когда все сопрограммы выполнены. Функция не может запустить новый цикл, если в текущем потоке уже есть другой цикл.

```python
>>> import asyncio
>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')
>>> asyncio.run(main())
hello
world
```

Такой подход реализован начиная с python3.7 и сейчас является основным. Запуск сопрограмм доступен и через [низкоуровневое АПИ](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop) посредством `asyncio.get_event_loop()`:

```python
>>> import asyncio
>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')
>>> event_loop = asyncio.get_event_loop()
>>> try:
...     coro = main()
...     event_loop.run_until_complete(coro)
>>> finally:
...     event_loop.close()
hello
world
```

Второй подход: добавление `await` вместо непосредственного добавления сопрограмм в цикл. Это возможно, так как на момент `await` поток выполнения уже находится в теле сопрограммы.

```python
>>> import asyncio
>>> import time

>>> async def say_after(delay, what):
...     await asyncio.sleep(delay)
...     print(what)

>>> async def main():
...     print(f"started at {time.strftime('%X')}")
...     await say_after(1, 'hello')
...     await say_after(2, 'world')
...     print(f"finished at {time.strftime('%X')}")

>>> asyncio.run(main())
started at 17:13:52
hello
world
finished at 17:13:55
```

Третий способ - использование [asyncio.create_task()](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task). Метод делает обертку для сопрограммы и возвращает объект `Task`. Такой подход стал доступен начиная с python3.7

```python
>>> import asyncio
>>> import time

>>> async def say_after(delay, what):
...     await asyncio.sleep(delay)

>>> async def main():
...     task1 = asyncio.create_task(
...         say_after(1, 'hello'))

...     task2 = asyncio.create_task(
...         say_after(2, 'world'))

...     await task1
...     await task2

>>> asyncio.run(main())
```

Устаревшим аналогом является вызов `asyncio.ensure_future`, который [возвращает](https://docs.python.org/3/library/asyncio-future.html#asyncio.ensure_future) `Task`:

```python
>>> task = asyncio.ensure_future(
...         say_after(1, 'hello'))
```

## [Awaitables](https://docs.python.org/3/library/asyncio-task.html#awaitables)

Помимо сопрограмм используются `Task` и `Future` объекты. Фьючерсы являются низкоуровневым объектами, представляют результаты еще не выполненных асинхронных операций и обеспечивают ассинхронное получение результатов выполнения сопрограмм. Таски - это высокоуровневые фьючерсо-подобные объекты, которые используются для запуска сопрограмм и отслеживания момента их выполнения, позволяя извлечь результат после завершения сопрограммы, обеспечивая таким образом параллельное выполнение сопрограмм.

Экземпляры фьючерса и таска обладают поведением, подобным сопрограммам, поэтому любые подходы, используемые для ожидания завершения сопрограмм, применимы и к этим объектам. Оба объекта потокон-небезопасны.

Пример создания тасков был показан выше. Таск можно отменить до его завершения, в этом случае поднимается эксепшен `CancelledError`.

```python
>>> import asyncio

>>> async def task_run():
...     await asyncio.sleep(1)

>>> async def tasc_cancel(task):
...     task.cancel()

>>> async def main():
...     print('creating task')
...     task1 = asyncio.create_task(task_run(), name='task_run')
...     task2 = asyncio.create_task(tasc_cancel(task1), name='task_cancel')
...     try:
...         await task1
...         print(f'task completed {task1.get_name()}')
...     except asyncio.CancelledError:
...         print('task canceled')
        
...     await task2
...     print(f'task completed {task2.get_name()}')

>>> asyncio.run(main())
creating task
task canceled
task completed task_cancel
```

Исключение можно перехватить и выполнить другие операции (в данном примере используется низкоуровневый апи `asyncio.get_running_loop()` для доступа к циклу - [метод доступен](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop) начиная с python3.7)

```python
>>> import asyncio

>>> async def task_run():
...     try:
...         await asyncio.sleep(1)
...     except asyncio.CancelledError:
...         print('task canceled')
...         raise

>>> def tasc_cancel(task):
...     task.cancel()

>>> async def main():
...     print('creating task')
...     loop = asyncio.get_running_loop()
...     task = loop.create_task(task_run(), name='task_run')
...     loop.call_soon(tasc_cancel, task)
...     try:
...         await task
...     except asyncio.CancelledError:
...         print('task canceled to')
        
>>> asyncio.run(main())
creating task
task canceled
task canceled to
```

Заметка в процессе доработки...

[[python-standart-library]]

Смотри еще:

- [[threading]]
- [[multiprocess]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[threading]: threading "Threading"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[threading]: threading "Threading"
[multiprocess]: multiprocess "Управление процессами в python"
[//end]: # "Autogenerated link references"