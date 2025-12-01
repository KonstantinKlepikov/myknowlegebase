---
description: Программный брокер сообщений на основе стандарта AMQP
title: Rabbitmq
tags: queue
---
Программный брокер сообщений на основе стандарта AMQP — тиражируемое связующее программное обеспечение, ориентированное на обработку сообщений. Создан на основе системы Open Telecom Platform, написан на языке Erlang, в качестве движка базы данных для хранения сообщений использует Mnesia.

Может работать в связке с [[celery]]. Вот инстуркция [как ставить](https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/rabbitmq.html#broker-rabbitmq).

Статьи:

- [Статья в вики](https://ru.wikipedia.org/wiki/RabbitMQ)
- [Messaging для чайников. Утилизируем все возможности RabbitMQ на Python](https://habr.com/ru/articles/743192/)

Смотри еще:

- [[bd]]
- [[apache-kafka]]
- [[celery]]
- [[redis]]


[celery]: celery "Celery"
[bd]: ../lists/bd "Data Bases"
[apache-kafka]: apache-kafka "Apache kafka"
[redis]: redis "Redis"
