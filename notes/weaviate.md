---
description: Weaviate — cloud-native vector database для semantic search, RAG и recommendation.
tags: ml machine-learning go python docker server bd
title: Weaviate
---
Weaviate — cloud-native vector database, которая хранит объекты и их векторы, объединяя векторный поиск с фильтрацией по метаданным. Подходит для RAG, semantic и image search, recommendation и задач nearest-neighbor. Основная реализация на Go; доступна как self-hosted, Edge-версия и управляемый сервис Weaviate Cloud.

Источник: [weaviate на GitHub](https://github.com/weaviate/weaviate)

## Установка и быстрый старт

- Docker (быстрый старт):

```bash
# пример из README
docker compose up -d
# либо запустить образ напрямую
docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:latest
```

- Другие опции: Kubernetes, Weaviate Cloud. Список в установке: [Weaviate installation docs](https://docs.weaviate.io/deploy).

Важно: при локальном запуске обычно подключают модуль vectorizer (встраиваемая модель) или используют `self_provided` векторы.

## Клиенты и API

Weaviate предоставляет клиентские библиотеки и API:

- Официальные клиенты: Python, JavaScript/TypeScript, Java, Go, C#/.NET.
- API: REST, gRPC и GraphQL (см. документацию).

Подключение и пример на Python:

```python
import weaviate
from weaviate.classes.config import Configure, DataType, Property

# подключение к локальному Weaviate
client = weaviate.connect_to_local()

# создать коллекцию с автоматическим векторизатором
client.collections.create(
    name="Article",
    properties=[Property(name="content", data_type=DataType.TEXT)],
    vector_config=Configure.Vectors.text2vec_model2vec(),
)

# вставка объектов (генерация векторов при импорте)
articles = client.collections.get("Article")
articles.data.insert_many([
    {"content": "Vector databases enable semantic search"},
    {"content": "Machine learning models generate embeddings"},
])

# семантический поиск
results = articles.query.near_text(query="Search objects by meaning", limit=3)
print(results)
client.close()
```

## Ключевые возможности

- Быстрый семантический поиск по миллиардам векторов (ANN). См. [benchmarks](https://docs.weaviate.io/weaviate/benchmarks/ann).
- Интегрированные векторизаторы (OpenAI, Cohere, HuggingFace и др.) и опция импортировать предсгенерированные векторы.
- Гибридный поиск: комбинирует семантику и BM25/keyword-поиск, image search и фильтры.
- Поддержка масштабирования: шардирование, репликация, multi-tenancy, RBAC.
- Встроенные RAG и reranking, TTL для объектов, векторная компрессия и квантование для экономии памяти.
- Web UI и набор demo/recipes для быстрого старта и интеграций.

## Когда использовать

- Системы RAG, чат-боты, semantic search и recommendation.
- Проекты, где важно комбинировать векторный поиск и точечную фильтрацию по payload.

## Ресурсы

- Документация: [Weaviate docs](https://docs.weaviate.io/)
- Quickstart: [Weaviate quickstart](https://docs.weaviate.io/weaviate/quickstart)
- Клиентские библиотеки: [Weaviate client libraries](https://docs.weaviate.io/weaviate/client-libraries/python)
- Репозиторий: [weaviate на GitHub](https://github.com/weaviate/weaviate)
- Weaviate Cloud: [console.weaviate.cloud](https://console.weaviate.cloud/)
- [[lists/bd]]
- [[notes/qdrant]]
- [[notes/milvus]]
- [[notes/chroma]]

## Лицензия

Большая часть кода доступна под BSD 3-Clause; в репозитории есть и коммерческие Enterprise-файлы (см. README и лицензионную секцию).

[lists/bd]: ../lists/bd "Data Bases"
[notes/qdrant]: qdrant "Qdrant"
[notes/milvus]: milvus "Milvus"
[notes/chroma]: chroma "Chroma"
