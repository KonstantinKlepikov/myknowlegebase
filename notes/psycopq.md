---
description: Коннектор для зщыепкуы
tags: data-bases sql
title: psycopq
---
Psycopg — самый популярный адаптер базы данных PostgreSQL для языка программирования Python. Его основными особенностями являются полная реализация спецификации Python DB API 2.0 и потокобезопасность (несколько потоков могут использовать одно и то же соединение). Он был разработан для многопоточных приложений, которые создают и уничтожают множество курсоров и выполняют большое количество одновременных операций INSERT или UPDATE.

- [Документация psycopq2](https://www.psycopg.org/docs/)
- [Документация psycopq3](https://www.psycopg.org/psycopg3/docs/)
- [SQL string composition для psycopq2](https://www.psycopg.org/docs/sql.html#psycopg2.sql.Identifier)

Вопросы и решения:

- [Passing list of parameters to SQL in psycopg2](https://stackoverflow.com/questions/8671702/passing-list-of-parameters-to-sql-in-psycopg2)
- [Postgres/psycopg2 - Inserting array of strings](https://stackoverflow.com/questions/6853161/postgres-psycopg2-inserting-array-of-strings)
- [Python/psycopg2 WHERE IN statement](https://stackoverflow.com/questions/28117576/python-psycopg2-where-in-statement)

Смотри еще:

- [[bd]]
- [[sql]]
- [[sqlalchemy]]
- [[postgres]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[bd]: ../lists/bd "Data Bases"
[sql]: sql "SQL"
[sqlalchemy]: ../lists/sqlalchemy "Sqlalchemy"
[postgres]: postgres "Postgres"
[//end]: # "Autogenerated link references"