---
description: python приложение для neo4j
title: pytoneo client library and toolkit for working with neo4j
tags: bd graphs python
---
Py2neo is a client library and toolkit for working with Neo4j from within Python applications and from the command line

`pip install --upgrade py2neo`

```python
>>> from py2neo import Graph
>>> graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
>>> graph.run("UNWIND range(1, 3) AS n RETURN n, n * n as n_sq")
   n | n_sq
-----|------
   1 |    1
   2 |    4
   3 |    9
```

## [Connection profiles](https://py2neo.org/2021.1/profiles.html)

## [Workflow](https://py2neo.org/2021.1/workflow.html)

`class py2neo.GraphService(profile=None, **settings)[source]` является средством доступа верхнего уровня для всей системы управления графовой базой данных [[neo4j]]. В иерархии объектов py2neo GraphService содержит один или несколько объектов Graph, в которых в основном происходит хранение и извлечение данных.

```python
>>> from py2neo import GraphService
>>> gs = GraphService("bolt://camelot.example.com:7687")

# Alternatively, the default value of bolt://localhost:7687 is used:
>>> default_gs = GraphService()
>>> default_gs
<GraphService uri='bolt://localhost:7687'>
```

`class py2neo.Graph(profile=None, name=None, **settings)` предоставляет дескриптор отдельной базы данных именованных графов, предоставляемой службой базы данных графов [[neo4j]]. Сведения о подключении предоставляются с использованием либо URI, либо ConnectionProfile, а также индивидуальных настроек, если это необходимо. Аргумент имени позволяет выбрать базу данных графа по имени. При работе с Neo4j 4.0 и выше это может быть любое имя, указанное в системном каталоге, полный список которого можно получить с помощью команды [[cypher]] `SHOW DATABASES`. Если здесь указать `None`, будет выбрана база данных по умолчанию, определенная на сервере. Для более ранних версий Neo4j имя должно быть установлено на `None`.

```python
>>> from py2neo import Graph
>>> sales = Graph("bolt+s://g.example.com:7687", name="sales")
>>> sales.run("MATCH (c:Customer) RETURN c.name")
 c.name
---------------
 John Smith
 Amy Pond
 Rory Williams
```

Доступ к системному графу, доступному во всех выпусках продукта 4.x+, также можно получить через класс SystemGraph.

```python
>>> from py2neo import SystemGraph
>>> sg = SystemGraph("bolt+s://g.example.com:7687")
>>> sg.call("dbms.security.listUsers")
 username | roles | flags
----------|-------|-------
 neo4j    |  null | []
```

Экземпляр Graph обеспечивает прямой или косвенный доступ к большей части функций, доступных в py2neo.

- `auto` новый автокоммит транзакции
- `begin` открыть новую транзакцию
- `call` Средство доступа для перечисления и вызова процедур. Это свойство содержит объект `procedureLibrary`, привязанный к этому графу, который предоставляет ссылки на процедуры Cypher в базовой реализации. Для вызова процедуры требуется только обычный синтаксис вызова функции Python

  ```python
    >>> g = Graph()
    >>> g.call.dbms.components()
    name         | versions   | edition
    --------------|------------|-----------
    Neo4j Kernel | ['3.5.12'] | community
  ```

- `commit` коммит транзакции
- `create(subgraph)`
- `delete(subgraph)`
- `delete_all` удаляет все ноды и связи
- `evaluate` выполняет один запрос Cypher и возвращает значение из первого столбца первой записи.
- `exist`
- `match`
- `match_one` Сопоставить и вернуть одну связь с определенными критериями.
- `merge`
- `name` имя графа
- `nodes` поиск нод по свойствам

  ```python
    graph = Graph()
    graph.nodes[1234]
    (_1234:Person {name: 'Alice'})
    graph.nodes.get(1234)
    (_1234:Person {name: 'Alice'})
    graph.nodes.match("Person", name="Alice").first()
    (_1234:Person {name: 'Alice'})
  ```

- `pull(subgraph)` получение данных сч реплик
- `push(subgraph)[source]`
- `query` один ридонли запрос с автокоммитом
- `relationships` Это можно использовать для поиска отношений, соответствующих заданным критериям, а также для эффективного подсчета отношений.
- `rollback`
- `run` один ри/райт запрос с автокоммитом
- `schema` схема графа
- `separate(subgraph)` удаление отношенийсоответствующих подграфу
- `service` сервис, в который входит объект Graph
- `update`

## [Node and relationship matching](https://py2neo.org/2021.1/matching.html)

Модуль py2neo.matching предоставляет функциональные возможности для сопоставления узлов и отношений в соответствии с определенными критериями. Для каждого типа сущности предусмотрены класс Matcher и класс Match. Сопоставитель можно использовать для выполнения базового выбора, возвращая совпадение, которое само может быть оценено или уточнено.

- [NodeMatcher](https://py2neo.org/2021.1/matching.html#nodematcher-objects)

  ```python
    >>> from py2neo import Graph
    >>> from py2neo.matching import *
    >>> g = Graph()
    >>> nodes = NodeMatcher(g)
    >>> keanu = nodes.match("Person", name="Keanu Reeves").first()
    >>> keanu
    Node('Person', born=1964, name='Keanu Reeves')
   ```

- [NodeMatch](https://py2neo.org/2021.1/matching.html#nodematch-objects)
  - `iter(match)`
  - `len(match)`
  - `all()`
  - `count()`
  - `exist()`
  - `fiest()`
  - `limit(amount)`
  - `order_by(fields)`
  - `skip(amount)`
  - `where(*predicates, **properties)`
- [RelationshipMatcher](https://py2neo.org/2021.1/matching.html#relationshipmatcher-objects)
- [RelationshipMatch](https://py2neo.org/2021.1/matching.html#relationshipmatch-objects)
- [Applying predicates](https://py2neo.org/2021.1/matching.html#applying-predicates)

  ```python
    >>> nodes.match("Person", name=STARTS_WITH("John")).all()
    [Node('Person', born=1966, name='John Cusack'),
    Node('Person', born=1950, name='John Patrick Stanley'),
    Node('Person', born=1940, name='John Hurt'),
    Node('Person', born=1960, name='John Goodman'),
    Node('Person', born=1965, name='John C. Reilly')]
  ```

- [Ordering and limiting](https://py2neo.org/2021.1/matching.html#ordering-and-limiting)

## [Errors](https://py2neo.org/2021.1/errors.html)

## [Graph data types](https://py2neo.org/2021.1/data/index.html)

- [Node objects](https://py2neo.org/2021.1/data/index.html#node-objects)

  ```python
    >>> from py2neo import Node
    >>> a = Node("Person", name="Alice")
  ```

- [Relationship objects](https://py2neo.org/2021.1/data/index.html#relationship-objects)

  ```python
    >>> c = Node("Person", name="Carol")
    >>> class WorksWith(Relationship): pass
    >>> ac = WorksWith(a, c)
    >>> type(ac)
    'WORKS_WITH
  ```

- [Path objects](https://py2neo.org/2021.1/data/index.html#path-objects)

  ```python
    >>> from py2neo import Node, Path
    >>> alice, bob, carol = Node(name="Alice"), Node(name="Bob"), Node(name="Carol")
    >>> abc = Path(alice, "KNOWS", bob, Relationship(carol, "KNOWS", bob), carol)
    >>> abc
    <Path order=3 size=2>
    >>> abc.nodes
    (<Node labels=set() properties={'name': 'Alice'}>,
    <Node labels=set() properties={'name': 'Bob'}>,
    <Node labels=set() properties={'name': 'Carol'}>)
    >>> abc.relationships
    (<Relationship type='KNOWS' properties={}>,
    <Relationship type='KNOWS' properties={}>)
    >>> dave, eve = Node(name="Dave"), Node(name="Eve")
    >>> de = Path(dave, "KNOWS", eve)
    >>> de
    <Path order=2 size=1>
    >>> abcde = Path(abc, "KNOWS", de)
    >>> abcde
    <Path order=5 size=4>
    >>> for relationship in abcde.relationships:
    ...     print(relationship)
    ({name:"Alice"})-[:KNOWS]->({name:"Bob"})
    ({name:"Carol"})-[:KNOWS]->({name:"Bob"})
    ({name:"Carol"})-[:KNOWS]->({name:"Dave"})
    ({name:"Dave"})-[:KNOWS]->({name:"Eve"})
  ```

- [Subgraph objects](https://py2neo.org/2021.1/data/index.html#subgraph-objects)

  ```python
    >>> s = ab | ac
    >>> s
    {(alice:Person {name:"Alice"}),
    (bob:Person {name:"Bob"}),
    (carol:Person {name:"Carol"}),
    (Alice)-[:KNOWS]->(Bob),
    (Alice)-[:WORKS_WITH]->(Carol)}
    >>> s.nodes()
    frozenset({(alice:Person {name:"Alice"}),
            (bob:Person {name:"Bob"}),
            (carol:Person {name:"Carol"})})
    >>> s.relationships()
    frozenset({(Alice)-[:KNOWS]->(Bob),
            (Alice)-[:WORKS_WITH]->(Carol)})
  ```

## [Geo-spatial data types](https://py2neo.org/2021.1/data/spatial.html)

## [Cypher](https://py2neo.org/2021.1/cypher/index.html)

### [Cursor objects](https://py2neo.org/2021.1/cypher/index.html#cursor-objects)

Курсор можно рассматривать как окно в базовый поток данных. Все курсоры в py2neo «только вперед», что означает, что навигация начинается до первой записи и может продолжаться только в прямом направлении.

Обычно коду приложения не требуется создавать экземпляр курсора напрямую, поскольку он будет возвращен любым методом выполнения Cypher. Для создания курсора требуется только объект `DataSource`, который содержит логику доступа к исходным данным, по которым перемещается курсор.

Для многих простых случаев использования курсора требуется только метод `forward()` и текущий атрибут.

```python
# navigate over all available records
while cursor.forward():
    print(cursor.current["name"])

# get first record
if cursor.forward():
    print(cursor.current["name"])

# or
print(next(cursor)["name"])

# use in a loop (ass iterable)
for record in cursor:
    print(record["name"])

# return first value for queries that return a value
print(cursor.evaluate())
```

`data`  возвращает весь результат как список словарей

```python
>>> from py2neo import Graph
>>> graph = Graph()
>>> graph.run("MATCH (a:Person) RETURN a.name, a.born LIMIT 4").data()
[{'a.born': 1964, 'a.name': 'Keanu Reeves'},
 {'a.born': 1967, 'a.name': 'Carrie-Anne Moss'},
 {'a.born': 1961, 'a.name': 'Laurence Fishburne'},
 {'a.born': 1960, 'a.name': 'Hugo Weaving'}]
```

[Больше rerurn опции смотри тут](https://py2neo.org/2021.1/cypher/index.html#cursor-objects)

### [Record objects](https://py2neo.org/2021.1/cypher/index.html#record-objects)

Объект `Record` содержит упорядоченную коллекцию значений с ключами. Он во многом похож на namedtuple, но разрешает доступ к полям только с помощью синтаксиса, заключенного в квадратные скобки, и предоставляет больше функциональных возможностей. Запись расширяет как кортеж, так и отображение.

### [Running procedures](https://py2neo.org/2021.1/cypher/index.html#running-procedures)

### [Utilities](https://py2neo.org/2021.1/cypher/index.html#utilities)

### [Cypher Lexer](https://py2neo.org/2021.1/cypher/lexer.html)

Этот модуль содержит лексер языка Cypher, основанный на платформе лексера Pygments. Это можно использовать для анализа операторов и выражений для варианта Cypher, доступного в Neo4j 3.4.

### [Cypher Query Generation Functions](https://py2neo.org/2021.1/cypher/queries.html)

## [Bulk data operations](https://py2neo.org/2021.1/bulk/index.html)

Этот модуль содержит средства для выполнения операций с большими объемами данных, таких как создание или слияние узлов и связей.

## [Exporting data](https://py2neo.org/2021.1/bulk/export.html)

Этот модуль позволяет экспортировать данные во внешние форматы.

```python
>>> from py2neo import Graph
>>> from py2neo.export import to_pandas_data_frame
>>> graph = Graph()
>>> to_pandas_data_frame(graph.run("MATCH (a:Person) RETURN a.name, a.born LIMIT 4"))
   a.born              a.name
0    1964        Keanu Reeves
1    1967    Carrie-Anne Moss
2    1961  Laurence Fishburne
3    1960        Hugo Weaving
```

## [Object-Graph Mapping](https://py2neo.org/2021.1/ogm/index.html)

Пакет py2neo.ogm содержит набор средств для сваинга объектов Python к основному набору даных графа. Определения классов расширяют модель и включают определения свойств и меток, а также сведения о связанных объектах.

```python
class Movie(Model):
    __primarykey__ = "title"

    title = Property()
    tag_line = Property("tagline")
    released = Property()

    actors = RelatedFrom("Person", "ACTED_IN")
    directors = RelatedFrom("Person", "DIRECTED")
    producers = RelatedFrom("Person", "PRODUCED")


class Person(Model):
    __primarykey__ = "name"

    name = Property()
    born = Property()

    acted_in = RelatedTo(Movie)
    directed = RelatedTo(Movie)
    produced = RelatedTo(Movie)
```

### [Repositories](https://py2neo.org/2021.1/ogm/index.html#repositories)

Конструктор этого класса имеет такую ​​же сигнатуру, что и конструктор класса Graph.

```python
>>> from py2neo.ogm import Repository
>>> from py2neo.ogm.models.movies import Movie
>>> repo = Repository("bolt://neo4j@localhost:7687", password="password")
>>> repo.match(Movie, "The Matrix").first()
<Movie title='The Matrix'>
```

### [Models](https://py2neo.org/2021.1/ogm/index.html#models)

В основе структуры py2neo OGM лежит Model. Это базовый класс для всех классов, которые должны отображаться в базе данных графа. Каждая Model содержит узел, а также набор указателей на RelatedObjects и сведения об отношениях, которые их соединяют.

Экземпляр Model может быть создан так же, как и любой другой объект Python, но также может быть сопоставлен с базой данных. Каждый экземпляр может содержать атрибуты, представляющие метки, узлы или связанные объекты.

### [Properties](https://py2neo.org/2021.1/ogm/index.html#properties)

Свойство, определенное в модели, предоставляет доступ к свойству определенного моделью узла.

```python
>>> class Person(Model):
...     name = Property()
...
>>> alice = Person()
>>> alice.name = "Alice Smith"
>>> alice.name
"Alice Smith"
```

### [Labels](https://py2neo.org/2021.1/ogm/index.html#labels)

Метка, определенная в модели, предоставляет средство доступа к метке узла. Она отображается как логическое значение, настройка которого позволяет включать или выключать метку.

Метки отображаются в API так же, как логические свойства. Разница между ними заключается в том, как значение преобразуется в базу данных графа. Обычно метку следует использовать, если для этого значения регулярно выполняются сопоставления. Вторичная или вспомогательная информация может храниться в логическом свойстве (bolean propertie).

```python
>>> class Food(Model):
...     hot = Label()
...
>>> pizza = Food()
>>> pizza.hot
False
>>> pizza.hot = True
>>> pizza.hot
True
```

### [Related Objects](https://py2neo.org/2021.1/ogm/index.html#related-objects)

Связанные объекты — это экземпляры Model, определенным образом связанные с данной Model.

```python
# for (:Person)-[:LIKES]->(:Person)
class Person(Model):
    __primarykey__ = "name"

    name = Property()

    likes = RelatedTo("Person")
```

### [Object Matching](https://py2neo.org/2021.1/ogm/index.html#object-matching)

Один или несколько экземпляров модели могут быть выбраны из базы данных с помощью метода match соответствующего подкласса.

```python
>>> Person.match(graph, "Keanu Reeves").first()
<Person name='Keanu Reeves'>

>>> list(Person.match(graph).where("_.name =~ 'K.*'"))
[<Person name='Keanu Reeves'>,
 <Person name='Kevin Bacon'>,
 <Person name='Kiefer Sutherland'>,
 <Person name='Kevin Pollak'>,
 <Person name='Kelly McGillis'>,
 <Person name='Kelly Preston'>]
```

Читай еще:

- [документация](https://py2neo.org/2021.1/)
- [simple example](https://github.com/elena/py2neo-quickstart)
- [[neo4j]]
- [[python-api-neo4j]]
- [[cypher]]
- [[graphs]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[neo4j]: neo4j "Neo4j graph data base"
[neo4j]: neo4j "Neo4j graph data base"
[cypher]: cypher "Cypher query language"
[neo4j]: neo4j "Neo4j graph data base"
[python-api-neo4j]: python-api-neo4j "Python api for neo4j"
[cypher]: cypher "Cypher query language"
[graphs]: ../lists/graphs "Machine learning with graphs"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[neo4j]: neo4j "Neo4j graph data base"
[neo4j]: neo4j "Neo4j graph data base"
[cypher]: cypher "Cypher query language"
[neo4j]: neo4j "Neo4j graph data base"
[python-api-neo4j]: python-api-neo4j "Python api for neo4j"
[cypher]: cypher "Cypher query language"
[graphs]: ../lists/graphs "Machine learning with graphs"
[//end]: # "Autogenerated link references"