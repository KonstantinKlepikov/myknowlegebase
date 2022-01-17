---
description: Очередь задач в python с помощью celery
---
# Celery

## Intro

[Celery](https://docs.celeryproject.org/en/stable/) is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system.

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

Для редиса можно черех [[docker]]: `docker run -d -p 6379:6379 redis`

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

Поддерживается формат в виде слвоаря. Отвалидировать конфиг можно так: `python -m celeryconfig`. Естественно можно создавать множество конфигов называя их как угодно для использования в разных приложениях celery

Более подробный пример [реализован тут](https://docs.celeryproject.org/en/stable/getting-started/next-steps.html) и включает:

- Using Celery in your Application
- Calling Tasks
- Canvas: Designing Work-flows
- Routing
- Remote Control
- Timezone
- Optimization

## [user guide](https://docs.celeryproject.org/en/stable/userguide/index.html)

### [Application](https://docs.celeryproject.org/en/stable/userguide/application.html)

```python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```

Значение имеет main имя модуля, т.к. селери общается с помощью меседжей. Извлекается имя таска для того чтобы каждый воркер знал к какой функции ему образщаться.

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

Мы можем извлечь имя в main к примеру для tasks.py

```python
from celery import Celery
app = Celery()

@app.task
def add(x, y): return x + y

if __name__ == '__main__':
    app.worker_main()
```

Но при импорте это будет выглядеть иначе:

```python
>>> from tasks import add
>>> add.name
tasks.add
```

Кроме того, имя main модуля можно задать нгепосредственно

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

#### [Configuration](https://docs.celeryproject.org/en/stable/userguide/application.html#configuration)

Конфиг доступен через `app.conf`

```python
>>> app.conf.timezone
'Europe/London'
```

можно задать значения напрямую

```python
>>> app.conf.enable_utc = True
```

или через апдейт сразу нескольких

```python
>>> app.conf.update(
...     enable_utc=True,
...     timezone='Europe/London',
...)
```

Другие способы (к примеру из ф-ла, переменных окружения или из конфигурационного класса) см. в доке. Как правильно писать таски и использовать абстрактные таски для создания собственных, [смотри тут](https://docs.celeryproject.org/en/stable/userguide/application.html#laziness).

### [Tasks](https://docs.celeryproject.org/en/stable/userguide/tasks.html)

ЗNfcr - это класс, который можно сконструировать из любого вызываемого объекта. Он выполняет двойную роль: определяет что происходит при вызове задачи (отправляет сообщение), и что происходит, когда воркер получает это сообщение.

Каждый класс задач имеет уникальное имя, и на это имя ссылаются в сообщениях, чтобы воркер мог найти нужную функцию для выполнения.

Сообщение таска не удаляется из очереди, пока это сообщение не будет подтверждено воркером. Воркер может заранее зарезервировать множество сообщений, и даже если он прекратит существовать - из-за сбоя питания или по какой-либо другой причине - сообщение будет повторно доставлено другому воркеру.

В идеале функции тасков должны быть идемпотентными: это означает, что **функция не будет вызывать непредвиденных эффектов, даже если вызывается несколько раз с одними и теми же аргументами**. Поскольку рабочий процесс не может определить, являются ли ваши таски идемпотентными, поведение по умолчанию заключается в том, чтобы заранее подтвердить сообщение, непосредственно перед его выполнением. Тогда вызов таска, который уже был запущен, никогда не выполнялся снова.

Если ваша задача идемпотентна, вы можете установить опцию acks_late, чтобы вместо этого воркер подтвердил сообщение после того, как задача вернется.

Обратите внимание, что воркер подтвердит сообщение, если дочерний процесс, выполняющий задачу, будет завершен (либо задачей, вызывающей sys.exit (), либо сигналом), даже если acks_late включен. Такое поведение преднамеренно, поскольку мы не хотим повторно запускать таски, которые заставляют ядро ​​отправлять SIGSEGV (ошибка сегментации) или аналогичные сигналы процессу ... и мы предполагаем, что системный администратор, намеренно завершающий задачу, не хочет ее автоматического перезапуска.

Таск, который выделяет слишком много памяти, рискует скрашить ядро, то же самое может произойти снова. Таск, который всегда завершается ошибкой при повторной доставке, может вызвать высокочастотный цикл передачи сообщений, приводящий к остановке системы.

Если вы действительно хотите, чтобы задача была повторно доставлена ​​в этих сценариях, вам следует рассмотреть возможность включения параметра task_reject_on_worker_lost.

#### [Базовые принципы](https://docs.celeryproject.org/en/stable/userguide/tasks.html#basics)

```python
@app.task(serializer='json')
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

В данном случае при создании таска использовалась [опция](https://docs.celeryproject.org/en/stable/userguide/tasks.html#list-of-options) - смотри список опций для тасков.

[Bound task](https://docs.celeryproject.org/en/stable/userguide/tasks.html#bound-tasks) - это такие таски, в которых первый аргумент это всегда инстанс таска (self), так же как в методах #python

```python
logger = get_task_logger(__name__)

@app.task(bind=True)
def add(self, x, y):
    logger.info(self.request.id)
```

Возможно наследование таска от базового класса

```python
import celery

class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@app.task(base=MyTask)
def add(x, y):
    raise KeyError()
```

У каждого таска должно быть уникальное имя. Если имя не задано - оно будет сгенерировано из имени модуля и имени функции

```python
>>> @app.task(name='sum-of-two-numbers')
>>> def add(x, y):
...     return x + y

>>> add.name
'sum-of-two-numbers'
```

Лучшая практика - использовать имя модуля как неймспейс для имени таска. В данном случае задано такое же имя, какое могло бы быть сгенерировано автоматически для таска, заданного в модуле tasks.py

```python
>>> @app.task(name='tasks.add')
>>> def add(x, y):
...     return x + y

>>> add.name
'tasks.add'
```

Вопрос автонейминга и релятивного импорта описан [тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#automatic-naming-and-relative-imports). Как менять схему автонейминга описано [тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#changing-the-automatic-naming-behavior).

Task Request содержит [информацию](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-request) и состояние текущего таска. Подробнее о полях смотри в доке.

```python
@app.task(bind=True)
def dump_context(self, x, y):
    print(
        'Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request)
        )
```

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

`app.Task.retry()` используется для извлечения таска, например для того, чтобы [поднять ошибку](https://docs.celeryproject.org/en/stable/userguide/tasks.html#retrying)

```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```

Подробнее читай [в доке](https://docs.celeryproject.org/en/stable/userguide/tasks.html#retrying).

Celery может [хранить состояние текущего таска](https://docs.celeryproject.org/en/stable/userguide/tasks.html#states) - это результат задачи или поднятая ошибка. Реализовано несколько бекендов для резалтов, [смотри чем они отличаются тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-result-backends).

Можно поднять несколько экцепшенов, которые [обеспечат определенное поведение воркера](https://docs.celeryproject.org/en/stable/userguide/tasks.html#semipredicates) для записи финального состояния. Это позволяет игнорить или отклонять таски.

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

[Пример использования тасков для фильтрации спама на джанго тут](https://docs.celeryproject.org/en/stable/userguide/tasks.html#task-example)

### [Calling tasks](https://docs.celeryproject.org/en/stable/userguide/calling.html)

`T.delay(arg, kwarg=value)`
Star arguments shortcut to .apply_async. (.delay(*args, **kwargs) calls .apply_async(args, kwargs)).

`T.apply_async((arg,), {'kwarg': value})`

`T.apply_async(countdown=10)`
executes in 10 seconds from now.

`T.apply_async(eta=now + timedelta(seconds=10))`
executes in 10 seconds from now, specified using eta

`T.apply_async(countdown=60, expires=120)`
executes in one minute from now, but expires after 2 minutes.

`T.apply_async(expires=now + timedelta(days=2))`
expires in 2 days, set using datetime.

Поддерживаются [слинкованные таски](https://docs.celeryproject.org/en/stable/userguide/calling.html#linking-callbacks-errbacks), [сборщик состояний](https://docs.celeryproject.org/en/stable/userguide/calling.html#on-message) таска, [утсановка](https://docs.celeryproject.org/en/stable/userguide/calling.html#eta-and-countdown) времени срабатывания и экспирейшен, а так-же жругие опции, включая сборщики ошибок, сжатие и т.д.

Другой способ выполнения тасков - [построение воркфлоу через signature](https://docs.celeryproject.org/en/stable/userguide/canvas.html)

### [Workers](https://docs.celeryproject.org/en/stable/userguide/workers.html#workers-guide)

Самый простой способ запустить воркера - `celery -A proj worker -l INFO`

Можно запускать множество воркеров

```shell
celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker2@%h
$ celery -A proj worker --loglevel=INFO --concurrency=10 -n worker3@%h
```

Воркера можно [завершить](https://docs.celeryproject.org/en/stable/userguide/workers.html#stopping-the-worker) или [рестартнуть](https://docs.celeryproject.org/en/stable/userguide/workers.html#restarting-the-worker). Все остальное смотри в [документации](https://docs.celeryproject.org/en/stable/userguide/workers.html#workers-guide)

### [Запуск демонов](https://docs.celeryproject.org/en/stable/userguide/daemonizing.html)

### [Периодически запускаемые таски](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)

### [Routing Tasks](https://docs.celeryproject.org/en/stable/userguide/routing.html)

### [Monitoring and Management Guide](https://docs.celeryproject.org/en/stable/userguide/monitoring.html)

### [Security](https://docs.celeryproject.org/en/stable/userguide/security.html)

### [Optimizing](https://docs.celeryproject.org/en/stable/userguide/optimizing.html)

### [Debugging](https://docs.celeryproject.org/en/stable/userguide/debugging.html)

### [Concurrency](https://docs.celeryproject.org/en/stable/userguide/concurrency/index.html)

### [Signals](https://docs.celeryproject.org/en/stable/userguide/signals.html)

### [Testing with Celery](https://docs.celeryproject.org/en/stable/userguide/testing.html)

### [Extensions and Bootsteps](https://docs.celeryproject.org/en/stable/userguide/extending.html)

### [Configuration and defaults](https://docs.celeryproject.org/en/stable/userguide/configuration.html)

Мониторить celery можно через [[flower]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[redis]: redis "Redis"
[rabbitmq]: rabbitmq "Rabbitmq"
[rabbitmq]: rabbitmq "Rabbitmq"
[redis]: redis "Redis"
[docker]: ../lists/docker "Docker"
[redis]: redis "Redis"
[python-logging]: ../lists/python-logging "Python-logging"
[flower]: flower "Flower"
[//end]: # "Autogenerated link references"