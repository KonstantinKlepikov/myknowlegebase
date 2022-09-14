---
description: Модули subprocess, signal и multiprocessing в стандартной библиотеке python
tags: python-standart-library python
title: Управление процессами в python
---
## [subprocess](https://docs.python.org/3/library/subprocess.html)

Предоставляет АПИ, позволяющий создавать дополнительные процессы и обмениваться данными с ними. Модуль поддерживает обмен через стандартные каналы ввода-вывода, поэтому удобен для работы с текстом.

Предоставляются три основных интрумента:

- `run()` - интерфейс для выполнения процесса с возможностью захвата его выхода
- `Popen` - класс, используемый для создания других более сложных интерфейсов
- функции `call()`, `check_call()`, `check_out()` старый интерфейс, активно использовавшийся в python2. Их поведение можно полностью реализовать с помощью `run()` и `Popen`

Функционал, предоставленный модулем, заменяет собой `os.system()`, `os.spawn()`, версии `popen()` из `os`, а также модуль `commands`. [Подробнее об этом](https://docs.python.org/3/library/subprocess.html#replacing-older-functions-with-the-subprocess-module)

Доступно:

- создание процессов
- выполнение команд
- обработка ошибок
- перехват или подавление выхода
- односторонее и двустороннее взаимодействие с процессом
- объединение каналов стандартного вывода и ошибок
- создание субпроцессов
- объединение процессов в конвеер
- обмен данными между процессами

## [signal](https://docs.python.org/3/library/signal.html?highlight=signal#module-signal)

Реализует ассинхронный обмен данными между процессами и позволяет создавать обработчики для событий.

Сигналы - это средство операционнй системы, обеспечтвающее доставку уведомлений о наступлении событий и ассинхронную обработку уведомлений. Сигналы можно посылать из процесса в процесс.

Сигналы прерывают ход выполнения программы. что может вести к ошибкам (особенно это касается ввода-вывода), если сигнал получен в момент выполнения.

Формат сигналов специфичен платформе и определяется в заголовочных файлах C операционной системы.

Обработчик сигналов Python не выполняется внутри обработчика сигналов низкого уровня (C). Вместо этого обработчик сигналов низкого уровня устанавливает флаг, который сообщает виртуальной машине выполнить соответствующий обработчик сигнала Python в более поздний момент (например, в следующей инструкции байт-кода). Это приводит к некоторым [нюансам в обработке ошибок](https://docs.python.org/3/library/signal.html?highlight=signal#execution-of-python-signal-handlers)

Обработчики сигналов Python всегда выполняются в основном потоке Python основного интерпретатора, даже если сигнал был получен в другом потоке. Это означает, что сигналы нельзя использовать как средство межпоточного взаимодействия. Кроме того, только основной поток основного интерпретатора может устанавливать новый обработчик сигналов.

Пример

```python
import signal, os

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError("Couldn't open device!")

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# This open() may hang indefinitely
fd = os.open('/dev/ttyS0', os.O_RDWR)

signal.alarm(0)          # Disable the alarm
```

## [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)

Позволяет инициировать процессы на разных ядрах в обход [[gil]]. АПИ модуля идентично [[threading]]

Поддерживается три метода создания процессов:

- spawn - родительский процесс запускает новый процесс интерпретатора python. Дочерний процесс наследует только те ресурсы, которые необходимы для запуска метода `run()` объекта процесса. В частности, ненужные файловые дескрипторы и дескрипторы родительского процесса не будут унаследованы. Запуск процесса с использованием этого метода довольно медленный по сравнению с использованием fork или forkserver. Доступно в Unix и Windows. По умолчанию в Windows и macOS (начиная с 3.8).
- fork - родительский процесс использует `os.fork()` для получения форка интерпретатора python. Дочерний процесс, когда он начинается, фактически идентичен родительскому процессу. Все ресурсы родителя наследуются дочерним процессом. Безопасное разветвление многопоточного процесса проблематично. Доступно только в Unix. По умолчанию в Unix.
- forkserver при запуске программы запускается процесс сервера. С этого момента, когда требуется новый процесс, родительский процесс подключается к серверу и запрашивает его форк для нового процесса. Процесс форкнутого сервера является однопоточным, поэтому использование `os.fork()` безопасно. Ненужные ресурсы не наследуются. Доступно на платформах Unix, которые поддерживают передачу файловых дескрипторов по каналам Unix.

Установить метод можно так (пример из документации):

```python
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

или получив объект контекста через `get_context()`, апи которого идентично апи модуля, что позволяет использовать несколько контекстов одновременно (пример из документации):

```python
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

Объекты из разных контекстов, особенно те, кторые реализуют ожидание с блокировкой, могут быть несовместимы с другими контекстами.

### [Process](https://docs.python.org/3/library/multiprocessing.html#process-and-exceptions)

Процессы создаются с помощью `Process`, который реализует апи, аналогичный `threading`:

- `run()` - инициализирует процесс, можно переопределить в собственном классе
- `start()` - предоставляет запуск процесса
- `join()` блокирует выход до тех пор пока не завершится процесс, чей join() был вызван. Процесс можно джойнить много раз, нельзя приджойнить к самому себе и нельзя заджойнить до старта. Можно задать время блокировки, если в это время процесс не завершился, происходит разблокировка вне зависимости от результата.
- `daemon` запуск професса фоном, без блокировки выхода из основной программы
- и др. методы

Кроме того, поддерживается передача аргументов в том же самом виде, что и в `threading` за исключением того, что объекты, передаваемые процессам должны иметь возможность быть сериализованными с помощью `pickle` (смотри [[data-storage-python]]).

```python
import multiprocessing

def worker(num):
    """thread worker function"""
    print('Worker:', num)

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()
```

Дочерний процесс должен иметь возможность импортировать сценарий, воркера. Это порождает проблему рекурсивного выполнения при импорте. Использование конструкции `if __name__ == "__main__":` в месте запуска процессов гарантирует, что воркер не будет исполнен при импорте.

Можно создавать дочерние классы от `Process` переопределяя метод `run()`

Аналогично `threading` мы можем определить текущий процесс по имени:

```python
import multiprocessing

def worker():
    name = multiprocessing.current_process().name
    print(name)
```

Процесс можно "убить" с помощью `terminate()` - этим не стоит злоупотреблять и стоит делать, только в ситуациях вероятного зависания процесса или при взаимоблокировке. После `terminate()` необходимо вызвать `join()` для процесса, чтобы `multiprocessing` успел обновить состояние посел преждевременного завершения (иначе мы рискуем завершить основную программу с ошибками). Кроме того, если этот метод используется, когда связанный процесс использует пайплайн, очередь или другие объекты, подразумевающие ожидание - это может привести к повреждению этих объектов. Метод `kill()` является аналогом, использующим другой код выхода.

Метод `close()` высвобождает все ресурсы, ассоциированные с процессом. Это становится полезным при создании пулов.

### Объекты [Pipes и Queue](https://docs.python.org/3/library/multiprocessing.html#pipes-and-queues)

В модуле реализованы объекты `Pipe`, `Queue`, `SimpleQueue` и `JoinableQueue`. Все они реализуют логику разделения процессов и передачи сообщений между процессами.

- `Pipe` последовательно синхронизирует работу процессов двух
- `Queue` создает общую очередь для процессов
- `SimpleQueue` упрощенный вариант очереди, похожий на `Pipe`
- `JoinableQueue` реализует дополнительные методы  `task_done()` и `join()` для самой очереди

Пример очереди процессов, возврпащающей данные сосновному рабочему процессу. В данном случае для принудительной остановки используются стоп-объекты для каждого рабочего процесса, которые добавляются в очередь. Когда рабочему процессу встречается такой объект - он завершается. Метод `join()` очереди используется, чтобы дождаться завершения всех процессов перед обработкой результата.

{% gist 28ac9f72918fa6436300d2c7c1ae7c02 %}

### Оюмен сигналами между процессами

Аналогично [[threading]] реализованы следующие объекты:

- [Event](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Event) обмен информацией между процессами с помощью флагов
- [Lock](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Lock) блокировка доступов к раздеяемым ресурсам
- [RLock](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.RLock) рекурсивный аналог, позволяет повторно лочить ресурс
- [Semaphore](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Semaphore) одновременный доступ процессов к ресурсам с ограничением количества процессов, имеющих доступ
- [BoundedSemaphore](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.BoundedSemaphore)
- [Barrier](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Barrier) блокировка на контрольной точке, блокирцующая процессы до тех пор, пока не будет достигнуто заданное число заблокированных процессов
- [Condition](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Condition) - синхронизация процессов таким образом, чтобы определить какие будут выполнены параллельно, а какие последовательно

### Разделяемые типы

Есть возможность создавать [объекты, разделяющие общую память для дочерних процессов](https://docs.python.org/3/library/multiprocessing.html#shared-ctypes-objects).

### [Managers](https://docs.python.org/3/library/multiprocessing.html#managers)

Менеджеры предоставляют способ создания данных, которые могут совместно использоваться разными процессами, включая обмен по сети между процессами, запущенными на разных машинах. Объект-менеджер управляет серверным процессом, который управляет общими объектами. Другие процессы могут получить доступ к общим объектам с помощью прокси.

В основном придется использовать:

В данном простом примере общий словарь, предоставленный посредством `Manager()` заполняется разными процессами. Естественно порядок вставки не гарантируется, т.к. процессы конкурируют за ресурсы процессора.

```python
import multiprocessing

def worker(d, key, value):
    d[key] = value

if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [
        multiprocessing.Process(
            target=worker,
            args=(d, i, i * 2),
        )
        for i in range(10)
    ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print(d)

{0: 0, 3: 6, 1: 2, 2: 4, 4: 8, 5: 10, 7: 14, 6: 12, 8: 16, 9: 18}
```

Кроме того, можно вызвать объект `Namespace` менеджера в котором реализовывать разделяемые объекты

```python
>>> manager = multiprocessing.Manager()
>>> Global = manager.Namespace()
>>> Global.x = 10
>>> Global.y = 'hello'
>>> Global._z = 12.3    # this is an attribute of the proxy
>>> print(Global)
Namespace(x=10, y='hello')
```

Важно - обновление содержимого изменяемых типов не рьбновляется автоматически в простарнстве имен. Такие типы как `list()` придется переопределять.

Примеры кастомизации и использования менеджеров удаленно [тут](https://docs.python.org/3/library/multiprocessing.html#customized-managers)

Наконец можно создавать прокси-обэекты - это объекты которые относятся к разделяемому (общему) объекту, который (предположительно) живет в другом процессе. Общий объект называется референтом прокси. У нескольких прокси-объектов может быть один и тот же референт. Прокси-объект имеет методы, которые вызывают соответствующие методы его референта (хотя не каждый метод референта обязательно будет доступен через прокси). Таким образом, прокси можно использовать так же, как и его референт. Важная особенность - прокси-объект сериализуем и его можно передавать между процессами.

```python
>>> from multiprocessing import Manager
>>> manager = Manager()
>>> a = manager.list()
>>> b = manager.list()
>>> a.append(b)         # referent of a now contains referent of b
>>> print(a, b)
[<ListProxy object, typeid 'list' at ...>] []
>>> b.append('hello')
>>> print(a[0], b)
['hello'] ['hello']
```

Больше примеров [тут](https://docs.python.org/3/library/multiprocessing.html#proxy-objects)

## [Pools](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool)

Класс `Pool` обеспечивает управление фиксированным количеством процессов, когда работу можно разбить на независимые части. Строится список, который заполняется при завершении процессов, а затем возвращается. Создавая пул, можно задать количество процессов и функцию, которая будет производить работую, которая будет вызвана однократно каждым процессом при запуске.

`Pool` поддерживает асинхронные расчеты с таймаутами и обратными вызовами и имеет реализацию `map`. Если для процессов установлено значение `None`, то используется число, возвращаемое `os.cpu_count()`. `maxtasksperchild` - это количество задач, которые рабочий процесс может выполнить до того, как он завершится и будет заменен новым рабочим процессом, чтобы освободить неиспользуемые ресурсы. Это полезно в случаях, когда есть медленные и быстрые задачи, чтобы общее время вычислений не зависело от того, насколько процесс с медленными задачами доминирует в общем времени исполнения. По умолчанию для `maxtasksperchild` установлено значение `None`, что означает, что рабочие процессы будут жить столько же, сколько и пул. `context` можно использовать для указания контекста, используемого для запуска рабочих процессов.

Методы объекта пула должны вызываться только процессом, создавшим пул.

Предупреждение Объекты `multiprocessing.pool` имеют внутренние ресурсы, которыми необходимо правильно управлять (как и любой другой ресурс), используя пул в качестве диспетчера контекста или вызывая `close()` и `terminate()` вручную. Невыполнение этого требования может привести к зависанию процесса при завершении. Крмое того, CPython не гарантирует, что сборщик мусора завершит и удалит пул.

Пример (в данном случае задействован двойной доступный пул ядер):

```python
import multiprocessing

def do_calculation(data):
    return data * 2

def start_process():
    print('Starting', multiprocessing.current_process().name)

if __name__ == '__main__':
    inputs = list(range(10))
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
        maxtasksperchild=2,
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print(pool_outputs)

```

```shell
Starting ForkPoolWorker-1
Starting ForkPoolWorker-2
Starting ForkPoolWorker-3
Starting ForkPoolWorker-4
Starting ForkPoolWorker-5
Starting ForkPoolWorker-6
Starting ForkPoolWorker-7
Starting ForkPoolWorker-8
Starting ForkPoolWorker-9
Starting ForkPoolWorker-10
Starting ForkPoolWorker-11
Starting ForkPoolWorker-12
Starting ForkPoolWorker-14
Starting ForkPoolWorker-13
Starting ForkPoolWorker-15
Starting ForkPoolWorker-16
Starting ForkPoolWorker-18
Starting ForkPoolWorker-17
Starting ForkPoolWorker-19
Starting ForkPoolWorker-20
Starting ForkPoolWorker-21
Starting ForkPoolWorker-22
Starting ForkPoolWorker-23
Starting ForkPoolWorker-24
Starting ForkPoolWorker-25
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

## Что посмотреть еще?

Предоставляется внутренний [логгер](https://docs.python.org/3/library/multiprocessing.html#logging), доступный через `log_to_stderr()`

```python
>>> import multiprocessing, logging
>>> logger = multiprocessing.log_to_stderr()
>>> logger.setLevel(logging.INFO)
>>> logger.warning('doomed')
[WARNING/MainProcess] doomed
>>> m = multiprocessing.Manager()
[INFO/SyncManager-...] child process calling self.run()
[INFO/SyncManager-...] created temp directory /.../pymp-...
[INFO/SyncManager-...] manager serving at '/.../listener-...'
>>> del m
[INFO/MainProcess] sending shutdown message to manager
[INFO/SyncManager-...] manager exiting with exitcode 0
```

Подробный гайд как работать с множественными процессами и примеры [смотри здесь](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines). Если вкратце:

- Насколько это возможно, следует стараться избегать перемещения больших объемов данных между процессами.
- Убедитесь, что аргументы методов прокси-серверов сериализуемы
- Не используйте прокси-объект из более чем одного потока, если вы не защитите его блокировкой.
- В Unix, когда процесс завершается, но не присоединен, он становится зомби. Их никогда не должно быть очень много
- При использовании методов запуска spawn или forkserver многие типы из многопроцессорной сборки должны быть сериализуемыми, чтобы дочерние процессы могли их использовать
- необходимо избегать `terminate()`
- Всякий раз, когда используется очередь, необходимо убедиться, что все объекты, помещенные в очередь, в конечном итоге будут удалены до присоединения к процессу. В противном случае нельзя быть увереным, что процессы, поместившие элементы в очередь, завершатся.

Пример последнего утверждения (здесь следует удалить джойн или поменять переместить его вниз):

```python
from multiprocessing import Process, Queue

def f(q):
    q.put('X' * 1000000)

if __name__ == '__main__':
    queue = Queue()
    p = Process(target=f, args=(queue,))
    p.start()
    p.join()                    # this deadlocks
    obj = queue.get()
```

[Примеры с использованием менеджера и проксей, пула и очередей](https://docs.python.org/3/library/multiprocessing.html#examples)

[[python-standart-library]]

Смотри еще:

- [[threading]]
- [[asyncio]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[gil]: gil "Gil"
[threading]: threading "Threading"
[data-storage-python]: data-storage-python "Pickle, shelve, dbm"
[threading]: threading "Threading"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[threading]: threading "Threading"
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"