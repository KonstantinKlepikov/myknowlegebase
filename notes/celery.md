# celery

[Celery](https://docs.celeryproject.org/en/stable/) is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system.

Очереди используются как механизм для распределения работы по потокам или машинам. Вход в очередь задач - это единица работы, называемая задачей. Выделенные рабочие процессы постоянно отслеживают очереди задач на предмет выполнения новой работы. Celery общается через сообщения, обычно используя брокера для посредничества между клиентами и воркерами. Чтобы инициировать задачу, клиент добавляет сообщение в очередь, а затем брокер доставляет это сообщение воркеру. Система Celery может состоять из нескольких воркеров и брокеров, уступая место высокой доступности и горизонтальному масштабированию. Celery написан на #python, но протокол может быть реализован на любом языке. В дополнение к Python есть node-celery и node-celery-ts для Node.js и клиент PHP. Взаимодействие языков также может быть достигнуто путем раскрытия конечной точки HTTP и наличия задачи, которая ее запрашивает (веб-перехватчики).

```Python
from celery import Celery

app = Celery('hello', broker='amqp://guest@localhost//')

@app.task
def hello():
    return 'hello world'
```

[introduction](https://docs.celeryproject.org/en/stable/getting-started/introduction.html#celery-is)

## [user guide](https://docs.celeryproject.org/en/stable/userguide/index.html)

### [Application](https://docs.celeryproject.org/en/stable/userguide/application.html)

```Python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```

Значение имеет main имя модуля, т.к. селери общается с помощью меседжей. Извлекается имя таска для того чтобы каждый воркер знал к какой функции ему образщаться.

```Python
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

```Python
from celery import Celery
app = Celery()

@app.task
def add(x, y): return x + y

if __name__ == '__main__':
    app.worker_main()
```

Но при импорте это будет выглядеть иначе:

```Python
>>> from tasks import add
>>> add.name
tasks.add
```

Кроме того, имя main модуля можно задать нгепосредственно

```Python
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

```Python
>>> app.conf.timezone
'Europe/London'
```

можно задать значения напрямую

```Python
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
