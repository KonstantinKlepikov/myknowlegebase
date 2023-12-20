---
description: Параллельные вычисления в процессах в python
tags: python-standart-library python
title: Threading
---
Модуль threading реализует управление параллельными вычислениями в рамках одного процесса. Он поставляет объектно-ориентированный АПИ - объекты потоков выполняются в рамках одного и того же процесса, разделяя общую память, что помогает сократить простой процессора.

Использование одного и того же контекста несколькими потоками означает, что данные нужно защищать от неконтроллируемого одновременного доступа, иначе может возникнуть состояние "гонки", когда порядок изменения в данных может повлиять на результат. Эту проблему можно решить блокировкой. Однако тут тоже есть сложности, так как могут возникать ситуации, когда несколько процессов будут одновременно блокировать ресусры, что может привести к тупикам блокировок.

В python многопоточность используется на уровне ядра, при этом все потоки, обращающиеся к объектам python (в cpython), работают с одной глобальной блокировкой, так как большая часть внутренней реализации и сторонний код на C небезопасны для потоков. Этот механизм называется глобальной блокировкой интерпретатора ([[gil]]).

Не смотря на блокировку, многопоточность в python позволяет эффективно использовать время, когда программа ожидает освобождения ресурса, так-как поток можно разбудить в момент возврата результата.

## [Thread](https://docs.python.org/3/library/threading.html?highlight=threading#thread-objects)

Класс `Thread` позволяет создать поток в простейшем случае

```python
import threading

def worker(i):
    print(f'Im worker {i}')

threds = []
for i in ranfe(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
```

Поток запускается методом `start()`. Кроме того, мы можем передать аргументы в поток. Кроме того, потоку можно передать имя с аргументом `name=` (в примере выше имя задано по умолчанию), которое сожно получить из объекта потока через `getName()`. К примеру текущий поток в примере выше можно узнать так: `threading.current_thread().getName()`

Можно создавать поток-демоны, которые не блокируют выход из основной программы. Это используется, когда прерывание потока затруднено или его работа не влияет на данные основной программы. Установка демона производится передачей аргумента `daemon=True` или вызовом метода `set_daemon()` с аргументом `True`. Чтобы дождаться завершения демона, надо использовать метод `join()`

```python
import threading

def worker():
    print('Im daemon')

d = threading.Thread(name='daemon', target=worker, daemon=True)
d.start()
d.join()
```

Методу `join()` можно передать значение с плавающей точкой, определяющего предельное время ожидания перехода потока в неактивное состояние. Если поток не успеет завершиться за это время, то такой метод `join()` в любом случае разлочит выход из основной программы, не дождавшись завершения потока.

Чтобы не хранить список потоков, можно воспользоваться встроенным методом `enumerate()`, который возвращает список всех активных экземпляров `Theread`. Основной поток так-же входит в этот список. Чтобы не создавать взаимную блокировку через `join()`, его надо исключать из списка, например так (задержка тут просто для продолжения потока):

```python
import threading
import time

def worker():
    time.sleep(1)
    print('Im worker')

for i in range(3):
    t = threading.Thread(target=worker)
    t.start()

main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    t.join()
```

`Thread` можно переопределить переопределив его метод `run()`, который и вызывает функцию воркера. Соответственно в `run()` можно добавлять произвольный код. Аргументы, переданные конструктору, сохраняются в закрытых атрибутах, поэтому следует переопределить конструктор и сохранить значения в экземпляре, чтобы они были видны в подклассе.

```python
import threading

class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                        daemon=daemon)
        self.args = args
        self.kwargs=kwargs

    def run(self):
        print(f'Im run with {self.args}, {self.kwargs}!')


for i in range(3):
    t = MyThread(args=(i,), kwargs={'a': 1, 'b': 2})
    t.start()
```

## [Timer](https://docs.python.org/3/library/threading.html?highlight=threading#threading.Thread.daemon)

Поток `Timer` начинает работать с некоторой задержкой, заданной в секундах. Кроме того, его можно отменить до того, как он начал исполняться с помощью `cancel()`.

## [Event](https://docs.python.org/3/library/threading.html?highlight=threading#event-objects)

Используется для синхронизации потоков (там где это нужно). В `Event` предоставлен флаг, котоырй можно безопасно устанавливать и сбрасывать в потока методами `set()` и `clear()`. С помощью метода `wait()` можно приостанавливать работу потока до тех пор пока не будет установлен флаг или пока не истечет время.

```python
import threading
import time

def wait_for(e, t):
    while not e.is_set():
        print('wait to event')
        event = e.wait(t)
        if event:
            print('event work')
        else:
            print('other works')

e1 = threading.Event()
e2 = threading.Event()

t1 = threading.Thread(target=wait_for, args=(e1, 2))
t1.start()

t2 = threading.Thread(target=wait_for, args=(e2, 4))
t2.start()

time.sleep(0.5)
e1.set()
time.sleep(0.5)
e2.set()
```

## [Lock](https://docs.python.org/3/library/threading.html?highlight=threading#threading.Lock)

`Lock` позволяет залочить потоконебезопасные структуры, чтобы избежать потери данных или их разрушения. К примеру, списки и словари потоко-безопасны, чего не скажешь о таких типах как числа. `Lock` блочит все обращения к объекту до тех пор, пока не разлочится текущее.

Метод `asquire()` устанавливает - блокирующий или нет лок. Если нужно определить, заблокирован ли поток, не останавливая текущий, следует использовать метод `asquire()` с аргументом `False`. С помощью `release()` поток можно выпустить, при условии что он заблокирован.

Пример демонстрирует как это может работать:

```python
import logging
import threading
import time

def holder(lock):
    logging.debug('Starting holder')
    while True:
        lock.acquire()
        try:
            logging.debug('Holding')
            time.sleep(0.5)
        finally:
            logging.debug('Not holding')
            lock.release()
        time.sleep(0.5)

def worker(lock):
    logging.debug('Starting worker')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying to acquire')
        have_it = lock.acquire(0)
        try:
            num_tries += 1
            if have_it:
                logging.debug('Iteration %d: Acquired',
                              num_tries)
                num_acquires += 1
            else:
                logging.debug('Iteration %d: Not acquired',
                              num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Done after %d iterations', num_tries)

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

lock = threading.Lock()

holder = threading.Thread(
    target=holder,
    args=(lock,),
    name='holder',
    daemon=True,
)
holder.start()

worker = threading.Thread(
    target=worker,
    args=(lock,),
    name='worker',
)
worker.start()
```

Вывод может выглядеть так:

```bash
(holder    ) Starting holder
(worker    ) Starting worker
(holder    ) Holding
(worker    ) Trying to acquire
(holder    ) Not holding
(worker    ) Iteration 1: Not acquired
(worker    ) Trying to acquire
(holder    ) Holding
(worker    ) Iteration 2: Not acquired
(holder    ) Not holding
(worker    ) Trying to acquire
(worker    ) Iteration 3: Acquired
(holder    ) Holding
(worker    ) Trying to acquire
(worker    ) Iteration 4: Not acquired
(holder    ) Not holding
(worker    ) Trying to acquire
(worker    ) Iteration 5: Acquired
(holder    ) Holding
(worker    ) Trying to acquire
(worker    ) Iteration 6: Not acquired
(holder    ) Not holding
(worker    ) Trying to acquire
(worker    ) Iteration 7: Acquired
(worker    ) Done after 7 iterations
```

Как видно, понадобилось 7 попыток, чтобы установить счетчик.

В ситуациях, когда другой код в том же потоке должен повторно получить блокировку, надо использовать [RLock](https://docs.python.org/3/library/threading.html?highlight=threading#threading.RLock)

`Lock` и `RLock` допускают [использование менеджера контекста](https://docs.python.org/3/library/threading.html?highlight=threading#using-locks-conditions-and-semaphores-in-the-with-statement). Это позволяет не заниматься явной установкой/выпуском блокировки.

```python
import threading

def worker_with(lock):
    with lock:
        print('Lock with')

lock = threading.Lock()
w1 = threading.Thread(target=worker_with, args=(lock,))
w2 = threading.Thread(target=worker_with, args=(lock,))

w1.start()
w2.start()
```

## [Condition](https://docs.python.org/3/library/threading.html?highlight=threading#threading.Condition)

Реализует ожидание одним или несколькими потоками разблокировки другого ресурса. В качестве аргумента принимает `Lock` или `RLock`. В примере ниже два потока освобождаются после выпуска третьего:

```python
import threading
import time

def slave(cond):
    with cond:
        cond.wait()
        print('Im free')

def master(cond):
    with cond:
        print('Wait!')
        cond.notify_all()

condition = threading.Condition()
s1 = threading.Thread(target=slave, args=(condition,))
s2 = threading.Thread(target=slave, args=(condition,))
m = threading.Thread(target=master, args=(condition,))

s1.start()
s2.start()
time.sleep(0.2)
m.start()
```

`wait_for()` реализует ожидание некоего расчетного условия.

## [Barrier](https://docs.python.org/3/library/threading.html?highlight=threading#barrier-objects)

Реализует контрольную точку для заданного количества потоков. Когда поток достигает контрольной точки, он блокируется до тех пор, пока этой же точки не достигнут остальные потоки. Барьер можно использовать повторно любое количество раз для одного и того же количества потоков. `reset()` возвращает барьер в начальное состояние. `abort()` позволяет выполниться заблокированным потокам (полезно, к примеру, когда мы ожидаем блокировки нескольких потоков, но заданное число так и не достигнуто)

Пример из документации:

```python
b = Barrier(2, timeout=5)

def server():
    start_server()
    b.wait()
    while True:
        connection = accept_connection()
        process_server_connection(connection)

def client():
    b.wait()
    while True:
        connection = make_connection()
        process_client_connection(connection)
```

## [Semaphore](https://docs.python.org/3/library/threading.html?highlight=threading#semaphore-objects)

Обеспечивает одновременный доступ к ресурсу нескольким потокам с ограничением их количества, к примеру это может быть сетевой пул, поддерживающий фиксированное число соединений.

## [local](https://docs.python.org/3/library/threading.html?highlight=threading#thread-local-data)

Реализует объекты, доступные только части потоков. Используется для следующих задач:

- сокрытие данных от потоков
- инициализация потоков с одинаковыми значениями

```python
import random
import threading


def show(data):
    try:
        print(data.value)
    except AttributeError:
        print('No value yet')

def worker(data):
    show(data)
    data.value = random.randint(1, 100)
    show(data)


data = threading.local()
show(data)
data.value = 1000
show(data)

for i in range(2):
    t = threading.Thread(target=worker, args=(data,))
    t.start()
```

```shell
No value yet
1000
No value yet
55
No value yet
95
```

В примере видно, что установленная переменаня досутпна только локально, включая основной поток - атрибут `data.value` отсутствует в потоке до утсановки атрибута непосредственно внутри.

[[python-standart-library]]

Смотри еще:

- [[multiprocess]]
- [[asyncio]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[gil]: gil "Gil"
[python-standart-library]: ..%2Flists%2Fpython-standart-library "Стандартная библиотека python и полезные ресурсы"
[multiprocess]: multiprocess "Управление процессами в python"
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"