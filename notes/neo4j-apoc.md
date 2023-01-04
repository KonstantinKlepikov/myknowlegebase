---
description: Neo4j APOC Library
title: Neo4j APOC библиотека
tags: data-bases graphs machine-learning
---
[APOC Library](https://neo4j.com/developer/neo4j-apoc/)

APOC расшифровывается как « Удивительные процедуры на шифровании » . Перед выпуском APOC разработчикам приходилось писать свои собственные процедуры и функции для общих функций, которые Cypher или база данных Neo4j еще не реализовали. Каждый разработчик мог бы написать свою версию этих функций, что привело бы к большому количеству дублирования. APOC - это стандартная служебная библиотека для общих процедур и функций. APOC включает более 450 стандартных процедур, предоставляющих функциональные возможности для утилит, преобразований, обновления графов и многого другого. Они хорошо поддерживаются и их очень легко запускать как отдельные функции или включать в запросы Cypher.

Начиная с Neo4j 4.1.1, доступны две версии библиотеки APOC:

- процедуры и функции APOC Core, которые не имеют внешних зависимостей и не требуют настройки. Это также доступно в Neo4j AuraDB
- APOC Full содержит все, что есть в ядре APOC, а также дополнительные процедуры и функции, которые доступны как в Neo4j Sandbox, Docker-образе и Neo4j Desktop, так и при селф-хостед размещении.

[Instalation](https://neo4j.com/labs/apoc/4.3/installation/)

Пример использования:

```sql
WITH 'https://raw.githubusercontent.com/neo4j-contrib/neo4j-apoc-procedures/4.3/core/src/test/resources/person.json' AS url

CALL apoc.load.json(url) YIELD value as person

MERGE (p:Person {name:person.name})
   ON CREATE SET p.age = person.age, p.children = size(person.children)
```

Процедура `call apoc.help('keyword')` позволяет получить справку по доступным в APOC функциям и процедурам. [Подробнее](https://neo4j.com/labs/apoc/4.3/help/).

## [Список функций](https://neo4j.com/labs/apoc/4.3/overview/)

- [конфигурация бд](https://neo4j.com/labs/apoc/4.3/config/)
- [import](https://neo4j.com/labs/apoc/4.3/import/)
- [export](https://neo4j.com/labs/apoc/4.3/export/)
- [Database Integration](https://neo4j.com/labs/apoc/4.3/database-integration/) (интеграция с другими BD ElasticSearch,MongoDB, Couchbase, Redis)
- [graph updates](https://neo4j.com/labs/apoc/4.3/graph-updates/)
- [structures](https://neo4j.com/labs/apoc/4.3/data-structures/) (collections of aggregate functions, maps and conversion to types)
- [date time functions](https://neo4j.com/labs/apoc/4.3/temporal/)
- [мат-функции](https://neo4j.com/labs/apoc/4.3/mathematical/)
- [дополнительные методы запросов к бд](https://neo4j.com/labs/apoc/4.3/graph-querying/) (ближайшие ноды, пути, связанности и т.п.)
- [сравнение графов](https://neo4j.com/labs/apoc/4.3/comparing-graphs/)
- [выполнение cypher запросов](https://neo4j.com/labs/apoc/4.3/cypher-execution/)
- [Virtual Nodes & Relationships](https://neo4j.com/labs/apoc/4.3/virtual/) (Graph Projections) - необходимо для работы в [[neo4j-ml]]. Виртуальные узлы и связи не существуют в графе, они возвращаются только по запросу и могут использоваться для представления проекции графа. Способы применения:
  - return only a few properties of nodes/rels to the visualization, e.g. if you have huge text properties
  - visualize clusters found by graph algorithms
  - aggregate information to a higher level of abstraction
  - skip intermediate nodes in a longer path
  - hide away properties or intermediate nodes/relationships for security reasons
  - graph grouping
  - visualization of data from other sources (computation, RDBMS, document-dbs, CSV, XML, JSON) as graph without even storing it
- [NLP](https://neo4j.com/labs/apoc/4.3/nlp/) (google, amazon and azure integration)
- [фоновое выполнение](https://neo4j.com/labs/apoc/4.3/background-operations/)
- [мониторинг БД](https://neo4j.com/labs/apoc/4.3/database-introspection/)
- [логирование и ворнинги](https://neo4j.com/labs/apoc/4.3/operational/)
- [несколько не вошедших в другие разделы функций](https://neo4j.com/labs/apoc/4.3/misc/) (к примеру для работы с текстом)
- [индексы](https://neo4j.com/labs/apoc/4.3/indexes/)

Тут [список процедур](https://neo4j.com/labs/apoc/4.3/transaction/), выполняемых со своей собственной транзакцией

Смотри еще:

- [документация](https://neo4j.com/labs/apoc/4.3/)
- [[neo4j-ml]]
- [[neosematics]]
- [[cypher]]
