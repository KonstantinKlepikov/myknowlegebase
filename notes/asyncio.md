---
description: Модуль acyncio в python
tags: python-standart-library asincio python
title: Asyncio
---
Модель асинхронности в python строится на концепции сопрограмм. Сопрограмма ([coroutine](https://docs.python.org/3/glossary.html#term-coroutine)) передает управление вызвавшему ее коду без потери своего состояния. В отличии от обычных программ, в которые входят в одной точке, а выходят в другой, в сопрограммы можно входить и выходить из них в разных точках, кроме того, их можно продолжать используя сохраненное состояние. Первоначально апи асинхронных функций был реализован на [генераторах с декораторами](https://docs.python.org/3/library/asyncio-task.html#asyncio-generator-based-coro). В python3.8 такой подход уже депрекейтед. Пример такого кода:

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

Основной рабочей структурой `asyncio` является цикл событий, в котором регистрируются сопрограммы и который управляет событиями ввода/вывода и контекстом. Реализацию цикла можно выбрать для конкретного приложения или использовать дефолтную. Реализации специфичны к операционной системе. Приложение коммуницирует с циклом, регистрирует функции и позволяет циклу выполнять вызовы, если доступны ресурсы. Код приложения должен уступать управление, если в контексте цикла для него нет работы.

Определено два понятие - сопрограмма и функция сопрограммы (coroutine function). Функция сопрограммы возвращает объект сопрограммы.

Кроме сопрограмм реализованы `Future` и `Task` (фьючерсы и таски), а так-же объекты предоставляющие апи параллельной обработки по аналогии с [[threading]].

`asyncio` как модуль оформился в python3.5. Были добавлены синтаксические конструкции `async` и `await`, которые реализуют непосредственный интерфейс асинхронного программирования. `async` перед `def` определяет новую функцию сопрограммы. Ключевое слово `await` используется для ожидания результата сопрограммы, фьючерса или таска (в текущий момент в библиотеке реализовано три awaitable объекта), после чего происходит передача циклу событий.

В общем случае функция сопрограммы определяется через `await def` и может содержать в своем теле `async for`, `await` и `async <ключевое слово>`. Более сложные конструкции см.тут: [[async-generators-and-iterators]]. Для простоты далее я не буду разделять понятия сопрограммы и функции, см. контекст.

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

Такой подход реализован начиная с python3.7 и сейчас является основным. Запуск сопрограмм доступен и через [низкоуровневое АПИ](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop), к примеру, посредством `asyncio.get_event_loop()`:

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

Второй подход: добавление `await` к вызываемым из сопрограмм объектам вместо непосредственного добавления объектов в цикл. Это возможно, так как на момент `await` поток выполнения уже находится в теле сопрограммы.

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

Низкоуровневым аналогом является вызов `asyncio.ensure_future`, который [возвращает](https://docs.python.org/3/library/asyncio-future.html#asyncio.ensure_future) `Task`:

```python
>>> task = asyncio.ensure_future(
...         say_after(1, 'hello'))
```

## [Awaitables](https://docs.python.org/3/library/asyncio-task.html#awaitables)

Awaitable - это объект, который можно использовать в выражении `await`. Может быть сопрограммой или объектом с методом `__await __()`

Помимо сопрограмм используются `Task` и `Future` объекты. Фьючерсы являются низкоуровневым объектами, представляют результаты еще не выполненных асинхронных операций и обеспечивают ассинхронное получение результатов выполнения сопрограмм. Таски - это высокоуровневые фьючерсо-подобные объекты, которые используются для запуска сопрограмм и отслеживания момента их выполнения, позволяя извлечь результат после завершения сопрограммы.

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

Исключение можно перехватить и выполнить другие операции (в данном примере используется низкоуровневый апи `asyncio.get_running_loop()` для доступа к циклу - [метод доступен](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop) начиная с python3.7). Подход с распространением эксепшена реализован для всего апи.

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

Помимо [метода](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep) `asynco.sleep()`, который уже использовался выше для ожидания в цикле, высокоуровневый апи предлагает несколько инстурментов для создания управляющих конструкций, которые сложно конструирвоать используя одни `await` и `async`

`wait()` реализует [ожидание завершения](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait) нескольких сопрограмм. Сопрограммы передаются функции в виде последовательности, а условие завершения можно определить через константы - завершить ожидание, когда любой переданный объект выполнен или отменен, либо когда поднята первая ошибка, либо когда все "работы" выполнены. Эвейтебл объекты, переданные функции, будут сконверчены в таски. Результатом выполнения метода будет кортеж, состоящий из выполненных тасков и невыполненных фьючерсов.

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

В данном примере интересна последовательность. Причина неупорядоченности заключается в том, что `wait()` хранит таски во множестве.

Помимо всего прочего, для `wait()` можно установить `timeout` в секундах. Ожидание будет остановлено по времени. Тут важен следующий нюанс - `wait()` не отмсеняет задачи при выходе по таймауту. При возврате управления циклу событий сопрограммы будут возобновлены, а невыполненные таски будут выполняться. Чтобы избежать этого, следует отменить их вручную, примерно так:

```python
...
...     if pending:
...         for i in pending:
...             i.cancel()
```

Более простая конструкция `wait_for()` реализует [ожидание до таймаута](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for). При наступлении таймаута переданный и невыполненный единственный таск будет отменен.

Метод `gather()` реализует [ожидание полного успешного](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather) завершения всех задач. Доступа к задачам нет и их нельзя отменить. Результат возвращается в порядке предоставления методу, в не зависимости от порядка исполнения задач. Если какая-то задача поднимет исключение - остальные не будут отменены и продолжат выполняться. По сути таким образом реализован оптимизированный сбор результатов сопрограмм.

`as_completed()` реализует [генератор, который заполняется по мере выполнения тасков](https://docs.python.org/3/library/asyncio-task.html#asyncio.as_completed). Очередность не гарантируется. Ждать завершения всех тасков не обязательно. Так-же доступен таймаут. Пример:

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

`asynco.shield()` [реализует защиту](https://docs.python.org/3/library/asyncio-task.html#asyncio.shield) сопрограммы от отмсены в случае отмены другой сопрограммы, содержащей защищенную. Сопрограмма оборачивается в таск и если случилась отмена, то таск отменен не будет. Если отмена происходит по какой-то другой причине (например непосредственно отменена сама переданная в `shield()` сопрограмма), то таск все-таки будет отменен.

Кроме того, в python3.9 добьавлен `asyncio.to_thread`, позволяющий запускать сопрограммы в разных потоках. В python3.7 добавлены `asyncio.current_task()` и `asyncio.all_tasks()` для получения текущей задачи из цикла и всех невыполненных тасков.

## Синхронизация и взаимодействие в цикле

`asynco` сконструирован для однопоточных процессов и конструкции синхронизации хоть и реализованы в стиле [[threading]], являются потоконебезопасными. Кроме того, в этих конструкциях нельзя задать время ожидания (вместо этого необходимо использовать `asyncio.wait_for()` и `asyncio.wait()`)

- [Lock](https://docs.python.org/3/library/asyncio-sync.html#lock) защищает доступ к разделяемым потоками ресурсам. Также можно использовать как асинхронный менеджер контекста
- [Event](https://docs.python.org/3/library/asyncio-sync.html#event) реализует ожидание наступления какого-либо события
- [Condition](https://docs.python.org/3/library/asyncio-sync.html#condition) ожидание с возможностью указания числа возобновляемых сопрограмм
- [Semaphore](https://docs.python.org/3/library/asyncio-sync.html#semaphore) и его обрезанный аналог ограничивают одновременный доступ к ресурсу

Пример реализации лока. Лок может иметь только одного владельца. В данном примере показаны два разных метода блокировки: непосредственно через `await` и `release()` и через менеджер контекста. Мы лочим поток в самом начале и запускаем две сопрограммы, завершения которых ожидаем с помощью `wait()`. Как только первый лок снят, владелец лока меняется и первая сопрограмма выполняются, затем последующая.

```python
>>> import asyncio
>>> import functools

>>> def unlock(lock):
...     lock.release()
...     print(lock.locked())

>>> async def worker1(lock):
...     print('worker1 get lock')
...     async with lock:
...         print('worker1 acquired lock')
...     print('worker1 released lock')

>>> async def worker2(lock):
...     print('worker2 get lock')
...     await lock.acquire()
...     print('worker2 acquired lock')
...     print('worker2 released lock')
...     lock.release()

>>> async def main():
...     lock = asyncio.Lock()

...     await lock.acquire()
...     print(lock.locked())

...     loop = asyncio.get_running_loop()

...     loop.call_later(0.1, functools.partial(unlock, lock))

...     await asyncio.wait([worker1(lock), worker2(lock)]),

>>> asyncio.run(main())
True
worker2 get lock
worker1 get lock
False
worker2 acquired lock
worker2 released lock
worker1 acquired lock
worker1 released lock
```

`Event` работает аналогично, за исключением того, что сопрограммы получат возможность выполняться одновременно как только будет установлен флаг `Event.set()`

Помимо объектов синхронизации, в высокоуровневом апи реализованы очереди. Асиннхронные очереди так-же потокнебезопасные.

- [Queue](https://docs.python.org/3/library/asyncio-queue.html#asyncio.Queue) FIFO (очередь)
- [PriorityQueue](https://docs.python.org/3/library/asyncio-queue.html#asyncio.PriorityQueue) очередь с приоритетом
- [LifoQueue](https://docs.python.org/3/library/asyncio-queue.html#asyncio.LifoQueue) LIFO (стек)

Очереди похожи на стандартные конструкции из [[queue]]

## [Низкоуровневый апи](https://docs.python.org/3/library/asyncio-eventloop.html) в `asyncio`

Как говорилось выше, в стандартной библиотеке указано, что нет особой необходимости использовать низкоуровневы апи для управления асинхронными задачами на уровне приложения и данный апи должен использоваться преимущественно для написания библиотек и фреймворков.

Доступ к циклу событий [осуществляется так](https://docs.python.org/3/library/asyncio-eventloop.html). Создание фьючерсов и управление ими [можно найти тут](https://docs.python.org/3/library/asyncio-future.html). Управление событиями в цикле реализуется [вот такими методами](https://docs.python.org/3/library/asyncio-eventloop.html#event-loop-methods).

Простейший пример работы с фьючерсом (из стандартной библиотеки):

```python
import asyncio

async def set_after(fut, delay, value):
    await asyncio.sleep(delay)

    fut.set_result(value)

async def main():
    loop = asyncio.get_running_loop()

    fut = loop.create_future()

    loop.create_task(
        set_after(fut, 1, '... world'))

    print('hello ...')

    print(await fut)

asyncio.run(main())
```

В данном случае мы создаем фьючерс в контексте текущего цикла событий с помощью `create_future()`. Затем создаем таск из сопрограммы, используя низкоуровневый апи `loop.create_task` так-как у нас уже есть доступ к текущему циклу. Сопрограмма, обернутая в таск будет ожидать выполнения 1 секунду. Основная программа будет ожидать, когда фьючер предоставит результат выполнения сопрограммы.

Кроме доступа к циклам и фьючерсам, низкоуровневый апи предоставляет абстракции `Protocol` и `Transport`. Это используется для переключенния контекстов с блокировкой операций ввода-вывода и обеспечивает высокопроизводительную реализацию сетевых протоколов или протоколов HTTP. `Transport` определяет какой байт-код передать, а `Protocol` - в каком порядке. Совместно эти интерфейсы реализуют абстрактный интерфейс для использования сетевого ввода-вывода и межпроцессного ввода-вывода. В данной заметке я не рассматриваю эту концепцию. Смотри [[asyncio-transports-and-protocols]].

## [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)

Отдельным вопросом является использование сопрограмм с несколькими потоками или процессами, так-как большинство объектов, определеннх в сторонних библиотеах не готово к взаимодействию в цикле событий и будет блокироваться.

Эту проблему частично устраняет модуль `concurrent.futures`, предоставляющий управление пулами асинхронных задач. Модуль предоставляет классы-исполнители `ThreadPoolExecutor` и `ProcessPoolExecutor` для создания организации пулов потоков и процессов соответственно и асинхронного выполнения.

В `concurrent.futures` для взаимодействия с пулами используются исполнители, а для управления результатами выполнения - объекты-фьючерсы. Приложение создает экземпляр исполнителя соответстющего класса и передает ему задачи. При запуске каждой задачи возвращается экземпляр `Future`, который будет использоваться для блокировки до тех пор, пока результат работы не станет доступен. Управление фьючерсами на уровне модуля не требуется.

Примеры реализации [работы с потоками](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor) и [с процессами](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor).

Модуль предоставляет несколько концепций для работы в асинхронном режиме:

- `submit()` - получение объекта фьючерса связанного с переданным объектом
- `map()` - получение результата всех работ из пула в том порядке, в котором они были переданы в пул

Для фьючерсов доступен апи `asynco` - обратные вызовы, отмены и `wait()`

Пример с `map()`:

```python
>>> from concurrent import futures
>>> import threading
>>> import time

>>> def task(n):
...     print(f'{threading.current_thread().name}: sleeping {n}')
...     time.sleep(n / 10)
...     print(f'{threading.current_thread().name}: done {n}')
...     return n / 10

>>> ex = futures.ThreadPoolExecutor(max_workers=2)
>>> results = ex.map(task, range(5, 0, -1))
>>> gone_results = list(results)
>>> print(f'main: results: {gone_results}')
ThreadPoolExecutor-0_0: sleeping 5
ThreadPoolExecutor-0_1: sleeping 4
ThreadPoolExecutor-0_1: done 4
ThreadPoolExecutor-0_1: sleeping 3
ThreadPoolExecutor-0_0: done 5
ThreadPoolExecutor-0_0: sleeping 2
ThreadPoolExecutor-0_0: done 2
ThreadPoolExecutor-0_1: done 3
ThreadPoolExecutor-0_0: sleeping 1
ThreadPoolExecutor-0_0: done 1
main: results: [0.5, 0.4, 0.3, 0.2, 0.1]
```

Объекты исполнители [могут выполнять функции менеджеров контекста](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.shutdown). Это позволяет освободить ресурсы после выполнения всех задач потока или процесса.

Апи пула процессов идентичен апи пула потоков, с тем лишь исключением, что если один из процессов будет завершен, то и работа всего пула будет прервана (при этом надо помнить, что прерывание процессов может занимать определенное время).

В низкоруовневом апи `asyncio` [предусмотрен метод для работы с пулами потоков и процессов](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor). `loop.run_in_executor` получает в качестве аргумента объект-исполнитель, функцию-воркера и аргументы, которые должны быть переданы воркеру. Возвращаемым объектом будет фьючерс. Если методу не предоставлен исполнитель, то в качестве исполнителя создается пул потоков. Вся эта конструкция позволяет уступать управлять циклу событий, ожидать выполнения воркеров в потоках/процессах, а затем получать результат, когда он готов.

Пример:

```python
>>> import asyncio
>>> import concurrent.futures
>>> import time


>>> def blocks(n):
...     print(f'blocks({n}) running')
...     time.sleep(0.1)
...     print(f'blocks({n}) done')
...     return n ** 2


>>> async def run_blocking_tasks(ex):
...     loop = asyncio.get_event_loop()
...     blocking_tasks = [
...         loop.run_in_executor(ex, blocks, i)
...         for i in range(5)
...     ]
...     completed, pending = await asyncio.wait(blocking_tasks)
...     results = [t.result() for t in completed]
...     print('results: {!r}'.format(results))

>>> if __name__ == '__main__':
...     ex = concurrent.futures.ThreadPoolExecutor(max_workers=3)
...     asyncio.run(run_blocking_tasks(ex))
blocks(0) running
blocks(1) running
blocks(2) running
blocks(0) done
blocks(3) running
blocks(1) done
blocks(2) done
blocks(4) running
blocks(3) done
blocks(4) done
results: [9, 0, 16, 1, 4]
```

На этом все.

[[python-standart-library]]

Смотри еще:

- [[aiohttp]]
- [[threading]]
- [[multiprocess]]
- [[asyncio-transports-and-protocols]]
- [[async-generators-and-iterators]]
- [[contextvars]]
- [[molotov]]
- [[jina]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[threading]: threading "Threading"
[async-generators-and-iterators]: async-generators-and-iterators "Async generators and iterators"
[functools]: functools "Functools"
[threading]: threading "Threading"
[queue]: queue "queue"
[asyncio-transports-and-protocols]: asyncio-transports-and-protocols "Asyncio transports and protocols"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[threading]: threading "Threading"
[multiprocess]: multiprocess "Управление процессами в python"
[asyncio-transports-and-protocols]: asyncio-transports-and-protocols "Asyncio transports and protocols"
[async-generators-and-iterators]: async-generators-and-iterators "Async generators and iterators"
[contextvars]: contextvars "Contextvars"
[molotov]: molotov "Molotov"
[jina]: jina "Jina"
[//end]: # "Autogenerated link references"