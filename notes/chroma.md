---
description: Chroma — open-source embedding database / vector store для быстрых semantic search и retrieval.
tags: ml machine-learning rust python server bd
title: Chroma
---
Chroma — open-source data infrastructure for AI: embedding database / vector store с простым Python/JS API, возможностью работать in-memory или как клиент-сервер. Подходит для быстрых прототипов и production use-cases, есть Chroma Cloud — управляемый сервис.

Источник: [Chroma на GitHub](https://github.com/chroma-core/chroma)

## Быстрый пример (Python)

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("all-my-documents")
collection.add(
    documents=["This is document1", "This is document2"],
    metadatas=[{"source": "notion"}, {"source": "google-docs"}],
    ids=["doc1", "doc2"],
)
results = collection.query(query_texts=["query example"], n_results=2)
```

## Особенности

- Простота API: быстрый старт для прототипов.
- Поддержка in-memory и persistence режимов (client-server).
- Chroma Cloud — managed сервис.
- Интеграции с embedding providers и экосистемой ML-инструментов.

## Ресурсы

- Документация: [Chroma docs](https://docs.trychroma.com/)
- Репозиторий: [chroma на GitHub](https://github.com/chroma-core/chroma)
- [[lists/bd]]
- [[notes/qdrant]]
- [[notes/weaviate]]
- [[notes/milvus]]

## Лицензия

Apache-2.0

## AI-warning

✨ Данная статья сгенерирована с помощью ChatGPT 5.0 mini. Текст проверен человеком.

[lists/bd]: ../lists/bd "Data Bases"
[notes/qdrant]: qdrant "Qdrant"
[notes/weaviate]: weaviate "Weaviate"
[notes/milvus]: milvus "Milvus"
