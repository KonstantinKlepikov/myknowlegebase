---
description: Сборник заметок про графовые алгоритмы машинного обучения
title: Machine learning with graphs
tags: machine-learning graphs
category: list
---
[graph-based-deep-learning-literature](https://github.com/naganandy/graph-based-deep-learning-literature)

Библиотеки, работающие с графами:

- [[pyg]] pytorch geometric
- [Networkx](https://networkx.org/)
- [Scikit-Network](https://scikit-network.readthedocs.io/en/latest/index.html#)
- [graph-tool](https://graph-tool.skewed.de/)
- [dgl.ai](https://www.dgl.ai/)
- [igraph](https://igraph.org/)
- [networkit](https://networkit.github.io/)
- [nx-cugraph](https://github.com/rapidsai/nx-cugraph/) GPU Accelerated Backend for NetworkX
- [RAPIDS cuGraph](https://github.com/rapidsai/cugraph) is a monorepo that represents a collection of packages focused on GPU-accelerated graph analytics, including support for property graphs, remote (graph as a service) operations, and graph neural (GNNs). cuGraph supports the creation and manipulation of graphs followed by the execution of scalable fast graph algorithms. Включает nx-cugraph, a [[networkx]] backend that provides GPU acceleration to NetworkX with zero code change.
- [SNAP](https://snap.stanford.edu/snap/)
- [deep snap](https://snap.stanford.edu/deepsnap/)
- [GraphGym](https://github.com/snap-stanford/GraphGym). GraphGym is a platform for designing and evaluating Graph Neural Networks (GNN)
- [Stellar Graph](https://stellargraph.readthedocs.io/en/stable/index.html#) Machine Learning on Graphs
- [Neo4j Graph Algorithms](https://neo4j.com/developer/graph-data-science/graph-algorithms/)
- [[apache-spark]] Unified engine for large-scale data analytics
- [[apache-tinkertop-and-gremlin]] Apache TinkerPop™ is a graph computing framework for both graph databases (OLTP) and graph analytic systems (OLAP)
- [SciGraph](https://github.com/SciGraph/SciGraph) Represent ontologies and ontology-encoded knowledge in a [[neo4j]] graph.
- [GraphRAG](https://microsoft.github.io/graphrag/) s a structured, hierarchical approach to Retrieval Augmented Generation (RAG), as opposed to naive semantic-search approaches using plain text snippets. The GraphRAG process involves extracting a knowledge graph out of raw text, building a community hierarchy, generating summaries for these communities, and then leveraging these structures when perform RAG-based tasks.
- [PyTorch-BigGraph](https://github.com/facebookresearch/PyTorch-BigGraph) Generate embeddings from large-scale graph-structured data.

- [Бенчмарк](https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages-v2)
- [Community detection for NetworkX](https://python-louvain.readthedocs.io/en/latest/index.html) Louvain Community Detection
- [CSRGraphs](https://github.com/VHRanger/CSRGraph) - Fast and memory efficient library for large read-only graphs
- [nodevectors](https://github.com/VHRanger/nodevectors) some alghoritms, depends on CSRGraphs
- [torchpr](https://github.com/mberr/torch-ppr) (Personalized) Page-Rank computation using PyTorch
- [karateclub](https://github.com/benedekrozemberczki/KarateClub) is an unsupervised machine learning extension library for [NetworkX](https://networkx.org/)
- [GraphWorld](https://github.com/google-research/graphworld) toolbox for graph learning researchers to systematically test new models on synthetic graph datasets. [More info](https://ai.googleblog.com/2022/05/graphworld-advances-in-graph.html)
- [GraphGalery](https://github.com/EdisonLeeeee/GraphGallery) GraphGallery is a gallery for benchmarking Graph Neural Networks (GNNs)
- [Large graphs datasets](https://law.di.unimi.it/datasets.php)
- [Networks](http://konect.cc/networks/) большая коллекция графовых датасетов с их описанием и подсчитанными метриками
- [Leaderboards](https://ogb.stanford.edu/docs/leader_overview/) allow researchers to keep track of state-of-the-art methods and encourage reproducible research.

- [Tools created by the OSoMe team](https://osome.iu.edu/tools)

## Boocs, cources

- [Graph Representation Learning Book](https://www.cs.mcgill.ca/~wlh/grl_book/)
- [network science book](https://networksciencebook.com/) Barabashi
- [Networks, Crowds, and Markets: Reasoning About a Highly Connected World](https://www.cs.cornell.edu/home/kleinber/networks-book/)  combines different scientific perspectives in its approach to understanding networks and behavior. Drawing on ideas from economics, sociology, computing and information science, and applied mathematics, it describes the emerging field of study that is growing at the interface of all these areas, addressing fundamental questions about how the social, economic, and technological worlds are connected.
- [Leaderboards](https://ogb.stanford.edu/docs/leader_overview/) allow researchers to keep track of state-of-the-art methods and encourage reproducible research.

## Graph [[bd]]

- [[neo4j]]
- [[dgraph]]
- [[janus-graph]]
- [TigerGraphDB](https://www.tigergraph.com/tigergraph-db/) The First Native Parallel Graph (NPG)
- [Ontotext GraphDB](https://www.ontotext.com/products/graphdb/?ref=menu). RDF Database for Knowledge Graphs. [docker](https://github.com/Ontotext-AD/graphdb-docker)
- [UKV](https://github.com/unum-cloud/UKV). UKV is an open C-layer binary standard for "Create, Read, Update, Delete" operations, or CRUD for short.
- [Tom Sawyer Graph Database Browser](https://www.tomsawyer.com/graph-database-browser)
- [Neo4j web brouser](https://neo4j.com/docs/browser-manual/current/deployment-modes/dedicated-web-server/) dedicated installation

Смотри еще:

- [[knowledge-graphs]]
- [[graph-visualization]]
- [[networkx]]
- [[pyg]]
- [[neo4j-ml]]
- [[cypher]]
- [[python-api-neo4j]]
- [[pytoneo]] python package for neo4j and cypher
- [[graphql]]
- [[sparql]]
- [[pytorch]]
- [[machine-learning]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[pyg]: ../notes/pyg "Pytorch geometric"
[networkx]: ../notes/networkx "Networkx"
[apache-spark]: ../notes/apache-spark "Unified engine for large-scale data analytics"
[apache-tinkertop-and-gremlin]: ../notes/apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[bd]: bd "Data Bases"
[dgraph]: ../notes/dgraph "Dgraph"
[janus-graph]: ../notes/janus-graph "Janus Graph"
[knowledge-graphs]: knowledge-graphs "Knowledge graphs"
[graph-visualization]: ../notes/graph-visualization "Graph visualization"
[neo4j-ml]: ../notes/neo4j-ml "Machine learning in Neo4j"
[cypher]: ../notes/cypher "Cypher query language"
[python-api-neo4j]: ../notes/python-api-neo4j "Python api for neo4j"
[pytoneo]: ../notes/pytoneo "pytoneo client library and toolkit for working with neo4j"
[graphql]: ../notes/graphql "Язык и система организации АПИ GraphQL"
[sparql]: ../notes/sparql "SPARQL"
[pytorch]: ../notes/pytorch "Machine learning framework pytorch"
[machine-learning]: machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[pyg]: ../notes/pyg "Pytorch geometric"
[apache-spark]: ../notes/apache-spark "Unified engine for large-scale data analytics"
[apache-tinkertop-and-gremlin]: ../notes/apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[bd]: bd "Data Bases"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[dgraph]: ../notes/dgraph "Dgraph"
[janus-graph]: ../notes/janus-graph "Janus Graph"
[knowledge-graphs]: knowledge-graphs "Knowledge graphs"
[graph-visualization]: ../notes/graph-visualization "Graph visualization"
[networkx]: ../notes/networkx "Networkx"
[pyg]: ../notes/pyg "Pytorch geometric"
[neo4j-ml]: ../notes/neo4j-ml "Machine learning in Neo4j"
[cypher]: ../notes/cypher "Cypher query language"
[python-api-neo4j]: ../notes/python-api-neo4j "Python api for neo4j"
[pytoneo]: ../notes/pytoneo "pytoneo client library and toolkit for working with neo4j"
[graphql]: ../notes/graphql "Язык и система организации АПИ GraphQL"
[sparql]: ../notes/sparql "SPARQL"
[pytorch]: ../notes/pytorch "Machine learning framework pytorch"
[machine-learning]: machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"