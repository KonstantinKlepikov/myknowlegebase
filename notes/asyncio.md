---
description: Модуль acyncio в python
tags: python-standart-library asyncio python
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

[Первый подход](https://docs.python.org/3/library/asyncio-task.html#asyncio.run) - через `asyncio.run()`. Непосредственный вызов сопрограммы возвращает инициализированный объект сопрограммы, который сам по себе ничего не делает и ожидает включения в цикл событий. Функция `asyncio.run()` запускает новый цикл и заботится о завершении цикла, когда все сопрограммы выполнены. Функция не может запустить новый цикл, если в текущем потоке уже есть другой цикл.

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

Помимо [метода](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep) `asyncio.sleep()`, который уже использовался выше для ожидания в цикле, высокоуровневый апи предлагает несколько инстурментов для создания управляющих конструкций, которые сложно конструирвоать используя одни `await` и `async`

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

`asyncio.shield()` [реализует защиту](https://docs.python.org/3/library/asyncio-task.html#asyncio.shield) сопрограммы от отмсены в случае отмены другой сопрограммы, содержащей защищенную. Сопрограмма оборачивается в таск и если случилась отмена, то таск отменен не будет. Если отмена происходит по какой-то другой причине (например непосредственно отменена сама переданная в `shield()` сопрограмма), то таск все-таки будет отменен.

Кроме того, в python3.9 добьавлен `asyncio.to_thread`, позволяющий запускать сопрограммы в разных потоках. В python3.7 добавлены `asyncio.current_task()` и `asyncio.all_tasks()` для получения текущей задачи из цикла и всех невыполненных тасков.

## Синхронизация и взаимодействие в цикле

`asyncio` сконструирован для однопоточных процессов и конструкции синхронизации хоть и реализованы в стиле [[threading]], являются потоконебезопасными. Кроме того, в этих конструкциях нельзя задать время ожидания (вместо этого необходимо использовать `asyncio.wait_for()` и `asyncio.wait()`)

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

## Высокоуровневый АПИ

[high level api reference](https://docs.python.org/3/library/asyncio.html)

### [Runers](https://docs.python.org/3/library/asyncio-runner.html)

`asyncio.run(coro, *, debug=None, loop_factory=None)`

Выполняет сопрограмму coro и возвращает результат. Эта функция запускает переданную сопрограмму, заботясь о управление циклом событий asyncio, завершении асинхронного генератора и закрытии исполнителя.

Эту функцию нельзя вызвать, когда выполняется другой цикл событий asyncio. работающий в том же потоке.

Если `debug` `True`, цикл событий будет запущен в режиме отладки. False отключает режим отладки явно. `None` используется для соблюдения глобального Настройки режима отладки.

Если `loop_factory` не `None`, он используется для создания нового цикла событий; в противном случае используется `asyncio.new_event_loop()`. В конце цикл закрывается. Эту функцию следует использовать в качестве основной точки входа для асинхронных программ. и в идеале она должена вызываться только один раз. Рекомендуется использовать `loop_factory` для настройки цикла событий вместо политик.

Исполнителю предоставляется тайм-аут продолжительностью 5 минут для завершения работы. Если исполнитель не закончил работу за это время, выдается предупреждение. поток выпускается и исполнитель закрывается.

```python
async def main():
    await asyncio.sleep(1)
    print('hello')

asyncio.run(main())
```

`class asyncio.Runner(*, debug=None, loop_factory=None)`

Менеджер контекста, который упрощает множественные вызовы асинхронных функций в одном и том же контексте.

Иногда в одном и том же цикле событий необходимо вызвать несколько асинхронных функций с тем же самым contextvars.Context.

Если debug равно True, цикл событий будет запущен в режиме отладки. False отключает режим отладки явно. None используется для соблюдения глобального Настройки режима отладки.

По сути, `asyncio.run()` пример можно переписать так:

```python
async def main():
    await asyncio.sleep(1)
    print('hello')

with asyncio.Runner() as runner:
    runner.run(main())
```

Методы:

- `run(coro, *, context=None)` (нельзя вызвать, когда выполняется другой цикл событий asyncio в том же потоке)
- `close()`
- `get_loop()`

### [Coroutines](https://docs.python.org/3/library/asyncio-task.html)

Предпочтительно создавать сопрограммы через `async/await`. При вызове сопрограммы вне цикла событий возвращается объект сопрограммы, а не результат вычислений. Механизмы вызова сопрограммы:

- функция `asyncio.run()` принимает сопрограмму в качестве аргумента
- ожидание сопрограммы через `await`
- функция `asyncio.create_task()` для запуска сопрограмм одновременно как объектов `Task`
- класс `asyncio.TaskGroup` предоставляет более современный альтернатива `create_task()`

Мы говорим, что объект является ожидаемым объектом (awaitable), если его можно использовать в выражении await.

Существует три основных типа ожидаемых объектов: сопрограммы (coroutines), задачи (tasks) и фьючерсы (futures).

Сопрограммы можно ожидать в других сопрограммах (функциях сопрограмм). Задачи используются для планирования сопрограмм одновременно. Фьючерс — это специальный **низкоуровневый** ожидаемый объект, который представляет конечный результат асинхронной операции. Объекты фьючерсов в asyncio необходимы для реализации кода на основе обратного вызова. для использования с async/await.

### [Creating Tasks](https://docs.python.org/3/library/asyncio-task.html#creating-tasks)

`asyncio.create_task(coro, *, name=None, context=None)` оборачивает сопрограмму и возвращает объект `Task`. Если `name` не `None`, оно устанавливается как имя задачи с помощью `Task.set_name()`. Необязательный аргумент `context`, предназначенный только для ключевых слов, позволяет указать специальный `contextvars.Context`. Текущая копия контекста создается, когда контекст не указан. Задача выполняется в цикле, возвращаемом `get_running_loop()`, `RuntimeError` возникает, если в текущем потоке нет работающиего цикла.

ВЦикл событий сохраняет только слабые ссылки на задачи. Задача, на которую нет ссылок в другом месте может быть собрана GC в любое время, даже до того, как это будет выполнена.

```python
background_tasks = set()

for i in range(10):
    task = asyncio.create_task(some_coro(param=i))

    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after
    # completion:
    task.add_done_callback(background_tasks.discard)
```

Задачи можно легко и безопасно отменить. Когда задача отменена, будет поднята `asyncio.CancelledError` в задаче как только появится возможность. Рекомендуется использовать `try/finaly` для надежной очистки.

Группы задач сочетают в себе API создания задач с удобным и надежный способ дождаться завершения всех задач в группе.

`class asyncio.TaskGroup` асинхронный менеджер, имеющий метод `create_task(coro, *, name=None, context=None)`

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(some_coro(...))
        task2 = tg.create_task(another_coro(...))
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
```

Инструкция будет ждать завершения всех задач в группе. Во время ожидания в группу еще могут добавляться новые задачи.После завершения последней задачи и выхода из блока в группу нельзя добавлять новые задачи. При первом сбое какой-либо задачи, принадлежащей группе за исключением `asyncio.CancelledError,` остальные задачи в группе отменяются. После этого в группу невозможно будет добавить никакие дальнейшие задачи.

После завершения всех задач, если какие-либо задачи не удалось выполнить за исключением `asyncio.CancelledError`, исключения объединены в `ExceptionGroup` или `BaseExceptionGroup`, который подымается. Если какая-либо задача завершается с ошибкой `KeyboardInterrupt` или `SystemExit`, группа задач по-прежнему отменяет оставшиеся задачи и ожидает завершения, а `KeyboardInterrupt` или `SystemExit` подымается вместо `ExceptionGroup` или `BaseExceptionGroup`.

Если тело оператора завершается с исключением, это рассматривается так же, как если бы одна из задач не удалась: оставшиеся задачи отменяются и затем ожидаются, и исключения, не подлежащие отмене группируются.

### Sleeping

`coroutine asyncio.sleep(delay, result=None)` приостанавливает задачу на переданное количество секунд. Установка задержки на 0 обеспечивает возможность другим сопрограммам запускаться. Если предоставлен `result`, он возвращается вызывающей стороне когда сопрограмма завершится.

### [Running Tasks Concurrently](https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)

`awaitable asyncio.gather(*aws, return_exceptions=False)` запуск ожидаемых объектов в aws последовательности одновременно. Все сопрограммы в последовательноси будут обернуты в `Task`. Если все awaitable выполнены успешно, результатом будет совокупный список возвращаемых значений. Порядок значений результата соответствует порядку ожидаемых объектов в aws.

`return_exceptions` определяет как будут обработаны исключения задач. `False` (дефолтное) поднимет исключения (что не отменит остальные задачи), `True` запишет их и вернет после завершения группы.

Если `gather()` отменен, все задачи, которые ще не завершены, тоже будут отвемнены. Отмена задач не отменяет gather.

Альтернатива gather - это `TaskGroup,` которая гарантирует отмену всех оставшихся вложенных задач при исключении задачи.

`asyncio.eager_task_factory(loop, coro, *, name=None, context=None)`. При использовании этой фабрики (через `loop.set_task_factory(asyncio.eager_task_factory)`), сопрограммы начинают выполнение синхронно во время построения Task. Задачи планируются в цикле событий только в том случае, если они блокируются. Это может быть улучшением производительности, поскольку накладные расходы на планирование циклов избегаются для сопрограмм, которые выполняются синхронно. Типичным примером, где это полезно, являются сопрограммы, которые используют кэширование или мемоизация, чтобы избежать фактического ввода-вывода, когда это возможно.

Примечание Немедленное выполнение сопрограммы является семантическим изменением. Если сопрограмма возвращается или вызывается, задача никогда не запланирована. в цикле событий. Если выполнение сопрограммы блокируется, задача запланирована в цикле событий. Это изменение может привести к изменению в существующих приложениях. Например, порядок выполнения задач приложения может измениться. Добавлено в 3.12.

`asyncio.create_eager_task_factory(custom_task_constructor)` реализует фабрику через кастомный конструктор.

### Shielding

`awaitable asyncio.shield(aw)` устанавливает защиту от отмены. Позволяет защитить от cancelled после создания таска. Сохранение ссылок на задачи, переданные в функцию, обязательно по тем же причинам, что и при создании таска

```python
task = asyncio.create_task(something())
res = await shield(task)

# эквивалентно (за исключением отмены содержащей сопрограммы)
res = await something()
```

### Timeouts

`asyncio.timeout(delay)` создает асинхронный контекстный менеджер который можно использовать для ограничения количества времени, затрачиваемого на ожидание чего-то (к примеру задачи). delay может быть либо None, либо int/flot. Если задержка равна None, ограничения по времени не будет применяться; это может быть полезно, если задержка неизвестна, когда контекстный менеджер создан. В любом случае, диспетчер контекста может быть перепланирован после создание с использованием `Timeout.reschedule()`. Добавлено в 3.11

```python
async def main():
    async with asyncio.timeout(10):
        await long_running_task()

# перехватить исключение TimeoutError можно только вне контекстного менеджера
async def main():
    try:
        async with asyncio.timeout(10):
            await long_running_task()
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")

    print("This statement will run regardless.")
```

`class asyncio.Timeout(when)` сам контекстный менеджер, обладает методами `when()`, `reschedule(when: float | None)`, `expired()`. Добавлено в 3.11

```python
async def main():
    try:
        # We do not know the timeout when starting, so we pass ``None``.
        async with asyncio.timeout(None) as cm:
            # We know the timeout now, so we reschedule it.
            new_deadline = get_running_loop().time() + 10
            cm.reschedule(new_deadline)

            await long_running_task()
    except TimeoutError:
        pass

    if cm.expired():
        print("Looks like we haven't finished on time.")
```

`asyncio.timeout_at(when)` аналогично функции за исключением того, что время ожидания абсолютное. Добавлено в 3.11

```python
async def main():
    loop = get_running_loop()
    deadline = loop.time() + 20
    try:
        async with asyncio.timeout_at(deadline):
            await long_running_task()
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")

    print("This statement will run regardless.")
```

`coroutine asyncio.wait_for(aw, timeout)` позволяет дождаться выполнения с таймаутом. Если происходит тайм-аут, задача отменяется и поднимается `TimeoutError`. Чтобы избежать cancellation, оберните в `shield()`. Функция будет ждать, пока future не будет фактически отменено, поэтому общее время ожидания может превысить тайм-аут. Если исключение происходит во время отмены, оно распространяется. Если ожидание отменяется, future aw также отменяется.

```python
async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except TimeoutError:
        print('timeout!')

asyncio.run(main())

# Expected output:
#
#     timeout!
```

### [Waiting Primitives](https://docs.python.org/3/library/asyncio-task.html#waiting-primitives)

`coroutine asyncio.wait(aws, *, timeout=None, return_when=ALL_COMPLETED)` таски запускаются одновременно и блокируются, пока не будет выполнено условие return_when. Итерируемый элемент aws не должен быть пустым. Возвращает два набора задач//ьючерсов: (done, pending)

```python
done, pending = await asyncio.wait(aws)
```

Эта функция не вызывает TimeoutError. В отличие от `wait_for()`, `wait()` не отменяет фьючерсы, когда происходит тайм-аут. Фьючерсы или задачи, которые не выполняются, когда наступает тайм-аут, просто вернулся во втором сете.

return_when указывает, когда эта функция должна вернуться. Это должно быть одной из следующих констант:

- `FIRST_COMPLETED` Функция вернется, когда любой из вьючерсов завершается или отменяется
- `FIRST_EXCEPTION` Функция вернется, когда любой фьючерс поднимает исключение (если ни один - эквивалент олл комплитед)
- `ALL_COMPLETED` Функция вернется, когда все фьючерсы заканчиваются или отменяются.

`asyncio.as_completed(aws, *, timeout=None)` Возвращает итератор сопрограмм. Каждую возвращенную сопрограмму можно ожидатьВызывает TimeoutError, если тайм-аут наступает раньше чем все фьючерсы выполнены.

```python
for coro in as_completed(aws):
    earliest_result = await coro
    # ...
```

### [Running in Threads](https://docs.python.org/3/library/asyncio-task.html#running-in-threads)

`coroutine asyncio.to_thread(func, /, *args, **kwargs)` Асинхронно запускает функцию func в отдельном потоке. Любые `*args` и `**kwargs`, указанные для этой функции, передаются напрямую функции. Кроме того, распространяется текущий `contextvars.Context`. Возвращает сопрограмму, которую можно ожидать, чтобы получить конечный результат func.

Эта в первую очередь предназначена для использования для выполнения синхронных Функции/методов, связанных с вводом-выводом, которые в противном случае заблокировали бы цикл событий, если они запускались бы в основном потоке.

```python
def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")

async def main():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())

# Expected output:
#
# started main at 19:50:53
# start blocking_io at 19:50:53
# blocking_io complete at 19:50:54
# finished main at 19:50:54
```

`asyncio.run_coroutine_threadsafe(coro, loop)` Функция предназначена для ожидания из другого потока.

Цикл событий запускается в потоке (обычно в основном потоке) и выполняется все обратные вызовы и задачи в своем потоке. Пока Задача выполняется в цикле событий, никакие другие задачи не могут выполняться в том же потоке. Когда задача выполняет выражение await, выполняющаяся задача приостанавливается и цикл событий выполняет следующую задачу. Чтобы запланировать обратный вызов из другого потока ОС, Следует использовать метод `loop.call_soon_threadsafe()`. Пример:

```python
loop.call_soon_threadsafe(callback, *args)
```

Почти все объекты asyncio не являются потокобезопасными, что обычно бывает не проблема, если нет кода, который разделяет общие объекты в памяти или работает с источниками данных снаружи. Планирование сопрограмм из другого потока делается так:

```python
async def coro_func():
     return await asyncio.sleep(1, 42)

# Later in another OS thread:

future = asyncio.run_coroutine_threadsafe(coro_func(), loop)
# Wait for the result:
result = future.result()
```

Для обработки сигналов цикл событий должен быть запустить в основном потоке. Метод `loop.run_in_executor()` можно использовать с `concurrent.futures.ThreadPoolExecutor` для выполнения блокировка кода в другом потоке ОС без блокировки потока где выполняется цикл событий.

В настоящее время невозможно напрямую запланировать сопрограммы или обратные вызовы. из другого процесса (например, запущенного с `multiprocessing`).

Блокирующий (привязанный к процессору) код не следует вызывать напрямую. Например, если функция выполняет вычисления с интенсивным использованием ЦП в течение 1 секунды, все одновременные задачи asyncio и операции ввода-вывода будут задержаны на 1 секунду.

Исполнитель может использоваться для запуска задачи в другом потоке или даже в другой процессе, см. метод `loop.run_in_executor()` [асинхроннорго цикла](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor).

```python
import asyncio
import concurrent.futures

def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)

def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))

async def main():
    loop = asyncio.get_running_loop()

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, blocking_io)
        print('custom thread pool', result)

    # 3. Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, cpu_bound)
        print('custom process pool', result)

if __name__ == '__main__':
    asyncio.run(main())
```

## [Task Object](https://docs.python.org/3/library/asyncio-task.html#task-object)

`class asyncio.Task(coro, *, loop=None, name=None, context=None, eager_start=False)`

Циклы событий используют совместное планирование: цикл событий запускается по одной задаче за раз. Пока Задача ожидает завершения В будущем цикл событий запускает другие задачи, обратные вызовы или выполняет Операции ввода-вывода.

Используйте функцию высокого уровня `asyncio.create_task()` для создания Задачи, или низкоуровневые `loop.create_task()` или `ensure_future()` функции. Не следует сздавать экземпляры тасков вручную.

Чтобы отменить запущенную Задачу, используйте метод `cancel()`, что выдаст исключение `CancelledError`. Если сопрограмма ожидает объект фьючерса во время отмены, он будет отменен.

`cancelled()` можно использовать, чтобы проверить, была ли задача отменена.

`asyncio.Task` наследует от `Future` все свои API, кроме `Future.set_result()` и `Future.set_exception()`.

Необязательный аргумент `context`, предназначенный только для ключевых слов, позволяет указать специальный `contextvars.Context` для coro для запуска. Если контекст не указан, Задача копирует текущий контекст. и позже запускает свою сопрограмму в скопированном контексте.

Необязательный аргумент `eager_start`, предназначенный только для ключевых слов, позволяет начать выполнять задачу во время создания (добавлено в 3.12).

Методы%

- `done()`
- `result()`
- `exception()`
- `add_done_callback(callback, *, context=None)`
- `remove_done_callback(callback)`
- `get_stack(*, limit=None)`
- `print_stack(*, limit=None, file=None)`
- `get_coro()`
- `get_context()`
- `get_name()`
- `set_name(value)`
- `cancel(msg=None)`
- `cancelled()`
- `uncancel()`
- `cancelling()`

### [Streams](https://docs.python.org/3/library/asyncio-stream.html)

Обеспечивает потоковое чтение и запись. Предоставлются два класса - `StreamReader` и `StreamWriter`, а так-же функции для управления сокетами. Дополнительно - [Transports and Protocols](https://docs.python.org/3/library/asyncio-protocol.html#asyncio-example-create-connection) и моудль [socket](https://docs.python.org/3/library/socket.html?highlight=socket#module-socket).

### [Synchronization Primitives](https://docs.python.org/3/library/asyncio-sync.html)

`class asyncio.Lock` реализует блокировку [мьютекса](https://ru.wikipedia.org/wiki/%D0%9C%D1%8C%D1%8E%D1%82%D0%B5%D0%BA%D1%81) для асинхронных задач. Не потокобезопасный. Асинхронную блокировку можно использовать, чтобы гарантировать эксклюзивный доступ к общкму ресурсу. Предпочтительным способом использования блокировки является `async with`

```python
lock = asyncio.Lock()

# ... later
async with lock:
    # access shared state
```

Методы:

- `acquire()`
- `release()`
- `locked()`

`class asyncio.Event` не потокобезопасный. Эвент можно использовать для уведомления нескольких задач asyncio. что произошло какое-то событие. Объект Event управляет внутренним флагом, которому можно установить `true` с помощью метода `set()` и сбросить значение в `false` с помощью `clear()` метод. Метод `wait()` блокируется до тех пор, пока флаг не будет установлен в `true`. Изначально для флага установлено значение `false`.

`class asyncio.Condition(lock=None)` Не потокобезопасный. Условие может использоваться задачей для ожидания что какое-то событие должно произойти, а затем получения преимущественого доступа к общему ресурсу.

По сути, объект Condition сочетает в себе функциональность Event и Lock. Несколько объектов Condition используют один Lock, что позволяет координировать эксклюзивный доступ к общему ресурсу между различными задачами. Необязательный аргумент lock должен быть объектом Lock или None. Предпочтительный способ использования условия – `async with`. Дополнительные методы `notify(n=1)` и `notify_all()` позволяют уведомить о событии n-сопрограмм или все. Методы `wait()` и `wait_for()` позволяют ожидать определенным сопрограммам наступления события.

`class asyncio.Semaphore(value=1)` Не потокобезопасный. Семафор управляет внутренним счетчиком, который уменьшается при каждом `acquire()`в и увеличивается при каждом `release()`. Счетчик никогда не может опуститься ниже нуля; когда `acquire()` найдет что он равен нулю, он блокируется, ожидая вызова какой-нибудь задачи и `release()`. Необязательный аргумент `value` задает начальное значение для счетчика (1 по умолчанию). Если заданное значение меньше, чем 0, поднимется `ValueError`. Предпочтительным способом использования семафора является `async with`.

`class asyncio.BoundedSemaphore(value=1)` Не потокобезопасный. Ограниченный семафор — это версия `Semaphore`, которая возбуждает `ValueError` в `release()`, если это увеличивает счетчик выше начального значения.

`class asyncio.Barrier(parties)` Не потокобезопасный. Барьер — это простой примитив синхронизации, который позволяет блокировать сопрограммы до тех пор, пока не накопится требуемое количество задач, ожидающих выполнения. Задачи могут ожидать выполнения метод `wait()` и будут заблокированы до тех пор, пока указанное количество задач не накопится. В этот момент все ожидающие задачи разблокируются одновременно. Добавлено в 3.11

```python
async def example_barrier():
   # barrier with 3 parties
   b = asyncio.Barrier(3)

   # create 2 new waiting tasks
   asyncio.create_task(b.wait())
   asyncio.create_task(b.wait())

   await asyncio.sleep(0)
   print(b)

   # The third .wait() call passes the barrier
   await b.wait()
   print(b)
   print("barrier passed")

   await asyncio.sleep(0)
   print(b)

asyncio.run(example_barrier())

<asyncio.locks.Barrier object at 0x... [filling, waiters:2/3]>
<asyncio.locks.Barrier object at 0x... [draining, waiters:0/3]>
barrier passed
<asyncio.locks.Barrier object at 0x... [filling, waiters:0/3]>
```

Возвращаемое `wait()` значение представляет собой целое число в диапазоне от 0 до parties-1, отличающееся для каждой задачи. Это можно использовать для выбора задачи, требующей выполнения каких-то особых действий.

```python
...
async with barrier as position:
   if position == 0:
      # Only one task prints this
      print('End of *draining phase*')
```

### [Subprocesses](https://docs.python.org/3/library/asyncio-subprocess.html)

### [Queues](https://docs.python.org/3/library/asyncio-queue.html)

пример

```python
import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main())
```

## [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)

## Дополнительные материалы

Смотри еще:

- [high level api reference](https://docs.python.org/3/library/asyncio.html)
- [[python-standart-library]]
- [[threading]]
- [[multiprocess]]
- [[asyncio-transports-and-protocols]]
- [[async-generators-and-iterators]]
- [[contextvars]]
- [[molotov]]
- [[jina]]
- [[trio]]
- [[aiohttp]]
- [[httpx]]
- [[anyio]]
- [[telegram-bots]]
- [[asyncpg]]
- [nest_asyncio](https://github.com/erdewit/nest_asyncio)
- [A list of libraries](https://github.com/python/asyncio/wiki/ThirdParty#filesystem) for AsyncIO is available on PyPI with Framework::AsyncIO classifier (github)

Полезные асинхронные пакеты:

- [aiobreaker](https://github.com/arlyon/aiobreaker) — это реализация шаблона Circuit Breaker на Python, описанная в книге Майкла Т. Найгарда `Release It!`. Автоматические выключатели существуют для того, чтобы позволить одной подсистеме выйти из строя, не разрушая всю систему. Это делается путем объединения опасных операций (обычно точек интеграции) с компонентом, который может обходить вызовы, когда система неработоспособна.
- [aiohttp_retry](https://github.com/inyutin/aiohttp_retry) Простой клиент реализации повторных попыток запросов для [[aiohttp]]
- [aiolimiter](https://github.com/mjpieters/aiolimiter) Эффективная реализация ограничителя скорости для asyncio

Статьи и ответы на вопросы:

- [Have two infinite task with asyncio](https://stackoverflow.com/questions/52199619/have-two-infinite-task-with-asyncio)
- [asyncio.gather vs asyncio.wait (vs asyncio.TaskGroup)](https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait-vs-asyncio-taskgroup)
- [python asyncio add tasks dynamically](https://stackoverflow.com/questions/66998329/python-asyncio-add-tasks-dynamically)
- [RuntimeError: This event loop is already running in python](https://stackoverflow.com/questions/46827007/runtimeerror-this-event-loop-is-already-running-in-python) solution: [nest_asyncio](https://github.com/erdewit/nest_asyncio)
- [How to cancel all remaining tasks in gather if one fails?](https://stackoverflow.com/a/59074112)

[//begin]: # "Autogenerated link references for markdown compatibility"
[threading]: threading "Threading"
[async-generators-and-iterators]: async-generators-and-iterators "Async generators and iterators"
[functools]: functools "Functools"
[queue]: queue "queue"
[asyncio-transports-and-protocols]: asyncio-transports-and-protocols "Asyncio transports and protocols"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[multiprocess]: multiprocess "Управление процессами в python"
[contextvars]: contextvars "Contextvars"
[molotov]: molotov "Molotov"
[jina]: jina "Jina"
[trio]: trio "Trio асинхронный фреймворк"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[httpx]: httpx "httpx cинхронный и асинхронный http-клиент"
[anyio]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[telegram-bots]: telegram-bots "Telegram python bots"
[asyncpg]: asyncpg "asyncpg postgresql client"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[threading]: threading "Threading"
[async-generators-and-iterators]: async-generators-and-iterators "Async generators and iterators"
[functools]: functools "Functools"
[threading]: threading "Threading"
[queue]: queue "queue"
[asyncio-transports-and-protocols]: asyncio-transports-and-protocols "Asyncio transports and protocols"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[threading]: threading "Threading"
[multiprocess]: multiprocess "Управление процессами в python"
[asyncio-transports-and-protocols]: asyncio-transports-and-protocols "Asyncio transports and protocols"
[async-generators-and-iterators]: async-generators-and-iterators "Async generators and iterators"
[contextvars]: contextvars "Contextvars"
[molotov]: molotov "Molotov"
[jina]: jina "Jina"
[trio]: trio "Trio асинхронный фреймворк"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[httpx]: httpx "httpx cинхронный и асинхронный http-клиент"
[anyio]: anyio "AnyIO асинхронный бекенд на базе asyncio и trio"
[telegram-bots]: telegram-bots "Telegram python bots"
[asyncpg]: asyncpg "asyncpg postgresql client"
[//end]: # "Autogenerated link references"