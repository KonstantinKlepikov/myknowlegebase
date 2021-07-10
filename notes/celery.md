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
