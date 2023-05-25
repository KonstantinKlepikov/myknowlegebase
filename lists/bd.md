---
description: Список заметок о базах данных
title: Data Bases
tags: data-bases
category: list
---
## SQL

- [[postgres]]
- [[databases]] Пакет python для ассинхронной работы с базами данных
- [[sqlalchemy]]
- [[ormar]] The ormar package is an async mini ORM for Python
- [SurrealDB](https://github.com/surrealdb/surrealdb) is an end-to-end cloud native database for web, mobile, serverless, Jamstack, backend, and traditional applications

## NOSQL and Graph data-bases

- [[mongodb]]
- [[apache-hadoop]]
- [[apache-spark]]
- [Apache Cassandra](https://cassandra.apache.org/_/index.html) OpenSource NoSQL DB
- [FaunaDB](https://fauna.com/) Combines the flexibility of NoSQL with the relational querying capabilities and ACID consistency of SQL systems with native [[graphql]]
- [TypeDB](https://github.com/vaticle/typedb) is a strongly-typed database with a rich and logical type system. TypeDB empowers you to tackle complex problems, and TypeQL is its query language.
- [SpiceDB](https://github.com/authzed/spicedb) is an open source, Google Zanzibar-inspired, database system for creating and managing security-critical application permissions.

- [TigerGraphDB](https://www.tigergraph.com/tigergraph-db/) The First Native Parallel Graph (NPG)
- [[neo4j]]
- [[dgraph]] is a horizontally scalable and distributed GraphQL database with a graph backend. It provides ACID transactions, consistent replication, and linearizable reads. It's built from the ground up to perform for a rich set of queries. Being a native GraphQL database, it tightly controls how the data is arranged on disk to optimize for query performance and throughput, reducing disk seeks and network calls in a cluster.
- [[janus-graph]] s a highly scalable graph database optimized for storing and querying large graphs with billions of vertices and edges distributed across a multi-machine cluster. JanusGraph is a transactional database that can support thousands of concurrent users, complex traversals, and analytic graph queries.
- [Cayley](https://github.com/cayleygraph/cayley) is an open-source database for Linked Data. It is inspired by the graph database behind Google's Knowledge Graph (formerly Freebase).
- [HugeGraph](https://github.com/apache/incubator-hugegraph) is a fast-speed and highly-scalable graph database. Billions of vertices and edges can be easily stored into and queried from HugeGraph due to its excellent OLTP ability. As compliance to Apache TinkerPop 3 framework, various complicated graph queries can be accomplished through Gremlin
- [XTDB](https://github.com/xtdb/xtdb) is a general purpose database with graph-oriented bitemporal indexes. Datalog, SQL & EQL queries are supported, and Java, HTTP & Clojure APIs are provided.
- [Cozo](https://github.com/cozodb/cozo) is a general-purpose, transactional, relational database that uses Datalog for query, is embeddable but can also handle huge amounts of data and concurrency, and focuses on graph data and algorithms
- [RedisGraph](https://github.com/RedisGraph/RedisGraph) is a graph database module for Redis
- [IndraDB](https://github.com/indradb/indradb) A graph database written in rust. Has [python binding](https://github.com/indradb/python-client).
- [Gaffer](https://github.com/gchq/Gaffer) is a graph database framework. It allows the storage of very large graphs containing rich properties on the nodes and edges. Several storage options are available, including Accumulo, Hbase and Parquet.
- [Apache TinkerPop](https://github.com/apache/tinkerpop)™ provides graph computing capabilities for both graph databases (OLTP) and graph analytic systems (OLAP).
- [Memgraph](https://github.com/memgraph/memgraph) Open-source graph database, built for real-time streaming data, compatible with [[neo4j]].

- [ArangoDB](https://github.com/arangodb/arangodb) is a scalable open-source multi-model database natively supporting graph, document and search.
- [NebulaGraph](https://github.com/vesoft-inc/nebula) is a popular open-source graph database that can handle large volumes of data with milliseconds of latency, scale up quickly, and have the ability to perform fast graph analytics. NebulaGraph has been widely used for social media, recommendation systems, knowledge graphs, security, capital flows, AI, etc.
- [OrientDB](https://orientdb.org/) is an Open Source Multi-Model NoSQL DBMS with the support of Native Graphs, Documents, Full-Text search, Reactivity, Geo-Spatial and Object Oriented concepts

- [Qdrant](https://github.com/qdrant/qdrant) - Vector Search Engine and Database for the next generation of AI applications. Also available in the cloud

### Triplet storages

- [ClioPatria](https://cliopatria.swi-prolog.org/home) is a SWI-Prolog application that integrates SWI-Prolog's the SWI-Prolog libraries for [[rdf]] and [[http]] services into a ready to use [[semantic-web]] server (**very old**)
- [OpenLink Virtuoso](https://virtuoso.openlinksw.com/) is a secure and high-performance platform for modern data access, integration, virtualization, and multi-model data management (tables & graphs) based on innovative support of existing open standards (e.g., SQL, SPARQL, and GraphQL).
- [[apache-jena]]
- [Eclipse RDF4J](https://rdf4j.org/) Java framework for processing and handling RDF data. This includes creating, parsing, scalable storage, reasoning and querying with RDF and Linked Data. It offers an easy-to-use API that can be connected to all leading RDF database solutions. It allows you to connect with SPARQL endpoints and create applications that leverage the power of linked data and Semantic Web.
- [Marklogic](https://www.marklogic.com/)
- [[ontotext-graphdb]]
- [4store](https://github.com/4store/4store) is an efficient, scalable and stable RDF database. **so old**
- [[alegrograph]]
- [Blazegraph](https://blazegraph.com/)™ DB is a ultra high-performance graph database supporting Blueprints and RDF/SPARQL APIs. It supports up to 50 Billion edges on a single machine. It is in production use for Fortune 500 customers such as EMC, Autodesk, and many others. It is supporting key Precision Medicine applications and has wide-spread usage for life science applications. It is used extensively to support Cyber analytics in commercial and government applications. It powers the Wikimedia Foundation's Wikidata Query Service.
- [Cayley](https://github.com/cayleygraph/cayley) is an open-source database for Linked Data. It is inspired by the graph database behind Google's Knowledge Graph (formerly Freebase).

По поводу дб для knowledge graphs смотри [[knowledge-graphs]]

## query languages

- [[cypher]]
- [[sparql]]
- [[apache-tinkertop-and-gremlin]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[postgres]: ../notes/postgres "Postgres"
[databases]: ../notes/databases "Databases python"
[sqlalchemy]: sqlalchemy "Sqlalchemy"
[ormar]: ../notes/ormar "Ormar"
[mongodb]: ../notes/mongodb "MongoDB"
[apache-hadoop]: ../notes/apache-hadoop "Apache hadoop"
[apache-spark]: ../notes/apache-spark "Unified engine for large-scale data analytics"
[graphql]: ../notes/graphql "Язык и система организации АПИ GraphQL"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[dgraph]: ../notes/dgraph "Dgraph"
[janus-graph]: ../notes/janus-graph "Janus Graph"
[rdf]: ../notes/rdf "RDF"
[http]: http "Http"
[semantic-web]: ../notes/semantic-web "Semantic web"
[apache-jena]: ../notes/apache-jena "Apache JENA"
[ontotext-graphdb]: ../notes/ontotext-graphdb "Ontotext graph-db"
[alegrograph]: ../notes/alegrograph "Alegro graph"
[knowledge-graphs]: knowledge-graphs "Knowledge graphs"
[cypher]: ../notes/cypher "Cypher query language"
[sparql]: ../notes/sparql "SPARQL"
[apache-tinkertop-and-gremlin]: ../notes/apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[//end]: # "Autogenerated link references"