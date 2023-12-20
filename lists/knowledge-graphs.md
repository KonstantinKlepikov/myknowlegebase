---
description: Графы знаний
title: Knowledge graphs
tags: machine-learning graphs knowledge-graphs
category: list
---
## Bases

- [[semantic-web]]
- [[rdf]]
- [[owl]]
- [[turtle]]
- [w3c semantic web wiki](https://www.w3.org/2001/sw/wiki/Main_Page)
- [W3c ALL STANDARDS AND DRAFTS](https://www.w3.org/TR/?tag=data)
- [W3c linking data](https://www.w3.org/wiki/LinkedData) note
- [SPIN](https://spinrdf.org/) is a W3C Member Submission that has become the de-facto industry standard to represent SPARQL rules and constraints on Semantic Web models. SPIN also provides meta-modeling capabilities that allow users to define their own SPARQL functions and query templates. Finally, SPIN includes a ready to use library of common functions.
- [SPIN - SPARQL Syntax](https://www.w3.org/Submission/spin-sparql/)
- [DASH Constraint Components](https://datashapes.org/constraints.html). The DASH namespace includes a collection of SHACL constraint components that extend the Core of SHACL with new constraint types. This document introduces these additional constraint components.
- [GRDDL](https://www.w3.org/2001/sw/wiki/GRDDL) (Gleaning Resource Descriptions from Dialects of Languages) - is a technique for obtaining RDF data from XML documents and in particular XHTML pages. Now is not supported.
- w3c [Converters to RDF ](https://www.w3.org/wiki/ConverterToRdf) list
- [Schema.org](https://schema.org/) is a collaborative, community activity with a mission to create, maintain, and promote schemas for structured data on the Internet, on web pages, in email messages, and beyond.
- [protege](https://protege.stanford.edu/). A free, open-source ontology editor and framework for building intelligent systems. [Docs](https://protegewiki.stanford.edu/wiki/Main_Page)
- [SPARQL Web Pages](https://uispin.org/) (SWP) is an RDF-based framework to describe user interfaces for rendering Semantic Web data

## Курсы и книги

- [курс лекций семантический web МИФИ](https://www.youtube.com/channel/UCTUhNxKRFtOHIW9ytAHbSDA/videos). [Ресусры курса](http://env-8380827.jelastic.regruhosting.ru/index_x.html).
- [KG Course (youtube)](https://www.youtube.com/playlist?list=PLlmfdv64-P33ROIzuATAWEp0V1jMXAoj_). [Site](https://migalkin.github.io/kgcourse2021/). Курс по графам знаний (Knowledge Graphs) и как их готовить в 2021 году.
- [kgbook](https://kgbook.org/)ю This book provides a comprehensive and accessible introduction to knowledge graphs, which have recently garnered notable attention from both industry and academia.

## Статьи

- [Evaluation of Metadata Representations in RDF stores](http://www.semantic-web-journal.net/system/files/swj1791.pdf)
- [A Toolkit for Generating Code Knowledge Graphs](https://arxiv.org/pdf/2002.09440.pdf) ([GraphGen4Code](https://github.com/wala/graph4code))
- [RDF 1.1: Knowledge Representation and Data Integration Language for the Web](https://arxiv.org/pdf/2001.00432.pdf)
- [Interactively Constructing Knowledge Graphs from Messy User-Generated Spreadsheets](https://arxiv.org/pdf/2103.03537.pdf)
- [OBDA for the WEb: Creating Virtual RDF Graphs On Top of Web Data Sources](https://arxiv.org/pdf/2005.11264.pdf)

## Data

- [[wikidata]]
- [dbpedia access](http://wikidata.dbpedia.org/OnlineAccess)
- [YAGO](https://yago-knowledge.org/): YAGO is a large knowledge base with general knowledge about people, cities, countries, movies, and organizations.
- [The Linked Open Data Cloud](https://lod-cloud.net/)

## Frameworks, languages, db and tools

- [RDFLib](https://github.com/RDFLib) python tools:
  - [RDFLIB](https://github.com/RDFLib/rdflib) RDFLib is a pure Python package for working with RDF. RDFLib contains most things you need to work with RDF, including:
    - parsers and serializers for RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, Trig and JSON-LD
    - a Graph interface which can be backed by any one of a number of Store implementations
    - store implementations for in-memory, persistent on disk (Berkeley DB) and remote SPARQL endpoints
    - a SPARQL 1.1 implementation - supporting SPARQL 1.1 Queries and Update statements
    - SPARQL function extension mechanisms
    - [docs](https://rdflib.readthedocs.io/en/stable/)
  - [sparqlwrapper](https://github.com/RDFLib/sparqlwrapper)
  - [pyshacl](https://github.com/RDFLib/pySHACL)
- [RASQAL](https://librdf.org/rasqal/) is a free software / Open Source C library that handles Resource Description Framework (RDF) query language syntaxes, query construction and execution of queries returning results as bindings, boolean, RDF graphs/triples or syntaxes. The supported query languages are SPARQL Query 1.0, SPARQL Query 1.1, SPARQL Update 1.1 (no executing) and the Experimental SPARQL extensions (LAQRS). Rasqal can write binding query results in the SPARQL XML, SPARQL JSON, CSV, TSV, HTML, ASCII tables, RDF/XML and Turtle / N3 and read them in SPARQL XML, CSV, TSV, RDF/XML and Turtle / N3.
- **[[bd]]**
  - [[ontotext-graphdb]]
  - [[neo4j]] rdf resources
    - [[neosematics]] [neosemantics](https://neo4j.com/labs/neosemantics/) (n10s) is a plugin that enables the use of RDF and its associated vocabularies like (OWL,RDFS,SKOS and others) in Neo4
    - [install](https://neo4j.com/labs/neosemantics/installation/)]
    - [Build a Knowledge Graph using NLP and Ontologies](https://neo4j.com/developer/graph-data-science/build-knowledge-graph-nlp-ontologies/) with Neo4j
  - [Eclipse RDF4J](https://rdf4j.org/). Eclipse RDF4J is an open source modular Java framework for working with RDF data. This includes parsing, storing, inferencing and querying of/over such data. It offers an easy-to-use API that can be connected to all leading RDF storage solutions. RDF4J offers a set of database implementations out of the box. [Repo](https://github.com/eclipse/rdf4j).
  - [[alegrograph]]
  - [[apache-jena]]
  - full list is here: [[bd]]
- [Awesome-knowledge-graph-question-answering](https://github.com/BshoterJ/awesome-kgqa) A collection of some materials of knowledge graph question answering
- [OpenRefine](https://github.com/OpenRefine)
  - [OpenRefine](https://github.com/OpenRefine/OpenRefine) is a Java-based power tool that allows you to load data, understand it, clean it up, reconcile it, and augment it with data coming from the web. All from a web browser and the comfort and privacy of your own computer. [Website](https://openrefine.org/).
- [XWiki](https://www.xwiki.org/xwiki/bin/view/Main/WebHome). First generation wikis are used to collaborate on content. [Second generation wikis](https://www.xwiki.org/xwiki/bin/view/Documentation/UserGuide/Features/SecondGenerationWiki/) (a.k.a Structured and Applications Wikis) can be used to create collaborative web applications (by using the wiki paradigm and editing wiki pages). XWiki can be used either as a first generation wiki or a second generation one.

## Site templating

- [jekill-rdf](https://github.com/AKSW/jekyll-rdf). A Jekyll plugin for including RDF data in static site. [Paper](https://arxiv.org/pdf/2201.00618.pdf)

## Other

- [Knowledge Base Question Answering (KBQA)](http://docs.deeppavlov.ai/en/master/features/models/kbqa.html) on [DeepPavlov](https://github.com/deeppavlov/DeepPavlov)
- [Natural Language AI google service](https://cloud.google.com/natural-language#section-5) provides a set of features for analyzing unstructured text.
- [GraphGen4Code](https://github.com/wala/graph4code) uses generic techniques to capture code semantics with the key nodes in the graph representing classes, functions and methods.
- [Sindice](https://sindice.com/developers/welcome.html) RDF-search engine
- [Ontop4theWeb](https://github.com/ConstantB/Ontop4TheWeb) is a framework that extends the OBDA paradigm with the ability to query Web APIs (Foursquare, Twitter, Yelp, etc) and Web tables (HTML) using SPARQL on-the-fly, saving time and resources for developers and data scientists/engineers as data don't have to be downloaded and converted into RDF before querying. With Ontop4TheWeb, you can create a virtual OBDA repository and pose SPARQL queries to the Web APIs of your interest. The data will be transparently downloaded after posing the queries, thus retrieving the most up-to-date snapshots of data. For this reason, Ontop4TheWeb is suitable for querying On-the-fly data of high velocity, i.e., that get updated frequently.
- [RSSOwlnix](https://github.com/Xyrio/RSSOwlnix) is a fork of RSSOwl a powerful application to organize, search and read your RSS, RDF & Atom news feeds in a comfortable way. Highlights are saved searches, notifications, filters, fast fulltext search and a flexible, clean user interface.
- [stardog](https://www.stardog.com/) - enterprize knowledge-graphs platform

Смотри еще:

- [небольшая презентация по КГ](https://docs.google.com/presentation/d/1Artsa47IV_dSZkz7smXyAVZQmn3xDeZRO9Z_hVklirs/edit?usp=sharing) (на основе материалов курса М.Галкина)
- [[sparql]]
- [[apache-tinkertop-and-gremlin]]
- [[neo4j]]
- [[janus-graph]]
- [[graphs]]
- [[pyg]]
- [[machine-learning]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[semantic-web]: ..%2Fnotes%2Fsemantic-web "Semantic web"
[rdf]: ..%2Fnotes%2Frdf "RDF"
[owl]: ..%2Fnotes%2Fowl "OWL ontology"
[turtle]: ..%2Fnotes%2Fturtle "Turtle for RDF"
[wikidata]: wikidata "Wikidata"
[bd]: bd "Data Bases"
[ontotext-graphdb]: ..%2Fnotes%2Fontotext-graphdb "Ontotext graph-db"
[neo4j]: ..%2Fnotes%2Fneo4j "Neo4j graph data base"
[neosematics]: ..%2Fnotes%2Fneosematics "Neosematics"
[alegrograph]: ..%2Fnotes%2Falegrograph "Alegro graph"
[apache-jena]: ..%2Fnotes%2Fapache-jena "Apache JENA"
[sparql]: ..%2Fnotes%2Fsparql "SPARQL"
[apache-tinkertop-and-gremlin]: ..%2Fnotes%2Fapache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[janus-graph]: ..%2Fnotes%2Fjanus-graph "Janus Graph"
[graphs]: graphs "Machine learning with graphs"
[pyg]: ..%2Fnotes%2Fpyg "Pytorch geometric"
[machine-learning]: machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[semantic-web]: ../notes/semantic-web "Semantic web"
[rdf]: ../notes/rdf "RDF"
[owl]: ../notes/owl "OWL ontology"
[turtle]: ../notes/turtle "Turtle for RDF"
[wikidata]: wikidata "Wikidata"
[bd]: bd "Data Bases"
[ontotext-graphdb]: ../notes/ontotext-graphdb "Ontotext graph-db"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[neosematics]: ../notes/neosematics "Neosematics"
[alegrograph]: ../notes/alegrograph "Alegro graph"
[apache-jena]: ../notes/apache-jena "Apache JENA"
[bd]: bd "Data Bases"
[sparql]: ../notes/sparql "SPARQL"
[apache-tinkertop-and-gremlin]: ../notes/apache-tinkertop-and-gremlin "Apache TinkerPop and Gremlin"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[janus-graph]: ../notes/janus-graph "Janus Graph"
[graphs]: graphs "Machine learning with graphs"
[pyg]: ../notes/pyg "Pytorch geometric"
[machine-learning]: machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"