---
description: Dgraph - native GraphQL Database With A Graph Backend
title: Dgraph
tags: data-bases graphs
---
- [dgraph](https://dgraph.io/) The Only Native GraphQL Database With A Graph Backend.
- [github repo](https://github.com/dgraph-io/dgraph)
- [docs](https://dgraph.io/docs/)
- [pydgraph](https://github.com/dgraph-io/pydgraph) dgraph python client

## Dgraph compared to other graph DBs

| Features | Dgraph | [[neo4j]] | [[janus-graph]] |
| -------- | ------ | ----- | ----------- |
| Architecture | Sharded and Distributed | Single server (+ replicas in enterprise) | Layer on top of other distributed DBs |
| Replication | Consistent | None in community edition (only available in enterprise) | Via underlying DB |
| Data movement for shard rebalancing | Automatic | Not applicable (all data lies on each server) | Via underlying DB |
| Language | [[graphql]] inspired | [[cypher]], [[apache-tinkertop-and-gremlin]] | [[apache-tinkertop-and-gremlin]] |
| Protocols | Grpc / HTTP + JSON / RDF | Bolt + Cypher | Websocket / HTTP |
| Transactions | Distributed ACID transactions | Single server ACID transactions | ~~Not typically ACID~~
| Full-Text Search | Native support | Native support | Via External Indexing System |
| Regular Expressions | Native support | Native support | Via External Indexing System |
| Geo Search | Native support | External support only | Via External Indexing System |
| License | Apache 2.0 | GPL v3 | Apache 2.0 |

[Comparison with oteher db and services](https://dgraph.io/comparison/) (Dgraph vs [[graphql]] platforms, [TigerGraphDB](https://www.tigergraph.com/tigergraph-db/), [[neo4j]], [FaunaDB](https://fauna.com/), [[mongodb]])

Смотри еще:

- [[graphs]]
- [[graphql]]
- [[neo4j]]
- [[mongodb]]
- [[bd]]


[neo4j]: neo4j "Neo4j graph data base"
[janus-graph]: janus-graph "Janus Graph"
[graphql]: graphql "Язык и система организации АПИ GraphQL"
[cypher]: cypher "Cypher query language"
[apache-tinkertop-and-gremlin]: apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[mongodb]: mongodb "MongoDB"
[graphs]: ../lists/graphs "Machine learning with graphs"
[bd]: ../lists/bd "Data Bases"


[neo4j]: neo4j "Neo4j graph data base"
[janus-graph]: janus-graph "Janus Graph"
[graphql]: graphql "Язык и система организации АПИ GraphQL"
[cypher]: cypher "Cypher query language"
[apache-tinkertop-and-gremlin]: apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[apache-tinkertop-and-gremlin]: apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[graphql]: graphql "Язык и система организации АПИ GraphQL"
[neo4j]: neo4j "Neo4j graph data base"
[mongodb]: mongodb "MongoDB"
[graphs]: ../lists/graphs "Machine learning with graphs"
[graphql]: graphql "Язык и система организации АПИ GraphQL"
[neo4j]: neo4j "Neo4j graph data base"
[mongodb]: mongodb "MongoDB"
[bd]: ../lists/bd "Data Bases"
