---
description: Mongomotor - async driver to mongodb
title: Mongomotor - асинхронный драйвер MongoDb
tags: data-bases mongodb asyncio
---
Motor presents a coroutine-based API for non-blocking access to MongoDB from [[tornado]] or [[asyncio]].

`$ python -m pip install motor`

## [Разница](https://motor.readthedocs.io/en/stable/differences.html) между pymongo и mongomotor

## Фичи

- Неблокирующий асинхронный драйвер для MongoDB. Его можно использовать из приложений Tornado или asyncio. Motor никогда не блокирует цикл обработки событий при подключении к MongoDB или выполнении операций ввода-вывода.
- Motor охватывает почти весь API PyMongo и делает его неблокирующим.
- Модуль `tornado.gen` позволяет использовать сопрограммы для упрощения асинхронного кода. Методы motor возвращают фьючерсы, которые удобно использовать с сопрограммами.
- Настраиваемые циклы ввода/вывода. Motor поддерживает приложения Tornado с несколькими файлами `IOLoops`. Передайте `io_loop` аргумент, чтобы настроить цикл для экземпляра `MotorClient`.
- Потоковая передача статических файлов из `GridFS`. Motor может передавать данные из GridFS в Tornado RequestHandler с помощью класса stream_to_handler() или GridFSHandler. Он также может обслуживать данные GridFS с помощью [[aiohttp]], используя AIOHTTPGridFSкласс.

## [Tutorial: Using Motor With Tornado](https://motor.readthedocs.io/en/stable/tutorial-tornado.html)

## [Tutorial: Using Motor With asyncio](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)

Motor, как и PyMongo, представляет данные с 4-уровневой иерархией объектов:

- `AsyncIOMotorClient` представляет процесс mongod или гуппу процессов. Вы явно создаете один из этих клиентских объектов, подключаете его к работающему mongod или mongods и используете его на протяжении всего времени существования вашего приложения.
- `AsyncIOMotorDatabase` каждый mongod имеет набор баз данных (отдельные наборы файлов данных на диске). Вы можете получить ссылку на базу данных от клиента.
- `AsyncIOMotorCollection` в базе данных есть набор коллекций, содержащих документы; вы получаете ссылку на коллекцию из базы данных.
- `AsyncIOMotorCursor` выполнение `find()` для `AsyncIOMotorCollection` получает `AsyncIOMotorCursor`, представляющий набор документов, соответствующих запросу.

- [Создание клиента](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#creating-a-client)
- [получение бд](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#getting-a-database)
- [получение коллекции](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#getting-a-collection)

```python
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.test_database
collection = db.test_collection
```

[Добавление документов](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#inserting-a-document)

```python
>>> async def do_insert():
...    document = {'key': 'value'}
...    result = await db.test_collection.insert_one(document)
...    print('result %s' % repr(result.inserted_id))


>>> import asyncio
>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_insert())
result ObjectId('...')
```

[Find one](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#getting-a-single-document-with-find-one)

```python
>>> async def do_find_one():
...    document = await db.test_collection.find_one({'i': {'$lt': 1}})
...    pprint.pprint(document)

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_find_one())
{'_id': ObjectId('...'), 'i': 0}
```

Используйте `find()` для запроса набора документов. `find()` не выполняет ввод-вывод и не требует выражения `await`. Он просто создает экземпляр `AsyncIOMotorCursor`. Запрос фактически выполняется на сервере, когда вы вызываете `to_list()` или выполняете асинхронный цикл for.

```python
>>> async def do_find():
...     cursor = db.test_collection.find({'i': {'$lt': 5}}).sort('i')
...     for document in await cursor.to_list(length=100):
...         pprint.pprint(document)

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_find())
{'_id': ObjectId('...'), 'i': 0}
{'_id': ObjectId('...'), 'i': 1}
{'_id': ObjectId('...'), 'i': 2}
{'_id': ObjectId('...'), 'i': 3}
{'_id': ObjectId('...'), 'i': 4}
```

Вы можете обрабатывать один документ за раз в асинхронном цикле for. Вы можете применить сортировку, ограничение или пропустить запрос, прежде чем начать итерацию.

```python
>>> async def do_find():
...     c = db.test_collection
...     # Modify the query before iterating
...     cursor.sort('i', -1).skip(1).limit(2)
...     async for document in cursor:
...         pprint.pprint(document)

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_find())
{'_id': ObjectId('...'), 'i': 2}
{'_id': ObjectId('...'), 'i': 1}
```

Подсчет документов

```python
>>> async def do_count():
...     n = await db.test_collection.count_documents({})
...     print('%s documents in collection' % n)
...     # matched to pattern
...     n = await db.test_collection.count_documents({'i': {'$gt': 1000}})
...     print('%s documents where i > 1000' % n)

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_count())
2000 documents in collection
999 documents where i > 1000
```

### [Updating documents](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#updating-documents)

`replace_one()` изменяет документ. Для этого требуются два параметра: запрос, указывающий, какой документ следует заменить, и замещающий документ. Запрос следует тому же синтаксису, что и для `find()` или `find_one()`. `replace_one()` заменяет все в старом документе, кроме его `_id`, новым документом.

Используйте `update_one()` с операторами-модификаторами MongoDB, чтобы обновить часть документа и оставить остальную часть нетронутой. `update_one()` афектит только первый найденный документ. Чтобы изменить несколько - надо использовать `update_many()`

```python
>>> async def do_replace():
...     coll = db.test_collection
...     old_document = await coll.find_one({'i': 50})
...     print('found document: %s' % pprint.pformat(old_document))
...     _id = old_document['_id']
...     result = await coll.replace_one({'_id': _id}, {'key': 'value'})
...     print('replaced %s document' % result.modified_count)
...     new_document = await coll.find_one({'_id': _id})
...     print('document is now %s' % pprint.pformat(new_document))

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_replace())
found document: {'_id': ObjectId('...'), 'i': 50}
replaced 1 document
document is now {'_id': ObjectId('...'), 'key': 'value'}

>>> async def do_update():
...     coll = db.test_collection
...     result = await coll.update_one({'i': 51}, {'$set': {'key': 'value'}})
...     print('updated %s document' % result.modified_count)
...     new_document = await coll.find_one({'i': 51})
...     print('document is now %s' % pprint.pformat(new_document))

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_update())
updated 1 document
document is now {'_id': ObjectId('...'), 'i': 51, 'key': 'value'}
```

### [Deleting documents](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#deleting-documents)

`delete_one()` и `delete_many()`. Оба метода используют тот же синтаксис, что и `find_one()`.

```python
>>> async def do_delete_one():
...     coll = db.test_collection
...     n = await coll.count_documents({})
...     print('%s documents before calling delete_one()' % n)
...     result = await db.test_collection.delete_one({'i': {'$gte': 1000}})
...     print('%s documents after' % (await coll.count_documents({})))

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_delete_one())
2000 documents before calling delete_one()
1999 documents after

>>> async def do_delete_many():
...     coll = db.test_collection
...     n = await coll.count_documents({})
...     print('%s documents before calling delete_many()' % n)
...     result = await db.test_collection.delete_many({'i': {'$gte': 1000}})
...     print('%s documents after' % (await coll.count_documents({})))

>>> loop = client.get_io_loop()
>>> loop.run_until_complete(do_delete_many())
1999 documents before calling delete_many()
1000 documents after
```

## [Примеры использования mongomotor](https://motor.readthedocs.io/en/stable/examples/index.html)

## API

- [Motor Tornado API](https://motor.readthedocs.io/en/stable/api-tornado/index.html)
  - `MotorClient` – Connection to MongoDB
  - `MotorClientSession` – Sequence of operations
  - `MotorDatabase`
  - `MotorCollection`
  - `MotorChangeStream`
  - `MotorClientEncryption`
  - `MotorCursor`
  - `MotorCommandCursor`
  - Motor GridFS Classes
  - `motor.web` - Integrate Motor with the [[tornado]] web framework
- [Motor asyncio API](https://motor.readthedocs.io/en/stable/api-asyncio/index.html)
  - [AsyncIOMotorClient](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client.html) – Connection to MongoDB
  - [AsyncIOMotorClientSession](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client_session.html) – Sequence of operations
  - [AsyncIOMotorDatabase](https://motor.readthedocs.io/en/stable/api-tornado/motor_database.html) some operations with given named db
  - [AsyncIOMotorCollection](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_one)
  - `AsyncIOMotorChangeStream`
  - `AsyncIOMotorClientEncryption`
  - [AsyncIOMotorCursor](https://motor.readthedocs.io/en/stable/api-asyncio/cursors.html#motor.motor_asyncio.AsyncIOMotorCursor.to_list) prowide query filtering
  - `AsyncIOMotorCommandCursor`
  - asyncio GridFS Classes
  - `motor.aiohttp` - Integrate Motor with the [[aiohttp]] web framework

Pymongo references:

- [mongo_client](https://pymongo.readthedocs.io/en/4.3.2/api/pymongo/mongo_client.html) – Tools for connecting to MongoDB
- [client_session](https://pymongo.readthedocs.io/en/4.3.2/api/pymongo/client_session.html) – Logical sessions for sequential operations
- [pynongo collection](https://pymongo.readthedocs.io/en/4.3.2/api/pymongo/collection.html)
- [operations](https://pymongo.readthedocs.io/en/4.3.2/api/pymongo/operations.html) – Operation class definitions, в т.ч. IndexModel
- [results](https://pymongo.readthedocs.io/en/4.3.2/api/pymongo/results.html) – Result class definitions
- [errorrs](https://pymongo.readthedocs.io/en/4.3.2/api/pymongo/errors.html#pymongo.errors.InvalidOperation) Exceptions raised by the pymongo package

## [[fastapi]] with motor and some questions

- [Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/). [Репо с примером](https://github.com/mongodb-developer/mongodb-with-fastapi)
- [Building a CRUD App with FastAPI and MongoDB](https://testdriven.io/blog/fastapi-mongo/)
- [How to parse ObjectId in a pydantic model?](https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model)
- [Why does PyMongo add an _id field to all of my documents?](https://pymongo.readthedocs.io/en/4.3.2/faq.html#writes-and-ids) in a [FAQ](https://pymongo.readthedocs.io/en/4.3.2/faq.html#id1)
- [Datetimes and Timezones in pymongo](https://pymongo.readthedocs.io/en/stable/examples/datetimes.html)

Смотри еще:

- [документация](https://motor.readthedocs.io/en/stable/)
- [на github](https://github.com/mongodb/motor)
- [on mongo world](https://www.mongodb.com/docs/drivers/motor/)
- [[mongodb]]
- [[mongoengine]]
- [[tornado]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[tornado]: tornado "Tornado - http web-фреймворк и асинхронная библиотека"
[asyncio]: asyncio "Asyncio"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[fastapi]: fastapi "Fastapi"
[mongodb]: mongodb "MongoDB"
[mongoengine]: mongoengine "Object Object-Document Mapper for MongoDB"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[tornado]: tornado "Tornado - http web-фреймворк и асинхронная библиотека"
[asyncio]: asyncio "Asyncio"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[tornado]: tornado "Tornado - http web-фреймворк и асинхронная библиотека"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[fastapi]: fastapi "Fastapi"
[mongodb]: mongodb "MongoDB"
[mongoengine]: mongoengine "Object Object-Document Mapper for MongoDB"
[tornado]: tornado "Tornado - http web-фреймворк и асинхронная библиотека"
[//end]: # "Autogenerated link references"