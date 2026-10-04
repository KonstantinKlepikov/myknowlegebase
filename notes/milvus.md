---
description: Milvus — высокопроизводительная cloud-native vector database для масштабируемого ANN и hybrid search.
tags: ml machine-learning go python server bd
title: Milvus
---
Milvus — высокопроизводительная cloud-native vector database, спроектированная для масштабируемого ANN (approximate nearest neighbor) поиска и hybrid search. Подходит для RAG, semantic/image search, recommendation и других задач, где нужны векторные представления и фильтрация по метаданным.

Источник: [Milvus на GitHub](https://github.com/milvus-io/milvus)

## Пример (Python)

```python
from pymilvus import MilvusClient

client = MilvusClient("milvus_demo.db")  # или endpoint:uri и credentials для удалённого кластера

client.create_collection(
    collection_name="demo_collection",
    dimension=768,
)

# вставка (data — список векторов/полей)
res = client.insert(collection_name="demo_collection", data=data)

# поиск
query_vectors = embedding_fn.encode_queries(["Who is Alan Turing?"])
res = client.search(collection_name="demo_collection", data=query_vectors, limit=2)
```

## Ключевые возможности

- Fully-distributed, K8s-native архитектура: разделение compute и storage, шардирование и репликация.
- Поддержка множества index типов: HNSW, IVF, FLAT, SCANN, DiskANN, IVFPQ и вариации с quantization.
- GPU/CPU hardware acceleration для индексирования и поиска.
- Hybrid search: dense + sparse (BM25) и multi-vector сценарии.
- Поддержка sparse vectors для full-text и совместное хранение dense+ sparse.
- Hot/cold storage, multi-tenancy, RBAC, TTL для объектов.
- Экосистема: интеграции с LangChain, LlamaIndex, OpenAI, HuggingFace; инструменты мониторинга (Prometheus/Grafana), миграции и CDC.

## Когда использовать

- RAG, semantic search, image search, recommendation, большие наборы векторов (миллиарды векторов) и сценарии с требованием low-latency.

## Ресурсы

- Официальный сайт и docs: [milvus.io](https://milvus.io/)
- Документация: [Milvus Docs](https://milvus.io/docs)
- Репозиторий: [milvus на GitHub](https://github.com/milvus-io/milvus)
- Quickstart и tutorials: [Milvus tutorials](https://milvus.io/docs/tutorials-overview.md)
- [[lists/bd]]
- [[notes/qdrant]]
- [[notes/weaviate]]
- [[notes/chroma]]

## Лицензия

Проект распространяется под Apache-2.0 (репозиторий на GitHub содержит ссылки на лицензию и коммерческие разделы).

[lists/bd]: ../lists/bd "Data Bases"
[notes/qdrant]: qdrant "Qdrant"
[notes/weaviate]: weaviate "Weaviate"
[notes/chroma]: chroma "Chroma"
