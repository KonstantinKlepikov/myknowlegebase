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

Фьючерсы реализуют низкоуровневый апи. Когда ожидается объект `Future`, это означает, что сопрограмма будет ждать, пока `Future` не разрешится в каком-то другом месте. В большинстве случаев подобные объекты не требуется создавать на уровне приложения. Одно из их непосредственных применения - организация колбеков по завершению сопрограмм.

```python
>>> import asyncio
>>> import functools

>>> def callback(future, n):
...     print(f'{n} in future: {future.result()}')

>>> async def register_callbacks(fut):
...     print('registering callbacks')
...     fut.add_done_callback(functools.partial(callback, n='cookies'))
...     fut.add_done_callback(functools.partial(callback, n='milk'))

>>> async def main():
...     fut = asyncio.Future()
...     await register_callbacks(fut)
...     print('set result')
...     fut.set_result('done')

>>> asyncio.run(main())
registering callbacks
set result
cookies in future: done
milk in future: done
```

В данном примере `finctools.partial` изи [[functools]] используется для передачи параметров в функцию колбека.

## Управление сопрограммами

Помимо [метода](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep) `asynco.sleep()`, который уже использовался выше для ожидания в цикле, высокоуровневый апи предлагает несколько инстурментов для создания управляющих конструкций, которые сложно конструирвоать только с помощью `await` и `async`

`wait()` реализует [ожидание завершения](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait) нескольких сопрограмм. Сопрограммы передаются функции в виде последовательности, а условие завершения можно определить через константы - завершить ожидание, когда любой переданный объект выполнен или отменен, либо когда поднята первая ошибка, либо когда все "работы" выполнены. Эвейтебл объекты, переданные функции, будут сконверчены таски. Результатом выполнения метода будет кортеж, состоящий из выполненных тасков и невыполненных фьючерсов.

```python
>>> import asyncio

>>> async def phase(i):
...     print(f'in phase {i}')
...     await asyncio.sleep(0.1 * i)
...     print(f'done with phase {i}')
...     return f'phase {i} result'

>>> async def main(num_phases):
...     phases = [
...         phase(i)
...         for i in range(num_phases)
...     ]
...     completed, pending = await asyncio.wait(phases)
...     results = [t.result() for t in completed]
...     print(results)

>>> asyncio.run(main(3))
in phase 2
in phase 0
in phase 1
done with phase 0
done with phase 1
done with phase 2
['phase 1 result', 'phase 2 result', 'phase 0 result']
```

В данном примере интересна последовательность. Причина неупорядоченности заключается в том, что `wait()` хранит тааски во множестве.

Помимо всего прочего, для `wait()` можно установить `timeout` в секундах. Ожидание будет остановлено по времени. Тут важен следующий нюанс - `wait()` не отмсеняет задачи при выходе по таймауту. При возврате управления циклю событий сопрограммы будут возобновлены, а невыполненные таски будут выполняться. Чтобы избежать этого, следует отменить их вручную, примерно так:

```python
...
...     if pending:
...         for i in pending:
...             i.cancel()
```

Более простая конструкция `wait_for()` реализует [ожидание до таймаута](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for). При наступлении таймаута переданные методу невыполненный таск будет отменен (в отличие от `wait()` ожидается единственный объект, а не последовательность).

Метод `gather()` реализует [ожидание полного успешного](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather) завершения всех задач. Доступа к задачам нет и их нельзя отменить. Результат возвращается в порядке предоставления методу, в не зависимости от порядка исполнения задач. Если какая-то задач поднимет исключение - остальные не будут отменены и продолжат выполняться. По сути таким образом реализован оптимизированный сбор результатов сопрограмм.

`as_completed()` реализует [генератор, который заполняется по мере выполнения тасков](https://docs.python.org/3/library/asyncio-task.html#asyncio.as_completed). Очередность не гарантируется. Ждать завершения всех тасков не обязательно. Так-же доступен таймоут. Пример:

```python
>>> import asyncio

>>> async def phase(i):
...     print(f'in phase {i}')
...     await asyncio.sleep(0.5 - (0.1 * i))
...     print(f'done with phase {i}')
...     return f'phase {i} result'

>>> async def main(num_phases):
...     phases = [
...         phase(i)
...         for i in range(num_phases)
...     ]
...     results = []
...     for next_to_complete in asyncio.as_completed(phases):
...         answer = await next_to_complete
...         results.append(answer)
...     print(results)

>>> asyncio.run(main(3))
in phase 2
in phase 0
in phase 1
done with phase 2
done with phase 1
done with phase 0
['phase 2 result', 'phase 1 result', 'phase 0 result']
```

`asynco.shield()` [реализует защиту](https://docs.python.org/3/library/asyncio-task.html#asyncio.shield) сопрограммы от отмсены в случае отмены другой сопрограммы, содержащей защищенную. Сопрограмма оборачивается в таск и если случилась отмена, то таск отменен не будет. Если отмена происходит по какой-то другой причине (например непосредственно отменена сама переданноая в `shield()` сопрограмма), то таск все-таки будет отменен.

Кроме того, в python3.9 добьавлен `asyncio.to_thread`, позволяющий запускать сопрограммы в разных потоках. В python3.7 добавлены `asyncio.current_task()` и `asyncio.all_tasks()` для получения текущей задачи из цикла и всех невыполненных тасков.

## Синхронизация

Заметка будет дополняться...

[[python-standart-library]]

Смотри еще:

- [[threading]]
- [[multiprocess]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[threading]: threading "Threading"
[functools]: functools "Functools"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[multiprocess]: multiprocess "Управление процессами в python"
[//end]: # "Autogenerated link references"