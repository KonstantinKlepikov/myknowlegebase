---
description: Очереди задач в python с celery
tags: queue python
title: Celery
---
## Intro

[Celery](https://docs.celeryproject.org/en/stable/) это простая, гибкая и надежная распределенная система для обработки большого количества сообщений, предоставляющая операции с инструментами, необходимыми для обслуживания такой системы.

Очереди используются как механизм для распределения работы по потокам или процессам.

Celery использует брокера для посредничества между клиентами и воркерами. Чтобы инициировать задачу, клиент добавляет сообщение в очередь, а затем брокер доставляет это сообщение воркеру.

Система Celery может состоять из нескольких воркеров и брокеров. Celery написан на python, но протокол может быть реализован на любом языке.

Простейший пример приложения.

```python
from celery import Celery

app = Celery('hello', broker='amqp://guest@localhost//')

@app.task
def hello():
    return 'hello world'
```

Celery поддерживает:

- brokers [[redis]], [[rabbitmq]], amazonsqs и [т.д.](https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/index.html#brokers)
- совместная работа обеспечивается через multiprocessing, eventied, gevent, multithreading или solo threading реализации
- поддерживает хранилища: AMQP, Redis, Memcached, SQLAlchemy, Django ORM, Apache Cassandra, Elasticsearch, Riak, MongoDB, CouchDB, Couchbase, ArangoDB, Amazon DynamoDB, Amazon S3, Microsoft Azure Block Blob, Microsoft Azure Cosmos DB, file system
- сериализация: pickle, json, yaml, msgpack, zlib, bzip2, Cryptographic message signing.

Фичи:

- мониторинг событий
- планировщик задач
- планировщик рабочих процессов
- защита от утечки ресурсов
- установка лимитов по времени и скорости
- кастомизируемость

Как инсталить [смотри тут](https://docs.celeryproject.org/en/stable/getting-started/introduction.html#installation). Там же весь набор бандлов для установки бекендов, сериализации, транспорта и т.д.

[introduction](https://docs.celeryproject.org/en/stable/getting-started/introduction.html#celery-is)

## [Быстрый запуск](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#redis)

- Выбираем и ставим транспорт сообщений (брокер)
- ставим Celery и создаем первую задачу
- запуск воркера и вызываем задачу
- отслеживаем задачи по мере их перехода через разные состояния и првоеряем возвращаемые значения

Брокеры: [[rabbitmq]] или [[redis]]

Для редиса можно через [[docker]]: `docker run -d -p 6379:6379 redis`

Ставим celery: `pip install celery`

[Ставим коннектор](https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/redis.html#broker-redis) для [[redis]]: `pip install -U "celery[redis]"`

Пишем апку (в боевых условия нам конечно понадобится сконфигурировать [доступ к redis](https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/redis.html#broker-redis), задав и указав логин/пароль)

```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y
```

Первым аргументом Celery является имя текущего модуля. Это нужно только для того, чтобы имена могли генерироваться автоматически, когда задачи определены в модуле `__main__`. Второй аргумент — это аргумент ключа брокера, указывающий URL-адрес брокера сообщений, который вы хотите использовать.

- для rabbitmq `amqp://localhost`
- для redis `redis://localhost`

Стартуема сервер из папки приложения: `celery -A tasks worker --loglevel=INFO` В данном случае сервак запускается в лоб. В реальности нужен демон - [смотри тут](https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#daemonizing)

Тада:

```shell
 -------------- celery@pop-os v5.2.3 (dawn-chorus)
--- ***** -----
-- ******* ---- Linux-5.8.0-7630-generic-x86_64-with-glibc2.32 2022-01-17 23:32:33
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x7fdfe7e14a60
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 12 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . tasks.add

[2022-01-17 23:32:33,390: INFO/MainProcess] Connected to redis://localhost:6379/0
[2022-01-17 23:32:33,394: INFO/MainProcess] mingle: searching for neighbors
[2022-01-17 23:32:34,401: INFO/MainProcess] mingle: all alone
[2022-01-17 23:32:34,440: INFO/MainProcess] celery@pop-os ready.
```

Хелпы: `celery worker --help` и `celery --help`

Для вызова тасков можно использовать метод delay().

```python
>>> from tasks import add
>>> add.delay(4, 4)
```

Теперь задача обработана воркером, назначенным ранее. Вы можете убедиться в этом в консоли. Вызов задачи возвращает экземпляр AsyncResult. Это можно использовать для проверки состояния задачи, ожидания завершения задачи или получения возвращаемого значения (или, если задача не удалась, для получения исключения и обратной трассировки). Результаты не включены по умолчанию. Чтобы выполнять удаленные вызовы процедур или отслеживать результаты задач в базе данных, вам необходимо настроить Celery для использования серверной части результатов.

```shell
[2022-01-18 00:02:45,633: INFO/MainProcess]
Task tasks.add[9e31d371-cb34-4e76-b559-b2e92f612c7d] received
[2022-01-18 00:02:45,634: INFO/ForkPoolWorker-8]
Task tasks.add[9e31d371-cb34-4e76-b559-b2e92f612c7d] succeeded in 0.00025742400612216443s: 8
```

Чтобы получить результат - его надо где-то хранить или куда-то отправить. На выбор куча бекендов под эти задачи, включая реляционыне базы данных и в т.ч. редис.

В [этом примере](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#keeping-results) используется rpc. Бекенд задается через аргумент при создании экземпляра воркера или через конфиг, например так:

```python
app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')
```

Теперь задача ставится в очередь, а результат отправляется на бекенд как только будет посчитан. Отправка осуществляется в асинхронном режиме. [Подробнее про бекенды](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-result-backends)

Конфигурация celery - нужно сконфигурировать брокера и сконфигурировать бекенд. Про конфиги и дефолты [читай тут](https://docs.celeryproject.org/en/stable/userguide/configuration.html#configuration). Хорошей практикой является создание конфига `celeryconfig.py` и вызов конфигурации в app через `app.config_from_object('celeryconfig')`

Пример конфига:

```python
broker_url = 'pyamqp://'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
```

Поддерживается формат в виде словаря. Отвалидировать конфиг можно так: `python -m celeryconfig`. Естественно можно создавать множество конфигов называя их как угодно для использования в разных приложениях celery

## [Более подробный пример](https://docs.celeryproject.org/en/stable/getting-started/next-steps.html)

- Using Celery in your Application
- Calling Tasks
- Canvas: Designing Work-flows
- Routing
- Remote Control
- Timezone
- Optimization

### Создание воркеров и тасков

В примере разбирается проект с такой структурой:

```shell
proj/__init__.py
    /celery.py
    /tasks.py
```

`celery.py`

```python
from celery import Celery

app = Celery('proj',
             broker='amqp://',
             backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
```

В данном случае в качестве брокера задан [[rabbitmq]], Бекендом является rpc, а в include мы прописываем путь к таскам - это необходимо, чтобы воркер знал где их искать после старта. Название воркера может не совпадать с названием содержащего фолдера.

`tasks.py`

```python
from .celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
```

### Два режима запуска

Стуртуем воркера снаружи `proj` вот так: `celery -A proj worker -l INFO`. В данном режиме воркер запускается локально на одной ноде.

Аргумент `--app` (`-A`) указывает используемый экземпляр приложения Celery в виде `module.path:attribute`. Но он также поддерживает форму быстрого доступа. Если указано только имя пакета, он попытается найти экземпляр приложения в следующем порядке:

С `--app=proj` - атрибут с именем `proj.app`, или атрибут с именем `proj.celery`, или любой атрибут в модуль `proj`, где значением является приложение Celery, или если ничего из этого не найдено, он попытается использовать подмодуль с именем `proj.celery` и найти в нем атрибут с именем `proj.celery.app`, или атрибут с именем `proj.celery.celery`, или любой атрибут в модуле `proj.celery`, где значением является приложение Celery. Эта схема имитирует приемы, используемые в документации, то есть `proj:app` для одного автономного модуля и `proj.celery:app` для более крупных проектов.

Видим что-то типа этого:

```shell
--------------- celery@halcyon.local v4.0 (latentcall)
--- ***** -----
-- ******* ---- [Configuration]
- *** --- * --- . broker:      amqp://guest@localhost:5672//
- ** ---------- . app:         __main__:0x1012d8590
- ** ---------- . concurrency: 8 (processes)
- ** ---------- . events:      OFF (enable -E to monitor this worker)
- ** ----------
- *** --- * --- [Queues]
-- ******* ---- . celery:      exchange:celery(direct) binding:celery
--- ***** -----

[2012-06-08 16:23:51,078: WARNING/MainProcess] celery@halcyon.local has started.
```

Здесь `broker` - это юрл к нашему брокеру. `concurrency`  определяет сколько доступно ядер. `events` это параметр, который заставляет Celery отправлять сообщения мониторинга (события) для действий, происходящих в воркере. Они могут использоваться программами мониторинга, такими как [[flower]]. `queues` это список доступных очередей, из которых процессы будут потреблять задачи. Это важный аспект, т.к. главный поинт в том, чтобы расписать из каких очередей что потреблять и в каком приоритете. Это делается через [маршрутизацию](https://docs.celeryproject.org/en/stable/userguide/routing.html#guide-routing).

В текущем режиме воркера можно остановить через `ctrl-c`. В реальных условиях воркеров потребуется запускать в фоне - [читай руководство по "демонизации"](https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#daemonizing). Вкратце - celery использует общие init-скрипты для всех воркеров и они должны работать на всех юникс-подобных платформах. Начальным скриптом является `/etc/default/celeryd`. Для его запуска требуются привилегии суперюзера (от которого конечно ни при каких условиях запускаться нельзя ввиду небезопасности структур данных, используемых в celery). К счастью реализован запуск через `celery multy`, которому рут-права не нужны. Выглядит это примерно так:

```bash
$ celery multi start w1 -A proj -l INFO
celery multi v4.0.0 (latentcall)
> Starting nodes...
    > w1.halcyon.local: OK
```

```bash
$ celery  multi restart w1 -A proj -l INFO
celery multi v4.0.0 (latentcall)
> Stopping nodes...
    > w1.halcyon.local: TERM -> 64024
> Waiting for 1 node.....
    > w1.halcyon.local: OK
> Restarting node w1.halcyon.local: OK
celery multi v4.0.0 (latentcall)
> Stopping nodes...
    > w1.halcyon.local: TERM -> 64052
```

Запущенный в фоне воркер не помнит контекеста, поэтому все переданные ему аругменты командной строки необходимо передавать каждый раз при каждой команде (wtf). Остановить можно через `multi stop`, но надо понить, что такая остановка будет синхронной, что может привести к незавершению ряда задач. Для асинхронного стопа использовать `stopwait`

Вот так на самом деле придется запускать воркеров (создавая разделы для логов, чтобы не возникли ошибки `IOError: [Errno 13] Permission denied`):

```python
$ mkdir -p /var/run/celery
$ mkdir -p /var/log/celery
$ celery multi start w1 -A proj -l INFO --pidfile=/var/run/celery/%n.pid \
                                        --logfile=/var/log/celery/%n%I.log
```

Кроме того. возможны ошибки с пермишеном к логам. Надо передать права. Смотри [тут](https://stackoverflow.com/questions/28825760/celery-not-running-permission-denied/28826090) и [тут](https://stackoverflow.com/questions/22736808/celery-daemon-permission-denied-on-log-file)

### Вызов тасков

Вызов тасков делается, как писалось выше, через `sig.delay(*args, **kwargs)`, котопый является оберткой для `sig.apply_async(args=(), kwargs={}, **options)`, получающий больше конфигурационных аргументов (например название очереди или значение колдауна).

Если реализован бекенд, то результат можно получить через `get()`. Поддерживаются атрибуты, дающие доступ к состояниям:

```python
>>> res = add.delay(2, 2)
>>> res.get(timeout=1)
4
>>> res.id
d6b3aea2-fb9b-4ebc-8da4-848818db9114
>>> res.failed()
False
>>> res.successful()
True
```

Если что-то пошло не так, будет поднята ошибка, избежать пропогейта которой можно так:

```python
>>> res.get(propagate=False)
TypeError("unsupported operand type(s) for +: 'int' and 'str'")
```

Таск проходит через три состояния (на самом деле состояние таска может меняться произволяно и SUCCESS не окончательный): PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS. Извлечь можно так:

```python
>>> res.state
'FAILURE'
```

Состояние STARTED появляется только если таск инициализирвоан через декоратор `@task(track_started=True)`, а PENDING просто определяет неопределенное состояние (дефолтное). [Про статусы подробно](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-states)

### Work-flow

Для построения сложных конструкций в Celery предусмотрены сигнатуры (signature). Сигнатура упаковывает таск и аргументы полностью или частично для передачи всего этого как объекта дрвгим таскам или для сериализации.

```python
>>> add.signature((2, 2), countdown=10)
tasks.add(2, 2)
```

сокращенный вариант:

```python
>>> s1 = add.s(2, 2)
>>> res = s1.delay()
>>> res.get()
4
```

частичная передача аргументов:

```python
# incomplete partial: add(?, 2)
>>> s2 = add.s(2)
# resolves the partial: add(8, 2)
>>> res = s2.delay(8)
>>> res.get()
10
```

### Примитивы

Все примитивы поддерживают частичные аргументы и могут быть скомбинированы между собой в любом порядке.

#### Groups

```python
>>> from celery import group
>>> from proj.tasks import add

>>> g = group(add.s(i, i) for i in range(10))
>>> g().get()
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

#### Chains

```python
>>> from celery import chain
>>> from proj.tasks import add, mul

# (4 + 4) * 8
>>> chain(add.s(4, 4) | mul.s(8))().get()
64
```

Короткий вариант записи

```python
>>> (add.s(4, 4) | mul.s(8))().get()
64
```

#### Chords

```python
>>> from celery import chord
>>> from proj.tasks import add, xsum

>>> chord((add.s(i, i) for i in range(10)), xsum.s())().get()
90
```

Если группа чейнится в другой таск, она автоматически конверстится в чорд:

```python
>>> (group(add.s(i, i) for i in range(10)) | xsum.s())().get()
90
```

Больше конструкций и подробности [смотри тут](https://docs.celeryproject.org/en/stable/userguide/canvas.html#guide-canvas)

### Routing

Определять очереди можно как в конфигах, непосредственно в тасках или через cli:

```python
app.conf.update(
    task_routes = {
        'proj.tasks.add': {'queue': 'hipri'},
    },
)
```

или

```python
>>> from proj.tasks import add
>>> add.apply_async((2, 2), queue='hipri')
```

### [Remote control](https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#remote-control)

Через `celery -A proj inspect` и `celery -A control`. К примеру все активные воркеры: `celery -A proj inspect active`

## [user guide](https://docs.celeryproject.org/en/stable/userguide/index.html)

### [Application](https://docs.celeryproject.org/en/stable/userguide/application.html)

Вначале необходимо инициализировать экземпляр celery. Этот объект является потокобезопасным, так что несколько приложений Celery с разными конфигурациями, компонентами и задачами могут сосуществовать в одном и том же пространстве процессов.

```python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```

Здесь имеется название, название модуля и адрес в памяти, но значение имеет только имя модуля, т.к. селери общается с помощью меседжей, которые не содержат кода, а содержат только имена тасков, которые необходимо вызвать. Задачи добавояются в локальный регистр задач:

```python
>>> @app.task
... def add(x, y):
...     return x + y

>>> add
<@task: __main__.add>

>>> add.name
__main__.add

>>> app.tasks['__main__.add']
<@task: __main__.add>
```

Когда celery не может определить к какому модуля принадлэеит функция, он использует `__main__`. Эта ситуация возникает при вызове модуля, в котором определена задача, как программы или через терминал python. Но при импорте это будет выглядеть иначе:

```python
>>> from tasks import add
>>> add.name
tasks.add
```

В конечном итоге имя основного модуля можно указать непосредственно, тогда в вызове из `__main__` все будет ок

```python
>>> app = Celery('tasks')
>>> app.main
'tasks'

>>> @app.task
... def add(x, y):
...     return x + y

>>> add.name
tasks.add
```

#### [Configuration](https://docs.celeryproject.org/en/stable/userguide/application.html#configuration) приложения

Конфиг доступен через атрибут `app.conf`

```python
>>> app.conf.timezone
'Europe/London'
```

можно задать значения напрямую

```python
>>> app.conf.enable_utc = True
```

или через апдейт сразу нескольких атрибутов

```python
>>> app.conf.update(
...     enable_utc=True,
...     timezone='Europe/London',
... )
```

Другие способы (к примеру из ф-ла, переменных окружения или из конфигурационного класса) смотри [в доке](https://docs.celeryproject.org/en/stable/userguide/application.html#config-from-object).

Запретить вывод в отладку определененых конфигов [можно так](https://docs.celeryproject.org/en/stable/userguide/application.html#censored-configuration).

[Список доступных конфигов](https://docs.celeryproject.org/en/stable/userguide/configuration.html#configuration)

#### [Laziness](https://docs.celeryproject.org/en/stable/userguide/application.html#laziness)

Экземпляр приложения является ленивым (laziness), то есть он не будет извлекаться до тех пор, пока он действительно не понадобится.

`app.task()` декораторы не создают задачи в тот момент, когда задача определена, вместо этого они откладывают создание задачи до того момента, как она будет использована, или после того, как приложение celery будет финализировано/

Финализация приложения происходит или явно путем вызова `app.finalize()` или неявно, путем доступа атрибуту таска приложения. При финализации задачи, которые должны быть разделены между приложениями, корпиуются, оцениваются все декораторы задач, происходит сверка принадлежности задач приложению.

#### [Breaking the chain](https://docs.celeryproject.org/en/stable/userguide/application.html#breaking-the-chain)

Здесь объясняется как правильно передавать экземпляры приложений другим объектам.

#### [Абстрактные задачи](https://docs.celeryproject.org/en/stable/userguide/application.html#abstract-tasks)

Объясняется как создавать задачи из других базовых классов кроме `Task`

### [Tasks](https://docs.celeryproject.org/en/stable/userguide/tasks.html)

Задача - это класс, который можно сконструировать из любого вызываемого объекта. Он выполняет двойную роль: определяет что происходит при вызове задачи (отправляет сообщение), и что происходит, когда воркер получает это сообщение.

Каждый класс задач имеет уникальное имя, и на это имя ссылаются в сообщениях, чтобы воркер мог найти нужную функцию для выполнения.

Сообщение таска не удаляется из очереди, пока это сообщение не будет подтверждено воркером. Воркер может заранее зарезервировать множество сообщений, и даже если он прекратит существовать - из-за сбоя питания или по какой-либо другой причине - сообщение будет повторно доставлено другому воркеру.

В идеале функции тасков должны быть идемпотентными: это означает, что **функция не будет вызывать непредвиденных эффектов, даже если вызывается несколько раз с одними и теми же аргументами**. Поскольку рабочий процесс не может определить, являются ли ваши таски идемпотентными, поведение по умолчанию заключается в том, чтобы заранее подтвердить сообщение, непосредственно перед его выполнением. Тогда вызов таска, который уже был запущен, никогда не выполнялся снова.

Если ваша задача идемпотентна, вы можете установить опцию `acks_late`, чтобы вместо этого воркер подтвердил сообщение после того, как задача вернется.

Воркер подтвердит сообщение, если дочерний процесс, выполняющий задачу, будет завершен (либо задачей, вызывающей `sys.exit()`, либо сигналом), даже если `acks_late` включен. Такое поведение выполнено преднамеренно, поскольку:

- мы не хотим повторно запускать таски, которые заставляют ядро отправлять SIGSEGV (ошибка сегментации) или аналогичные сигналы процессу
- мы предполагаем, что системный администратор, намеренно завершающий задачу, не хочет ее автоматического перезапуска
- таск, который выделяет слишком много памяти, рискует скрашить ядро, то же самое может произойти снова
- таск, который всегда завершается ошибкой при повторной доставке, может вызвать высокочастотный цикл передачи сообщений, приводящий к остановке системы.

Если вы действительно хотите, чтобы задача была повторно доставлена в этих сценариях, вам следует рассмотреть возможность включения параметра `task_reject_on_worker_lost`.

Если для текущего таска не нужны результаты, их можно отключить через декоратор `@task(ignore_result=True)`

#### [Базовое использование](https://docs.celeryproject.org/en/stable/userguide/tasks.html#basics)

```python
from .models import User

@app.task(serializer='json')
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

В данном случае при создании таска использовалась опция serializer - смотри [список опций для тасков](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-options).

[Bound task](https://docs.celeryproject.org/en/stable/userguide/tasks.html#bound-tasks) - это такие таски, в которых первый аргумент это всегда инстанс таска (self), так же как в методах python. Связанные задачи необходимы для повторных попыток (с помощью `app.Task.retry()`), для доступа к информации о текущем запросе задачи и для любых дополнительных функций, которые вы добавляете в базовые классы пользовательских задач.

```python
logger = get_task_logger(__name__)

@app.task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)
```

Возможно наследование таска от базового класса при помощи аргумента декоратора `base`

```python
import celery

class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@app.task(base=MyTask)
def add(x, y):
    raise KeyError()
```

#### Name

У каждого таска должно быть уникальное имя. Если имя не задано - оно будет сгенерировано из имени модуля и имени функции

Лучшая практика - использовать имя модуля как неймспейс для имени таска, чтобы избежат ьконфликта имен. В данном случае задано такое же имя, какое могло бы быть сгенерировано автоматически для таска, заданного в модуле `tasks.py`

```python
>>> @app.task(name='tasks.add')
>>> def add(x, y):
...     return x + y

>>> add.name
'tasks.add'
```

Вопрос автонейминга и релятивного импорта описан [тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#automatic-naming-and-relative-imports). Как менять схему автонейминга описано [тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#changing-the-automatic-naming-behavior).

#### Task request

[Запрос задачи](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-request) осуществляется через `app.Task.request`, который содержит информацию и состояние текущего таска. Подробнее об атрибутах запрсоа смотри [в доке](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-request). Пример:

```python
@app.task(bind=True)
def dump_context(self, x, y):
    print(
        'Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request)
        )
```

#### Logging

Воркер может автоматически логировать данные. Это можно настроить вручную. [Подробнее](https://docs.celeryproject.org/en/stable/userguide/tasks.html#logging). Лучшая практика - создать простой логгер для всех тасков в модуле:

```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y
```

Селери использует стандартную питоню библиотеку для логирования. [[python-logging]]

#### Args check

Реализована стандартная для python проверка аргументво таска, которую [можно отключить](https://docs.celeryproject.org/en/stable/userguide/tasks.html#argument-checking). Кроме того, конфиденциальную информацию аргументво [можно скрывать](https://docs.celeryproject.org/en/stable/userguide/tasks.html#hiding-sensitive-information-in-arguments).

#### Retrying

`app.Task.retry()` используется для повтороного извлечения таска, например в случае ошибки. В этом случае будет оправлено новое сообщение с тем же идентификатором, чтобы сообщение было поставлено в туже очередь, что и исходная задача. [Подробнее](https://docs.celeryproject.org/en/stable/userguide/tasks.html#retrying)

```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```

Что еще доступно:

- [пользовательская задержка повтора](https://docs.celeryproject.org/en/stable/userguide/tasks.html#using-a-custom-retry-delay)
- [автоматический повтор](https://docs.celeryproject.org/en/stable/userguide/tasks.html#automatic-retry-for-known-exceptions) для известных исключений

Подробнее читай [в доке](https://docs.celeryproject.org/en/stable/userguide/tasks.html#retrying).

#### Состояния

Celery может [хранить состояние текущего таска](https://docs.celeryproject.org/en/stable/userguide/tasks.html#states) - это результат задачи или поднятая ошибка. Реализовано несколько бекендов для резалтов, [Смотри чем они отличаются тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-result-backends). Про [настройку бекендов](https://docs.celeryproject.org/en/stable/userguide/configuration.html#conf-result-backend). Про [бекенды в целом](https://docs.celeryproject.org/en/stable/userguide/tasks.html#result-backends).

За время своего существования задача будет проходить через несколько возможных состояний, и к каждому состоянию могут быть присоединены произвольные метаданные. Когда задача переходит в новое состояние, о предыдущем состоянии будет забыть, но некоторые переходы можно вывести (например, FAILED подразумевается, что задача, находящаяся сейчас в состоянии, находилась в STARTED состоянии в какой-то момент).

Существуют также наборы состояний, такие как набор FAILURE_STATES и набор READY_STATES.

Клиент использует членство в этих наборах, чтобы решить, следует ли повторно инициировать исключение (PROPAGATE_STATES) или можно ли кэшировать состояние.

Кроме торго, можно определить [пользовательские состояния](https://docs.celeryproject.org/en/stable/userguide/tasks.html#custom-states). Встреонные статусы [описаны тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#built-in-states)

#### Полупредикаты

Можно поднять несколько экцепшенов, которые [обеспечат определенное поведение воркера](https://docs.celeryproject.org/en/stable/userguide/tasks.html#semipredicates) для записи финального состояния. Это позволяет игнорить или отклонять таски. Реализовано:

- Ignore
- Reject
- Retry

```python
from celery.exceptions import Ignore

@app.task(bind=True)
def some_task(self):
    if redis.ismember('tasks.revoked', self.request.id):
        raise Ignore()
```

Кроме того, можно задавать [кастомные классы](https://docs.celeryproject.org/en/stable/userguide/tasks.html#custom-task-classes) для тасков, отнаследовавшись от базового `Task`

Можно [игнорить резалт таска](https://docs.celeryproject.org/en/stable/userguide/tasks.html#ignore-results-you-don-t-want), если он неважен. Есть и другие способы [оптимизировать производительность](https://docs.celeryproject.org/en/stable/userguide/optimizing.html#guide-optimizing).

Если нужно организовать таски последовательно, это может привести к непредвиденным задержкам в выполнении цепочки. Лучше организовать цепочку [асинхронно](https://docs.celeryproject.org/en/stable/userguide/tasks.html#avoid-launching-synchronous-subtasks).

Пример (плохо)

```python
@app.task
def update_page_info(url):
    page = fetch_page.delay(url).get()
    info = parse_page.delay(url, page).get()
    store_page_info.delay(url, info)

@app.task
def fetch_page(url):
    return myhttplib.get(url)

@app.task
def parse_page(page):
    return myparser.parse_document(page)

@app.task
def store_page_info(url, info):
    return PageInfo.objects.create(url, info)
```

С использованием сейна тасков (хорошо):

```python
def update_page_info(url):
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain()

@app.task()
def fetch_page(url):
    return myhttplib.get(url)

@app.task()
def parse_page(page):
    return myparser.parse_document(page)

@app.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)
```

#### [Стратегии повышения производительности](https://docs.celeryproject.org/en/stable/userguide/tasks.html#performance-and-strategies)

#### [Пример использования тасков для фильтрации спама на джанго тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-example)

### [Как вызывать таски](https://docs.celeryproject.org/en/stable/userguide/calling.html)

#### Базавые принципы

`T.delay(arg, kwarg=value)`
Star arguments shortcut to .apply_async. (.delay(*args, **kwargs) calls .apply_async(args, kwargs)).

`T.apply_async((arg,), {'kwarg': value})`

`T.apply_async(countdown=10)`
выполняется через 10 секунд

`T.apply_async(eta=now + timedelta(seconds=10))`
выполняется через 10 секунд, указанный с помощью eta

`T.apply_async(countdown=60, expires=120)`
выполняется через одну минуту, но истекает через 2 минуты

`T.apply_async(expires=now + timedelta(days=2))`
истекает через 2 дня, устанавливается с помощью datetime.

В большинстве случаев используется `delay()`, но если нужны дополнительные опции, то `apply_async`. Еще один способ - вызвать через signature, вот так: `task.s(arg1, arg2, kwarg1='x', kwargs2='y').apply_async()`. Читай про [построение воркфлоу через signature](https://docs.celeryproject.org/en/stable/userguide/canvas.html)

Все примеры ниже для этой функции

```python
@app.task
def add(x, y):
    return x + y
```

#### Linking (callbacks/errbacks)

Поддерживаются [слинкованные таски](https://docs.celeryproject.org/en/stable/userguide/calling.html#linking-callbacks-errbacks), так что одна задача следует за другой. Задача обратного вызова будет применяться с результатом родительской задачи в качестве частичного аргумента:

```python
add.apply_async((2, 2), link=add.s(16))
```

Если таск поднимает исключение, можно вызвать [колбек напрямую](https://docs.celeryproject.org/en/stable/userguide/calling.html#linking-callbacks-errbacks)

Кроме того, Celery поддерживает перехват всех изменений состояния, [устанавливая обратный вызов on_message](https://docs.celeryproject.org/en/stable/userguide/calling.html#on-message).

#### [ETA and Countdown](https://docs.celeryproject.org/en/stable/userguide/calling.html#eta-and-countdown)

Поддерживается [установка](https://docs.celeryproject.org/en/stable/userguide/calling.html#eta-and-countdown) времени срабатывания и ожидаемого времени выполнения

```python
>>> result = add.apply_async((2, 2), countdown=3)
>>> result.get()    # не раньше чем через 3 секунды
20
```

ETA (расчетное время прибытия) позволяет установить конкретную дату и время, которые являются самым ранним временем выполнения задачи. Eta должен быть datetime объектом, указывающим точную дату и время (включая точность в миллисекундах и информацию о часовом поясе)

```python
>>> from datetime import datetime, timedelta

>>> tomorrow = datetime.utcnow() + timedelta(days=1)
>>> add.apply_async((2, 2), eta=tomorrow)
```

#### Expiration

Аргумент expires определяет необязательное время истечения срока действия, либо в секундах после публикации задачи, либо в определенную дату и время, используя datetime. Когда рабочий процесс получает задачу с истекшим сроком действия, он помечает задачу как REVOKED(TaskRevokedError).

```python
>>> # Task expires after one minute from now.
>>> add.apply_async((10, 10), expires=60)

>>> # Also supports datetime
>>> from datetime import datetime, timedelta
>>> add.apply_async((10, 10), kwargs,
...                 expires=datetime.now() + timedelta(days=1)
```

#### Повторная отправка

Celery будет автоматически повторять отправку сообщений в случае сбоя подключения, а поведение повторных попыток [можно настроить](https://docs.celeryproject.org/en/stable/userguide/calling.html#message-sending-retry)

#### [Обработка ошибок соединения с транспортом](https://docs.celeryproject.org/en/stable/userguide/calling.html#connection-error-handling)

#### [Serializers](https://docs.celeryproject.org/en/stable/userguide/calling.html#serializers)

Данные, передаваемые между клиентами и работниками, должны быть сериализованы, поэтому каждое сообщение в Celery имеет content_type заголовок, описывающий метод сериализации, используемый для его кодирования.

#### [Compression](https://docs.celeryproject.org/en/stable/userguide/calling.html#compression)

#### [Connections](https://docs.celeryproject.org/en/stable/userguide/calling.html#connections)

Соединения можно обрабатывать вручную, создавая паблишеров.

Смотри еще [перенаправление задач в разные очереди](https://docs.celeryproject.org/en/stable/userguide/calling.html#routing-options) и как [отклонять результаты задач](https://docs.celeryproject.org/en/stable/userguide/calling.html#results-options).

### [Canvas: Designing Work-flows](https://docs.celeryproject.org/en/stable/userguide/canvas.html)

В разделе перечисляются примитивы и конструкции для signatures и как собирать асинхронные цепочки выполнения тасков.

### [Workers](https://docs.celeryproject.org/en/stable/userguide/workers.html#workers-guide)

Самый простой способ запустить воркера - `celery -A proj worker -l INFO`

Можно запускать множество воркеров, при этом обязательно указание имени узла

```shell
celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker3@%h
```

Воркера можно [завершить](https://docs.celeryproject.org/en/stable/userguide/workers.html#stopping-the-worker) или [рестартнуть](https://docs.celeryproject.org/en/stable/userguide/workers.html#restarting-the-worker). Все остальное (совместная работа, управление и т.д.) смотри в [документации](https://docs.celeryproject.org/en/stable/userguide/workers.html#workers-guide)

### [Запуск демонов](https://docs.celeryproject.org/en/stable/userguide/daemonizing.html)

### [Периодически запускаемые таски](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)

В разделе рассматривается работа celery beat - планировщика, запускающего таски через равные промежутки времени.

### [Routing Tasks](https://docs.celeryproject.org/en/stable/userguide/routing.html)

Рассматривается автоматическое и ручное распределение по очередям и некотоыре опции.

### [Monitoring and Management Guide](https://docs.celeryproject.org/en/stable/userguide/monitoring.html)

В том числе про [[flower]]

### [Security](https://docs.celeryproject.org/en/stable/userguide/security.html)

### [Optimizing](https://docs.celeryproject.org/en/stable/userguide/optimizing.html)

### [Debugging](https://docs.celeryproject.org/en/stable/userguide/debugging.html)

### [Concurrency](https://docs.celeryproject.org/en/stable/userguide/concurrency/index.html)

### [Signals](https://docs.celeryproject.org/en/stable/userguide/signals.html)

### [Testing with Celery](https://docs.celeryproject.org/en/stable/userguide/testing.html)

### [Extensions and Bootsteps](https://docs.celeryproject.org/en/stable/userguide/extending.html)

### [Configuration and defaults](https://docs.celeryproject.org/en/stable/userguide/configuration.html)

Смотри queueеще:

- [документация cli celery](https://docs.celeryproject.org/en/stable/reference/cli.html?highlight=command)
- [celery cli](https://docs.celeryq.dev/en/stable/reference/cli.html)
- [[redis]]
- [[rabbitmq]]
- [[apache-kafka]]
- [[flower]] дашборд для мониторинга тасков в celery
- [[asyncio]]
- [[fastapi]]
- [Working example of celery with mongo DB](https://stackoverflow.com/questions/15740755/working-example-of-celery-with-mongo-db) бекенд celery на [[mongodb]]
- [Where should I put the Celery configuration file?](https://stackoverflow.com/questions/53318596/where-should-i-put-the-celery-configuration-file)
- [How can I trigger tasks from another task in Python Celery?](https://stackoverflow.com/questions/15887081/how-can-i-trigger-tasks-from-another-task-in-python-celery)

Более простой аналог: [[python-rq]]

## Celery и [[fastapi]]

Самый простой пример [тут](https://testdriven.io/blog/fastapi-and-celery/) ([ссылка на репо](https://github.com/testdrivenio/fastapi-celery/tree/master/project))

Здесь более подробный пример реализации [[fastapi]], celery и [[poetry]]

Большой подробный курс на testdriven.io: [The Definitive Guide to Celery and FastAPI](https://testdriven.io/courses/fastapi-celery/intro/) (используется [[docker-compose]]) - в данном примере все запихивают в один контейнер.

[Celery Asynchronous Task Queues with Flower & FastAPI](https://medium.com/thelorry-product-tech-data/celery-asynchronous-task-queue-with-fastapi-flower-monitoring-tool-e7135bd0479f)

## Еще статьи

- [How to combine Celery with asyncio?](https://stackoverflow.com/questions/39815771/how-to-combine-celery-with-asyncio)

[//begin]: # "Autogenerated link references for markdown compatibility"
[redis]: redis "Redis"
[rabbitmq]: rabbitmq "Rabbitmq"
[docker]: ../lists/docker "Docker"
[flower]: flower "Flower дашборд для мониторинга celery"
[python-logging]: ../lists/python-logging "Python logging"
[apache-kafka]: apache-kafka "Apache kafka"
[asyncio]: asyncio "Asyncio"
[fastapi]: fastapi "Fastapi"
[mongodb]: mongodb "MongoDB"
[python-rq]: python-rq "Python-rq"
[poetry]: poetry "Poetry"
[docker-compose]: docker-compose "Docker compose"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[redis]: redis "Redis"
[rabbitmq]: rabbitmq "Rabbitmq"
[rabbitmq]: rabbitmq "Rabbitmq"
[redis]: redis "Redis"
[docker]: ../lists/docker "Docker"
[redis]: redis "Redis"
[rabbitmq]: rabbitmq "Rabbitmq"
[flower]: flower "Flower дашборд для мониторинга celery"
[python-logging]: ../lists/python-logging "Python logging"
[flower]: flower "Flower дашборд для мониторинга celery"
[redis]: redis "Redis"
[rabbitmq]: rabbitmq "Rabbitmq"
[flower]: flower "Flower дашборд для мониторинга celery"
[asyncio]: asyncio "Asyncio"
[fastapi]: fastapi "Fastapi"
[python-rq]: python-rq "Python-rq"
[fastapi]: fastapi "Fastapi"
[fastapi]: fastapi "Fastapi"
[poetry]: poetry "Poetry"
[docker-compose]: docker-compose "Docker compose"
[//end]: # "Autogenerated link references"