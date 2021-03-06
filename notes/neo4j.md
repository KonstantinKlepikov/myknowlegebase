---
description: Графовая база данных neo4j
title: Neo4j graph data base
tags: bd graphs
---
Графовая база neo4j реализует эффективные алгоритмы запросов к графу. Особенности:

- реализует модель направленного графа со свойствами - узлы и связи содержат свзяи, связи реализуют направление.
- в neo4j свойства хранятся ввиде пар ключ-значение отдельно от графа, где ключ это строка, а значение - java строка в определенном для этого динамическое хранилище
- сам граф хранится в виде смежности без индексом (index-free adjacencee) - каждый узел содержит ссылки на смежные с ним узлы. Время исполнения запроса зависит не от общего размера графа, а от размера подграфа, задействованногно в поиске, что наиболее эффективно для запросов, исследующих окрестность начального узла
- бд поддерживает встраивание значений свойств непосредственно в файл хранения свойств, что для определенных задач (к примеру для коротких значений типа индексов почты) снижает число операций ввод/вывод. кроме того, оптимизируется и хранение имен свойств.
- узлы могут размечаться метками, что позволяет их группировать
- связи имеют только один исходящий узел и один входящий (модель не предусматривает мультисвязей)
- поддержка транзакций. Блокируются операции записи узлов, участвующих в транзакции. Используется журнал предварительной регшистрации записи для гарантий завершения транзакции.
- реализует репликацию на базе схемы ведущий сервер - подчиненные
- производится разделение трафика чтения и записи - в основной реализации запись ведется только на ведущий сервер, а чтение только с ведомых
- доступен распределенный кэш для ускорения процедуры запросов
- реализован очень быстрый первоначальный импорт данных (инициализация) и пакетный импорт из csv
- язык запросов - [[cypher]]
- есть [gui endpoint](https://neo4j.com/developer/neo4j-browser/) для визуализации запросов
- продукт разделен на комьюнити и энтерпрайз версию. Первый вариант ограничен по мощности
- собственная [библиотека графовых алгоритмов](https://neo4j.com/developer/graph-data-science/graph-algorithms/)

neo4j реализует два типа поддержки - встроенную и серверную.

Встроенный режим - бд запускается в одном процессе с приложением. Преимущество:

- быстрый отклик
- большой выбор интерфейсов
- управление транзакциями

Недостатки:

- только виртуальная машина java
- звыисимость от сборки мусора, как следствие - длинные паузы между сборками, приводящие к увеличению времени выполнения запросов
- жизненный цикл БД целиком и полностью связан с приложением

В серверном режиме экземпляры бд запускаются на собственных серверах и доступны через интерфейсы. Преимущества:

- доступ по Rest api
- не зависит от использующего приложения
- легко масштабируется
- не зависит от сборщиков мусора

Недостатки:

- накладные расходы сети
- проблемы с транзакциями, собирающими большое число запросов
- сложности с шардитрованием очень больших графов (большие расходы на переходы из одного сегмента графа в другой по сети)

Смотир еще:

- [документация](https://neo4j.com/developer/graph-platform/)
- [[graphs]]
- [[cypher]]
- [[python-api-neo4j]]
- [container](https://hub.docker.com/_/neo4j/?tab=description)
- [docker how-to](https://neo4j.com/developer/docker-run-neo4j/)
- [docker-compose how to](https://neo4j.com/labs/kafka/4.0/docker/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[cypher]: cypher "Cypher query language"
[graphs]: ../lists/graphs "Machine learning with graphs"
[cypher]: cypher "Cypher query language"
[python-api-neo4j]: python-api-neo4j "Python api for neo4j"
[//end]: # "Autogenerated link references"