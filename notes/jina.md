---
description: Фреймворк для работы с ml-моделями
title: Jina
tags: ml
---

Jina — это платформа нейронного поиска, которая позволяет любому создавать SOTA и масштабируемые приложения нейронного поиска за считанные минуты.

Основная идея нейронного поиска заключается в использовании самых современных глубоких нейронных сетей для создания каждого компонента поисковой системы. Короче говоря, нейронный поиск — это глубокий поиск информации с помощью нейронной сети. Jina обеспечивает расширенный анализ всех видов неструктурированных данных, таких как изображения, аудио, видео, PDF, 3D.

Jina использует DocArray в качестве основной структуры данных; Jina Hub для совместного использования, контейнеризации и повторного использования компонентов поисковых конвейеров. Jina разработана как компактная и простая в использовании структура. Есть только две основные концепции, которые нужно изучить:

- Executor является самодостаточным компонентом и выполняет группу задач над документами.
- Flow объединяет исполнителей в конвейер обработки, обеспечивает масштабируемость и упрощает развертывание в облаке.

## Start project

`pip install -U jina`

`jina new hello-jina`

```python
hello-jina
|- app.py
|- executor1/
        |- config.yml
        |- executor.py
```

- `app.py` is the entrypoint of your Jina project. You can run it via python `app.py`
- `executor1/` is where we’ll write our Executor code
- `config.yml` is the config file for the Executor. It’s where you keep metadata for your Executor, as well as dependencies

[more demos](https://docs.jina.ai/get-started/hello-world/?utm_source=jina)

## DocArray

[DocArray](https://docarray.jina.ai/?utm_source=jina)

DocArray — это библиотека для вложенных, неструктурированных данных в пути, включая текст, изображения, аудио, видео и т. д. Он позволяет инженерам глубокого обучения эффективно обрабатывать, внедрять, искать, рекомендовать, хранить и передавать данные с помощью python API.

- сверхвыразительная структура данных для представления сложного/смешанного/вложенного текста, изображений, видео, аудио, данных 3D
- разработан так, чтобы быть таким же простым, как список Python
- оптимизирован для сетевой связи, готов к подключению в любое время благодаря быстрой и сжатой сериализации в Protobuf, байтах, base64, JSON, CSV, DataFrame
- работайте с данными, не занимающими память, с помощью хранилища документов на диске, сохраняя при этом тот же опыт работы с API. Поддержка классических баз данных и векторных баз данных для более быстрого поиска
- поддержка [[graphql]] делает ваш сервер универсальным по запросу и ответу; встроенная проверка данных и схема JSON (OpenAPI) помогают создавать надежные веб-сервисы
- интеграция с ИДЕ

### Document

![Document](../attachments/2022-05-14-01-11-11.png)

Объект Document имеет [предопределенную схему данных](https://docarray.jina.ai/fundamentals/document). Как [работать с документом](https://docarray.jina.ai/fundamentals/document/construct/?utm_source=docarray).

### DocumentArray

DocumentArray представляет собой контейнер объектов, похожий на список. Это лучший способ при работе с несколькими документами. Он реализует все списковые интерфейсы. Он также мощный, как Numpy ndarray и Pandas DataFrame, позволяя вам эффективно получать доступ к элементам и атрибутам содержащихся документов. Кроме того доступны расширенные функции DocumentArray. Эти функции значительно ускоряют работу специалистов по обработке и анализу данных при доступе к вложенным элементам, оценке, визуализации, параллельных вычислениях, сериализации, сопоставлении и т. д. Если ваши данные слишком велики и не помещаются в память, вы можете просто переключиться на хранилище документов на диске или в удаленном хранилище . Все API и пользовательский интерфейс остаются прежними.

[Как работать](https://docarray.jina.ai/fundamentals/documentarray/construct/?utm_source=docarray)

### Dataclass

Предоставляет АПИ для работы с мультимодальными данными. Продолжает идиому python датаклассов. [Подробнее](https://docarray.jina.ai/fundamentals/dataclass/?utm_source=docarray).

![dataclass](../attachments/2022-05-14-01-56-21.png)

[API](https://docarray.jina.ai/fundamentals/dataclass/construct)

### Примеры и интеграция

[Примеры](https://docarray.jina.ai/datatypes)

Интеграции:

- [[sqlite]] [и другие способы хранения]](https://docarray.jina.ai/advanced/document-store/)
- [jupyter notebook](https://docarray.jina.ai/fundamentals/notebook-support)
- [pytorch](https://docarray.jina.ai/advanced/torch-support)
- [[fastapi]]/[[pydantic]] [смотри тут](https://docarray.jina.ai/fundamentals/fastapi-support)
- [[graphql]] [смотри тут](https://docarray.jina.ai/advanced/graphql-support)

## Flow и Executor

![flow and executor](../attachments/2022-05-14-00-52-20.png)

**Gateway**: Шлюз — это служба, запускаемая потоком, который отвечает за предоставление клиенту конечных точек WebSocker или gRPC. Это сервис, с которым будут общаться клиенты приложения. Кроме того, он сохраняет информацию о топологии потока, чтобы гарантировать, что исполнители Documents обрабатывают их в правильном порядке. Он связывается с развертываниями через gRPC

**Deployment**: Развертывание — это абстракция вокруг Executor, которая позволяет Gateway взаимодействовать с Executors. Он инкапсулирует и абстрагирует детали внутренней репликации.

**Pod**: Pod — это простая абстракция над средой выполнения, которая запускает любой сервис Jina, будь то процесс, контейнер Docker или Kubernetes Pod.

**Head**: The Head — это служба, добавленная Jina в сегментированное развертывание. Она управляет связью с различными сегментами на основе настроенной стратегии опроса. Она общается с Executors через gRPC.

### Executors

- позволяют организовать ваши функции на основе `DocumentArray` в логические объекты, которые могут совместно использовать состояние конфигурации в соответствии с ООП
- преобразуют ваши локальные функции в функции, которые можно распределять внутри потока
- внутри потока могут одновременно обрабатывать несколько массивов `DocumentArray` и легко развертываться в облаке как часть вашего приложения нейронного поиска
- могут быть легко контейнеризированы и разделены с вашими коллегами с помощью `jina hub push/pull`

[API of executors](https://docs.jina.ai/fundamentals/executor/executor-api/?utm_source=jina)

## Аналоги

- [MLFlow](https://github.com/mlflow/mlflow/) Machine Learning Lifecycle Platform
- [KubeFlow](https://github.com/kubeflow/kubeflow) the cloud-native platform for machine learning operations - pipelines, training and deployment
- [RayWorkflow](https://github.com/ray-project/ray) provides a simple, universal API for building distributed applications, [дока](https://docs.ray.io/en/latest/workflows/concepts.html)
- [seldon-core](https://github.com/SeldonIO/seldon-core) converts your ML models (Tensorflow, Pytorch, H2o, etc.) or language wrappers (Python, Java, etc.) into production REST/GRPC microservices.

Еще ссылки:

- [[machine-learning]]
- [Документация jina](https://docs.jina.ai/)
- [Документация DocArray](https://docarray.jina.ai/?utm_source=jina)

[//begin]: # "Autogenerated link references for markdown compatibility"
[graphql]: graphql "GraphQL"
[machine-learning]: ../lists/machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[graphql]: graphql "GraphQL"
[sqlite]: sqlite "Sqlite"
[fastapi]: fastapi "Fastapi"
[pydantic]: pydantic "Pydantic"
[graphql]: graphql "GraphQL"
[machine-learning]: ../lists/machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"