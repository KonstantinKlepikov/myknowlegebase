---
description: Высокопроизводительная vector search engine и vector database для semantic/nearest-neighbor search.
tags: ml machine-learning rust python server bd
title: Qdrant
---
Qdrant — высокопроизводительная vector search engine и vector database, оптимизированная для приложений с embedding/semantic search, recommendation и nearest-neighbor задач. Написан на Rust, доступен как self-hosted server, легковесная версия Edge и как управляемый сервис [Qdrant Cloud](https://cloud.qdrant.io/).

Источник: [qdrant на GitHub](https://github.com/qdrant/qdrant)

## Установка и быстрый старт

- Запуск локального сервера в Docker (быстрый старт):

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Обратите внимание: этот запуск не защищён (open to all interfaces). Перед продакшеном изучите раздел `security` в документации.

## Клиенты

Официальные клиенты: Go, [[tag/rust]], JavaScript/TypeScript, [[tag/python]], .NET/C#, Java. Есть также community-клиенты (Kotlin, PHP и др.).

Пример использования с Python client:

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# создать коллекцию и добавить точку (vector + payload)
client.recreate_collection("my_collection", vector_size=1536, distance="Cosine")
client.upsert(
    collection_name="my_collection",
    points=[{
        "id": 1,
        "vector": [0.1, 0.2, ...],
        "payload": {"title": "Example"}
    }]
)

# поиск похожих
res = client.search("my_collection", query_vector=[...], limit=5)
```

## Основные возможности

- Dense, Sparse и Multi-vector search (поддержка нескольких эмбеддингов на объекте).
- Фильтрация по payload: rich JSON-поиск (keyword, full-text, numeric ranges, geo и т.д.) с `must/should/must_not`.
- Hybrid search: комбинация семантики и точечного/ключевого поиска с различными стратегиями fusion.
- Vector quantization и on-disk storage: значительная экономия RAM с компромиссом точности.
- Горизонтальное масштабирование: sharding, replication, zero-downtime updates.
- Рекомендации, фасетирование, MMR, relevance feedback, multitenancy.
- SIMD-ускорение, GPU-поддержка для индексирования, async I/O (io_uring) и WAL для устойчивости.
- Web UI для инспекции коллекций и мониторинга.

## Архитектура и интерфейсы

- [REST API](https://api.qdrant.tech/) с OpenAPI спецификацией.
- gRPC интерфейс для высокопроизводительных сценариев.
- Qdrant Edge — встроенная, локальная версия для edge/embedded-приложений (встраивается в процесс приложения).

## Когда использовать

- Семантический поиск и поиск по эмбеддингам (NLP, recommendation, image search).
- Приложения, где важна фильтрация по метаданным вместе с векторным поиском.
- Сценарии с ограниченной памятью — благодаря квантованию и on-disk хранению.

## Ресурсы

- Документация: [qdrant.tech — Documentation](https://qdrant.tech/documentation/)
- Quick Start: [Quick Start guide](https://qdrant.tech/documentation/quickstart/)
- OpenAPI: [api.qdrant.tech](https://api.qdrant.tech/)
- Qdrant Cloud: [cloud.qdrant.io](https://cloud.qdrant.io/)
- Репозиторий: [qdrant на GitHub](https://github.com/qdrant/qdrant)
- [[lists/bd]]
- [[notes/weaviate]]
- [[notes/milvus]]
- [[notes/chroma]]

## Лицензия

Apache License 2.0.

## AI-warning

✨ Данная статья сгенерирована с помощью ChatGPT 5.0 mini. Текст проверен человеком.

[tag/rust]: ../tag/rust "Tag: rust"
[tag/python]: ../tag/python "Tag: python"
[lists/bd]: ../lists/bd "Data Bases"
[notes/weaviate]: weaviate "Weaviate"
[notes/milvus]: milvus "Milvus"
[notes/chroma]: chroma "Chroma"
