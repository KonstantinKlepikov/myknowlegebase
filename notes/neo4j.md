---
description: Графовая база данных neo4j
title: Neo4j graph data base
tags: data-bases graphs
---
Графовая база neo4j реализует эффективные алгоритмы запросов к графу. Особенности:

- реализует модель направленного графа со свойствами - узлы и связи содержат связи, связи реализуют направление.
- в neo4j свойства хранятся в виде пар ключ-значение отдельно от графа, где ключ это строка, а значение - java строка в определенном для этого динамическое хранилище
- сам граф хранится в виде смежности без индексов (index-free adjacencee) - каждый узел содержит ссылки на смежные с ним узлы. Время исполнения запроса зависит не от общего размера графа, а от размера подграфа, задействованногно в поиске, что наиболее эффективно для запросов, исследующих окрестность начального узла. Для сложных запросов реализуется модель in-memory графа, когда необходимый для выполнения запроса подграф предварительно катологизируется в память машины.
- бд поддерживает встраивание значений свойств непосредственно в файл хранения свойств, что для определенных задач (к примеру для коротких значений типа индексов почты) снижает число операций ввод/вывод. кроме того, оптимизируется и хранение имен свойств.
- узлы могут размечаться метками, что позволяет их группировать
- связи имеют только один исходящий узел и один входящий (модель не предусматривает мультисвязей)
- поддержка транзакций. Блокируются операции записи узлов, участвующих в транзакции. Используется журнал предварительной регистрации записи для гарантий завершения транзакции.
- реализует репликацию на базе схемы ведущий сервер - подчиненные
- производится разделение трафика чтения и записи - в основной реализации запись ведется только на ведущий сервер, а чтение только с ведомых
- доступен распределенный кэш для ускорения процедуры запросов
- реализован очень быстрый первоначальный импорт данных (инициализация) и пакетный импорт из csv
- язык запросов - [[cypher]]
- есть [gui endpoint](https://neo4j.com/developer/neo4j-browser/) для визуализации запросов
- продукт разделен на комьюнити и энтерпрайз версию. Первый вариант ограничен по производительности
- собственная [библиотека графовых алгоритмов](https://neo4j.com/developer/graph-data-science/graph-algorithms/)

neo4j реализует два типа поддержки - встроенную и серверную.

**Встроенный режим** - бд запускается в одном процессе с приложением. Преимущество:

- быстрый отклик
- большой выбор интерфейсов
- управление транзакциями

Недостатки:

- только виртуальная машина java
- звыисимость от сборки мусора, как следствие - длинные паузы между сборками, приводящие к увеличению времени выполнения запросов
- жизненный цикл БД целиком и полностью связан с приложением

В **серверном режиме** экземпляры бд запускаются на собственных серверах и доступны через интерфейсы. Преимущества:

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
- [[cypher]]
- [[python-api-neo4j]]
- [[pytoneo]]
- [[neo4j-apoc]]
- [[neo4j-ml]]
- [[neosematics]] (n10s) is a plugin that enables the use of RDF and its associated vocabularies like (OWL,RDFS,SKOS and others) in Neo4
- [Natural Language Processing (NLP)](https://neo4j.com/labs/apoc/4.1/nlp/)
- [graph-data-science-client](https://github.com/neo4j/graph-data-science-client) A Python client for the Neo4j Graph Data Science (GDS) library (sorce is hosted on Amazon)
- [docker container](https://hub.docker.com/_/neo4j/?tab=description)
- [neo4jupyter](https://github.com/merqurio/neo4jupyter) A quick visualization tool for Jupyter and Neo4J (not great)
- [SciGraph](https://github.com/SciGraph/SciGraph) Represent ontologies and ontology-encoded knowledge in a neo4j graph.
- [[trinity]] A VSCode extension for [[cypher]] and Neo4j (very weak)
- [Neo4j web brouser](https://neo4j.com/docs/browser-manual/current/deployment-modes/dedicated-web-server/) dedicated installation
- [yworks.com](https://www.yworks.com/) Niils and solutions for graph and diagram visualizing. [demos](https://live.yworks.com/demos/)
  - [Data Explorer for Neo4j](https://www.yworks.com/products/data-explorer-for-neo4j)ю The free tool to visualize and explore graph database
  - [yFiles Graphs for Jupyter](https://www.yworks.com/products/yfiles-graphs-for-jupyter). [How use](https://youtu.be/M_PbbMVg4ME). [Repo](https://github.com/yWorks/yfiles-jupyter-graphs)
- [pyingest](https://github.com/neo4j-field/pyingest). A script for loading CSV and JSON files into a Neo4j . It performs well due to several factors: Records are grouped into configurable-sized chunks before ingest. For CSV files, we leverage the optimized CSV parsing capabilities of the Pandas library. For JSON files, we use a streaming JSON parser (ijson) to avoid reading the entire document into memorydatabase written in Python3
- [[apache-spark]] Unified engine for large-scale data analytics
- [[dgraph]]
- [[mongodb]]

Полезные ресурсы:

- [How to reset / clear / delete neo4j database?](https://stackoverflow.com/questions/23310114/how-to-reset-clear-delete-neo4j-database)
- [Bite-Sized Neo4j for Data Scientists](https://github.com/cj2001/bite_sized_data_science) repo and [videos](https://neo4j.com/video/bite-sized-neo4j-for-data-scientists/)
- [docker how-to](https://neo4j.com/developer/docker-run-neo4j/)
- [docker-compose how to](https://neo4j.com/labs/kafka/4.0/docker/)
- [User Defined Procedures and Functions](https://neo4j.com/developer/cypher/procedures-functions/)
- [Operators](https://neo4j.com/docs/cypher-manual/current/syntax/operators/)
- [Temporal values](https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/)
- [Temporal functions - instant types](https://neo4j.com/docs/cypher-manual/current/functions/temporal/)
- [Lists](https://neo4j.com/docs/cypher-manual/current/values-and-types/lists/)
- [Property, structural, and constructed values](https://neo4j.com/docs/cypher-manual/current/values-and-types/property-structural-constructed/)
- [Maps](https://neo4j.com/docs/cypher-manual/current/values-and-types/maps/)
- [Dates, datetimes, and durations](https://neo4j.com/docs/getting-started/cypher-intro/dates-datetimes-durations/)
- [Test if relationship exists in neo4j / spring data](https://stackoverflow.com/questions/42022215/test-if-relationship-exists-in-neo4j-spring-data)
- [EXISTS subqueries](https://neo4j.com/docs/cypher-manual/current/subqueries/existential/)
- [Parameters](https://neo4j.com/docs/cypher-manual/current/syntax/parameters/)
- [Data types and mapping to Cypher types](https://neo4j.com/docs/python-manual/current/data-types/)
- [Scalar functions](https://neo4j.com/docs/cypher-manual/current/functions/scalar/#functions-elementid)
- [Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/)
- [Create, show, and drop constraints](https://neo4j.com/docs/cypher-manual/current/constraints/managing-constraints/#constraints-examples-relationship-property-existence)
- [Check whether a node exists, if not create](https://stackoverflow.com/questions/24015854/check-whether-a-node-exists-if-not-create)

[//begin]: # "Autogenerated link references for markdown compatibility"
[cypher]: cypher "Cypher query language"
[python-api-neo4j]: python-api-neo4j "Python api for neo4j"
[pytoneo]: pytoneo "pytoneo client library and toolkit for working with neo4j"
[neo4j-apoc]: neo4j-apoc "Neo4j APOC библиотека"
[neo4j-ml]: neo4j-ml "Machine learning in Neo4j"
[neosematics]: neosematics "Neosematics"
[trinity]: trinity "Trinity"
[apache-spark]: apache-spark "Unified engine for large-scale data analytics"
[dgraph]: dgraph "Dgraph"
[mongodb]: mongodb "MongoDB"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[cypher]: cypher "Cypher query language"
[cypher]: cypher "Cypher query language"
[python-api-neo4j]: python-api-neo4j "Python api for neo4j"
[pytoneo]: pytoneo "pytoneo client library and toolkit for working with neo4j"
[neo4j-apoc]: neo4j-apoc "Neo4j APOC библиотека"
[neo4j-ml]: neo4j-ml "Machine learning in Neo4j"
[neosematics]: neosematics "Neosematics"
[trinity]: trinity "Trinity"
[cypher]: cypher "Cypher query language"
[apache-spark]: apache-spark "Unified engine for large-scale data analytics"
[dgraph]: dgraph "Dgraph"
[mongodb]: mongodb "MongoDB"
[//end]: # "Autogenerated link references"