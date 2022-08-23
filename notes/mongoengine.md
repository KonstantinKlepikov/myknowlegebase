---
description: MongoEngine - ОРМ для mongodb
title: Object Object-Document Mapper for MongoDB
tags: bd
---
MongoEngine — это средство сопоставления объектов и документов, написанное на Python для работы с MongoDB.

`python -m pip install -U mongoengine`

## Minimal example

```python
from mongoengine import *
connect('mydb')

class BlogPost(Document):
    title = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True}

class TextPost(BlogPost):
    content = StringField(required=True)

class LinkPost(BlogPost):
    url = StringField(required=True)

# Create a text-based post
>>> post1 = TextPost(title='Using MongoEngine', content='See the tutorial')
>>> post1.tags = ['mongodb', 'mongoengine']
>>> post1.save()

# Create a link-based post
>>> post2 = LinkPost(title='MongoEngine Docs', url='hmarr.com/mongoengine')
>>> post2.tags = ['mongoengine', 'documentation']
>>> post2.save()

# Iterate over all posts using the BlogPost superclass
>>> for post in BlogPost.objects:
...     print('===', post.title, '===')
...     if isinstance(post, TextPost):
...         print(post.content)
...     elif isinstance(post, LinkPost):
...         print('Link:', post.url)
...

# Count all blog posts and its subtypes
>>> BlogPost.objects.count()
2
>>> TextPost.objects.count()
1
>>> LinkPost.objects.count()
1

# Count tagged posts
>>> BlogPost.objects(tags='mongoengine').count()
2
>>> BlogPost.objects(tags='mongodb').count()
1
```

## Connection to db

```python
from mongoengine import connact

connect(
    db='test',
    username='user',
    password='12345',
    host='mongodb://admin:qwerty@localhost/production'
)
```

- [Более подробно о подключении](http://docs.mongoengine.org/guide/connecting.html#guide-connecting)
- [АПИ connect](http://docs.mongoengine.org/apireference.html#connecting)

## Collections and [Fields](http://docs.mongoengine.org/guide/defining-documents.html#fields)

MongoDB не имеет схемы, что означает, что база данных не применяет никакую схему — мы можем добавлять и удалять поля, как захотим, и MongoDB не будет жаловаться. Это значительно упрощает жизнь во многих отношениях, особенно при изменении модели данных. Однако определение схем для наших документов может помочь сгладить ошибки, связанные с неправильными типами или отсутствующими полями, а также позволит нам определить служебные методы для наших документов так же, как это делают традиционные ORM.

`Document` - [базовый класс](http://docs.mongoengine.org/apireference.html#documents), используемый для определения структуры и свойств коллекций документов, хранящихся в MongoDB. Наследуйтесь от этого класса и добавляйте поля в качестве атрибутов класса, чтобы определить структуру документа. Затем могут быть созданы отдельные документы путем создания экземпляров Documentподкласса.

```python
class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
```

Это похоже на то, как структура таблицы определяется в обычном ORM. Ключевое отличие состоит в том, что эта схема никогда не будет передана в MongoDB — она будет применяться только на уровне приложения, что упрощает управление будущими изменениями. Кроме того, документы пользователя будут храниться в коллекции MongoDB, а не в таблице.

Мы будем хранить все документы в одной коллекции, а разные типы документов будут хранить разные типы данных. Нам не надо организовывать иерархию таблиц, как в реляционной БД.

```python
class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)

    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()
```

Мы можем думать о `Post` как о базовом классе, `TextPost` и `ImagePost` и `LinkPost` как о подклассах `Post`. На самом деле, MongoEngine поддерживает такое моделирование «из коробки» — все, что вам нужно сделать, это включить наследование, установив `allow_inheritance` значение `True` в `meta`. Мы храним ссылку на автора сообщений с помощью `ReferenceField`. Они аналогичны полям внешнего ключа в традиционных ORM и автоматически преобразуются в ссылки при сохранении и разыменовываются при загрузке.

MongoDB позволяет нам изначально хранить списки элементов, поэтому вместо таблицы ссылок мы можем просто хранить список тегов в каждом сообщении. Таким образом, ради эффективности и простоты мы будем хранить теги в виде строк непосредственно в сообщении, а не хранить ссылки на теги в отдельной коллекции.

```python
class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
```

Объект `ListField`, который используется для определения тегов сообщения, принимает объект поля в качестве первого аргумента — это означает, что вы можете иметь списки полей любого типа (включая списки).

Комментарий обычно связан с одним постом. В реляционной базе данных, чтобы отобразить сообщение с его комментариями, нам пришлось бы получить сообщение из базы данных, а затем снова запросить базу данных для комментариев, связанных с сообщением. Это работает, но нет реальной причины хранить комментарии отдельно от связанных с ними сообщений, кроме как для обхода реляционной модели. Используя MongoDB, мы можем хранить комментарии в виде списка встроенных документов непосредственно в документе. Используя MongoEngine, мы можем определить структуру встроенных документов вместе с служебными методами точно так же, как мы это делаем с обычными документами:

```python
class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
```

Кроме того, в поле author мы определили `reverse_delete_rule` для удаления всех `Post` в случае удаления связанного с ними `User`. MapFields и DictFields в настоящее время не поддерживают автоматическую обработку удаленных ссылок.

Подробнее об [embeded document](http://docs.mongoengine.org/apireference.html#mongoengine.EmbeddedDocument). Другие встроеныне типы документов:

- [dynamic document](http://docs.mongoengine.org/apireference.html#mongoengine.DynamicDocument)
- [dynamic embeded document](http://docs.mongoengine.org/apireference.html#mongoengine.DynamicEmbeddedDocument)
- [MapReduceDocument](http://docs.mongoengine.org/apireference.html#mongoengine.document.MapReduceDocument)
- [ValidationError](http://docs.mongoengine.org/apireference.html#mongoengine.ValidationError)
- [FieldDoesNotExist](http://docs.mongoengine.org/apireference.html#mongoengine.FieldDoesNotExist)

Класс `DynamicDocument`, позволяющий использовать гибкие, расширяемые и неконтролируемые схемы. Действует так же, как обычный документ, но имеет расширенные свойства стиля. Любые данные, переданные или заданные `DynamicDocument` для поля, которое не является полем, автоматически преобразуются в поле, DynamicFieldи данные могут быть отнесены к этому полю.

```python
from mongoengine import *

class Page(DynamicDocument):
    title = StringField(max_length=200, required=True)

# Create a new page and add tags
>>> page = Page(title='Using MongoEngine')
>>> page.tags = ['mongodb', 'mongoengine']
>>> page.save()

>>> Page.objects(tags='mongoengine').count()
>>> 1
```

### Fields

По умолчанию поля необязательны. Чтобы сделать поле обязательным, задайте для аргумента `required` значение `True`. Поля также могут иметь ограничения (например, `max_length` в приведенном выше примере). Поля также могут принимать значения по умолчанию, которые будут использоваться, если значение не указано. Значения по умолчанию могут быть опционально вызываемыми, которые будут вызываться для извлечения значения. Доступны следующие типы полей:

- BinaryField
- BooleanField
- ComplexDateTimeField
- DateTimeField
- DecimalField
- DictField
- DynamicField
- EmailField
- EmbeddedDocumentField
- EmbeddedDocumentListField
- EnumField
- FileField
- FloatField
- GenericEmbeddedDocumentField
- GenericReferenceField
- GenericLazyReferenceField
- GeoPointField
- ImageField
- IntField
- ListField
- LongField
- MapField
- ObjectIdField
- ReferenceField
- LazyReferenceField
- SequenceField
- SortedListField
- StringField
- URLField
- UUIDField
- PointField
- LineStringField
- PolygonField
- MultiPointField
- MultiLineStringField
- MultiPolygonField

Подробнее в [описании АПИ](http://docs.mongoengine.org/apireference.html#fields).

Дополнительно у полей доступны [аргументы](http://docs.mongoengine.org/guide/defining-documents.html#field-arguments)

- Если установлено `db_fiekd`, операции в MongoDB будут выполняться с этим значением вместо атрибута класса.

    ```python
    from mongoengine import *

    class Page(Document):
        page_number = IntField(db_field="pageNumber")

    # Create a Page and save it
    Page(page_number=1).save()

    # How 'pageNumber' is stored in MongoDB
    Page.objects.as_pymongo() # [{'_id': ObjectId('629dfc45ee4cc407b1586b1f'), 'pageNumber': 1}]

    # Retrieve the object
    page: Page = Page.objects.first()

    print(page.page_number)  # prints 1

    print(page.pageNumber) # raises AttributeError
    ```

- `required`
- `default`
- `unique` при значении True никакие документы в коллекции не будут иметь одинаковое значение для этого поля.
- `unique with` имя поля (или список имен полей), которое взято вместе с этим полем не будет иметь в коллекции двух документов с одинаковым значением.

    ```python
    class User(Document):
        username = StringField(unique=True)
        first_name = StringField()
        last_name = StringField(unique_with='first_name')
    ```

- `primary_key` при значении True используйте это поле в качестве первичного ключа для коллекции. DictField и EmbeddedDocuments поддерживают первичный ключ для документа.
- `choices`

    ```python
    SIZE = (('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
            ('XXL', 'Extra Extra Large'))


    class Shirt(Document):
        size = StringField(max_length=3, choices=SIZE)

    # or
    SIZE = ('S', 'M', 'L', 'XL', 'XXL')

    class Shirt(Document):
        size = StringField(max_length=3, choices=SIZE)
    ```

- `validation` вызываемый объект для проверки значения поля. Вызываемый объект принимает значение в качестве параметра и должен вызвать `ValidationError`, если проверка не пройдена.

    ```python
    def _not_empty(val):
    if not val:
        raise ValidationError('value can not be empty')

    class Person(Document):
        name = StringField(validation=_not_empty)
    ```

- `**kwargs`

Кроме того доступны последовательности и встроеныне документы:

- `ListField`

    ```python
    class Page(Document):
        tags = ListField(StringField(max_length=50))
    ```

- `EmbeddedDocument`

    ```python
    class Comment(EmbeddedDocument):
        content = StringField()

    class Page(Document):
        comments = ListField(EmbeddedDocumentField(Comment))

    comment1 = Comment(content='Good work!')
    comment2 = Comment(content='Nice article!')
    page = Page(comments=[comment1, comment2])
    ```

- `DictField` Часто вместо словаря можно использовать встроенный документ — обычно рекомендуются встроенные документы, поскольку словари не поддерживают проверку или настраиваемые типы полей. Однако иногда вы не будете знать структуру того, что хотите сохранить; в этой ситуации подходит `DictField`

    ```python
    class SurveyResponse(Document):
        date = DateTimeField()
        user = ReferenceField(User)
        answers = DictField()

    survey_response = SurveyResponse(date=datetime.utcnow(), user=request.user)
    response_form = ResponseForm(request.POST)
    survey_response.answers = response_form.cleaned_data()
    survey_response.save()
    ```

- `ReferenceField` Ссылки указывают на другие документы в базе данных. Чтобы добавить ReferenceField, который ссылается на определяемый документ, используйте строку «self» вместо класса документа в качестве аргумента для конструктора ReferenceField. Чтобы сослаться на документ, который еще не определен, используйте имя неопределенного документа в качестве аргумента конструктора

    ```python
    class User(Document):
        name = StringField()

    class Page(Document):
        content = StringField()
        author = ReferenceField(User)

    john = User(name="John Smith")
    john.save()

    post = Page(content="Test Page")
    post.author = john
    post.save()

    # or
    class Employee(Document):
        name = StringField()
        boss = ReferenceField('self')
        profile_page = ReferenceField('ProfilePage')

    class ProfilePage(Document):
        content = StringField()
    ```

### Many to Many with ListFields.

Если вы реализуете отношения «многие ко многим» через список ссылок, то ссылки хранятся как DBRefs, и для запроса вам необходимо передать экземпляр объекта в запрос.

```python
class User(Document):
    name = StringField()

class Page(Document):
    content = StringField()
    authors = ListField(ReferenceField(User))

bob = User(name="Bob Jones").save()
john = User(name="John Smith").save()

Page(content="Test Page", authors=[bob, john]).save()
Page(content="Another Page", authors=[john]).save()

# Find all pages Bob authored
Page.objects(authors__in=[bob])

# Find all pages that both Bob and John have authored
Page.objects(authors__all=[bob, john])

# Remove Bob from the authors for a page.
Page.objects(id='...').update_one(pull__authors=bob)

# Add John to the authors for a page.
Page.objects(id='...').update_one(push__authors=john)
```

По умолчанию MongoDB не проверяет целостность ваших данных, поэтому удаление документов, ссылки на которые есть в других документах, приведет к проблемам согласованности. ReferenceField Mongoengine добавляет некоторые функции для защиты от таких проблем с целостностью базы данных, предоставляя каждой ссылке спецификацию правила удаления. Подробнее [тут](http://docs.mongoengine.org/guide/defining-documents.html#dealing-with-deletion-of-referred-documents)

### Another solution for reference

Другой вариант добавления рефернсов - это [женерики](http://docs.mongoengine.org/guide/defining-documents.html#generic-reference-fields)

```python
class Link(Document):
    url = StringField()

class Post(Document):
    title = StringField()

class Bookmark(Document):
    bookmark_object = GenericReferenceField()

link = Link(url='http://hmarr.com/mongoengine/')
link.save()

post = Post(title='Using MongoEngine')
post.save()

Bookmark(bookmark_object=link).save()
Bookmark(bookmark_object=post).save()
```

### Collection names and capped collection

Классы документов, которые наследуются непосредственно от `Document`, будут иметь собственную коллекцию в базе данных. Имя коллекции по умолчанию является именем класса, преобразованного в снейк кейс. Если вам нужно изменить имя коллекции (например, чтобы использовать MongoEngine с существующей базой данных), создайте атрибут словаря класса с именем meta в своем документе и установите для коллекции имя коллекции, которое вы хотите, чтобы использовал ваш класс документа.

```python
class Page(Document):
    title = StringField(max_length=200, required=True)
    meta = {'collection': 'cmsPage'}
```

Документ может использовать ограниченную коллекцию, указав `max_documents` и `max_size` в метасловаре. `max_documents` — это максимальное количество документов, которое разрешено хранить в коллекции, а `max_size` — это максимальный размер коллекции в байтах

```python
class Log(Document):
    ip_address = StringField()
    meta = {'max_documents': 1000, 'max_size': 2000000}
```

### Indexes

Вы можете указать индексы для коллекций, чтобы ускорить запросы. Это делается путем создания списка спецификаций индексов, называемых indexes, в метасловаре, где спецификацией индекса может быть либо одно имя поля, кортеж, содержащий несколько имен полей, либо словарь, содержащий полное определение индекса.

Направление может быть указано в полях путем добавления к имени поля префикса (для возрастания) или знака - (для убывания). Обратите внимание, что направление имеет значение только для составных индексов. Текстовые индексы могут быть указаны путем добавления к имени поля префикса $. Хешированные индексы могут быть указаны путем добавления префикса # к имени поля:

```python
class Page(Document):
    category = IntField()
    title = StringField()
    rating = StringField()
    created = DateTimeField()
    meta = {
        'indexes': [
            'title',   # single-field index
            '$title',  # text index
            '#title',  # hashed index
            ('title', '-rating'),  # compound index
            ('category', '_cls'),  # compound index
            {
                'fields': ['created'],
                'expireAfterSeconds': 3600  # ttl index
            }
        ]
    }
```

Дополнительные опции, глобальные и кеоспасиал индексы [смотри тут](http://docs.mongoengine.org/guide/defining-documents.html#indexes)

TTL index - специальный тип индекса, который позволяет автоматически удалять данные из коллекции по истечении заданного периода.

```python
class Session(Document):
    created = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 3600}
        ]
    }
```

Индексы TTL происходят на сервере MongoDB, а не в коде приложения, поэтому при удалении документа не будет генерироваться никаких сигналов. Если вам нужно, чтобы сигналы запускались при удалении, вы должны обрабатывать удаление документов в коде своего приложения.

### Ordering

Порядок по умолчанию может быть указан для вашего `QuerySet` с помощью атрибута `ordering` в `meta`. Упорядочивание будет применено при создании `QuerySet` и может быть переопределено последующими вызовами `order_by()`.

```python
from datetime import datetime

class BlogPost(Document):
    title = StringField()
    published_date = DateTimeField()

    meta = {
        'ordering': ['-published_date']
    }

blog_post_1 = BlogPost(title="Blog Post #1")
blog_post_1.published_date = datetime(2010, 1, 5, 0, 0 ,0)

blog_post_2 = BlogPost(title="Blog Post #2")
blog_post_2.published_date = datetime(2010, 1, 6, 0, 0 ,0)

blog_post_3 = BlogPost(title="Blog Post #3")
blog_post_3.published_date = datetime(2010, 1, 7, 0, 0 ,0)

blog_post_1.save()
blog_post_2.save()
blog_post_3.save()

# get the "first" BlogPost using default ordering
# from BlogPost.meta.ordering
latest_post = BlogPost.objects.first()
assert latest_post.title == "Blog Post #3"

# override default ordering, order BlogPosts by "published_date"
first_post = BlogPost.objects.order_by("+published_date").first()
assert first_post.title == "Blog Post #1"
```

## [Добавление данных](http://docs.mongoengine.org/guide/document-instances.html)

```python
>>> page = Page(title="Test Page")
>>> page.title
'Test Page'

>>> page.title = "Example Page"
>>> page.title
'Example Page'

>>> page.save()  # Performs an insert
>>> page.title = 'Example Page'
>>> page.save()  # Performs an atomic set on the title field.
```

Чтобы удалить документ, вызовите метод `delete()`. Обратите внимание, что это будет работать только в том случае, если документ существует в базе данных и имеет действительный идентификатор. Каждый документ в базе данных имеет уникальный идентификатор. Доступ к этому можно получить через атрибут id объектов Document. Обычно идентификатор автоматически генерируется сервером базы данных при сохранении объекта, а это означает, что вы можете получить доступ к полю идентификатора только после сохранения документа

```python
>>> page = Page(title="Test Page")
>>> page.id
>>> page.save()
>>> page.id
ObjectId('123456789abcdef000000000')
```

В качестве альтернативы вы можете определить одно из своих собственных полей в качестве «первичного ключа» документа, указав `primary_key=True` в качестве аргумента ключевого слова конструктору поля.

```python
>>> class User(Document):
...     email = StringField(primary_key=True)
...     name = StringField()

>>> bob = User(email='bob@example.com', name='Bob')
>>> bob.save()
>>> bob.id == bob.email == 'bob@example.com'
True
```

Вы также можете получить доступ к «первичному ключу» документа, используя поле `pk`, это псевдоним для `id`

```python
>>> page = Page(title="Another Test Page")
>>> page.save()
>>> page.id == page.pk
True
```

## [Querying the database](http://docs.mongoengine.org/guide/querying.html)

```python
for post in Post.objects:
    print(post.title)

# or
for post in TextPost.objects:
    print(post.content)
```

Использование атрибута `objects` для `TextPost` возвращает только документы, созданные с использованием `TextPost`. На самом деле здесь действует более общее правило: `objects` любого подкласса `Document` ищет только те документы, которые были созданы с использованием этого подкласса или одного из его подклассов.

Атрибут `objects`  `Document`а на самом деле является `QuerySet` объектом. Это лениво запрашивает базу данных только тогда, когда вам нужны данные. Он также может быть отфильтрован, чтобы сузить ваш запрос

```python
for post in Post.objects(tags='mongodb'):
    print(post.title)
```

### Filtering

Ключи в аргументах ключевого слова соответствуют полям запрашиваемого документа.

```python
# This will return a QuerySet that will only iterate over users whose
# 'country' field is set to 'uk'
uk_users = User.objects(country='uk')
```

На поля встроенных документов также можно ссылаться с помощью синтаксиса поиска полей, используя двойное подчеркивание вместо точки в синтаксисе доступа к атрибутам объекта

```python
# This will return a QuerySet that will only iterate over pages that have
# been written by a user whose 'country' field is set to 'uk'
uk_pages = Page.objects(author__country='uk')
```

### [Query operators](http://docs.mongoengine.org/guide/querying.html#query-operators)

Доступно все, что используется в стандарте реляционных БД, а так-же строковые запросы, гео-запросы, списочные запросы, а так-же raw-запросы.

Пирмер "нативного" raw-запроса.

```python
Page.objects(__raw__={'tags': 'coding'})
```

### Sorting/Ordering

```python
# Order by ascending date
blogs = BlogPost.objects().order_by('date')    # equivalent to .order_by('+date')

# Order by ascending date first, then descending title
blogs = BlogPost.objects().order_by('+date', '-title')
```

### Limiting and skipping

Можно через методы `limit()` и `skip()`, а можно через слайс.

```python
# Only the first 5 people
users = User.objects[:5]

# All except for the first 5 people
users = User.objects[5:]

# 5 users, starting from the 11th user found
users = User.objects[10:15]
```

`get()` позволяет получить уникальный результат

### [Default document query](http://docs.mongoengine.org/guide/querying.html#default-document-queries)

По умолчанию атрибут объектов в документе возвращает QuerySet, который не фильтрует коллекцию — он возвращает все объекты. Это можно изменить, определив в документе метод, который изменяет набор запросов. Метод должен принимать два аргумента — doc_cls и queryset. Первый аргумент — это класс Document, для которого определен метод (в этом смысле метод больше похож на classmethod(), чем на обычный метод), а второй аргумент — это исходный набор запросов. Метод должен быть дополнен queryset_manager(), чтобы его можно было распознать.

### [Custom QuerySets](http://docs.mongoengine.org/guide/querying.html#custom-querysets)

### [Aggregation](http://docs.mongoengine.org/guide/querying.html#aggregation)

### [Эффективность запросов и производительность](http://docs.mongoengine.org/guide/querying.html#query-efficiency-and-performance)

### [Расширенные запросы](http://docs.mongoengine.org/guide/querying.html#advanced-queries)

Иногда вызов объекта `QuerySet` с аргументами ключевого слова не может полностью выразить запрос, который вы хотите использовать — например, если вам нужно объединить ряд ограничений. Это стало возможным в MongoEngine благодаря классу `Q`. Объект Q представляет собой часть запроса и может быть инициализирован с использованием того же синтаксиса ключевого слова-аргумента, который вы используете для запроса документов.

```python
from mongoengine.queryset.visitor import Q

# Get published posts
Post.objects(Q(published=True) | Q(publish_date__lte=datetime.now()))

# Get top posts
Post.objects((Q(featured=True) & Q(hits__gte=1000)) | Q(hits__gte=5000))
```

### [Atomic updates](http://docs.mongoengine.org/guide/querying.html#atomic-updates)

Документы могут быть обновлены атомарно с помощью методов `update_one()`, `update()` и `modify()` в `QuerySet` или с помощью методов `modify()` и `save()` (с аргументом `save_condition`) в документе. Есть несколько различных «модификаторов», которые вы можете использовать с этими методами:

- `set` – set a particular value
- `set_on_insert` – set only if this is new document
- `unset` – delete a particular value
- `max` – update only if value is bigger
- `min` – update only if value is smaller
- `inc` – increment a value by a given amount
- `dec` – decrement a value by a given amount
- `push` – append a value to a list
- `push_all` – append several values to a list
- `pop` – remove the first or last element of a list depending on the value
- `pull` – remove a value from a list
- `pull_all` – remove several values from a list
- `add_to_set` – add value to a list only if its not in the list already
- `rename` – rename the key name

```python
>>> post = BlogPost(title='Test', page_views=0, tags=['database'])
>>> post.save()
>>> BlogPost.objects(id=post.id).update_one(inc__page_views=1)
>>> post.reload()  # the document has been changed, so we need to reload it
>>> post.page_views
1
BlogPost.objects(id=post.id).update_one(set__title='Example Post')
>>> post.reload()
>>> post.title
'Example Post'
>>> BlogPost.objects(id=post.id).update_one(push__tags='nosql')
>>> post.reload()
>>> post.tags
['database', 'nosql']
```

## [Document Validation](http://docs.mongoengine.org/guide/validation.html)

Build-in

```python
from mongoengine import Document, EmailField

class User(Document):
    email = EmailField()
    age = IntField(min_value=0, max_value=99)

user = User(email='invalid@', age=24)
user.validate()     # raises ValidationError (Invalid email address: ['email'])
user.save()         # raises ValidationError (Invalid email address: ['email'])

user2 = User(email='john.doe@garbage.com', age=1000)
user2.save()        # raises ValidationError (Integer value is too large: ['age'])
```

Custom

```python
def not_john_doe(name):
    if name == 'John Doe':
        raise ValidationError("John Doe is not a valid name")

class Person(Document):
    full_name = StringField(validation=not_john_doe)

Person(full_name='Billy Doe').save()
Person(full_name='John Doe').save()  # raises ValidationError (John Doe is not a valid name)
```

## G[ridFS](http://docs.mongoengine.org/guide/gridfs.html)

Поддержка GridFS осуществляется в виде объекта поля `FileField`. Это поле действует как файлоподобный объект и предоставляет несколько различных способов вставки и извлечения данных. Произвольные метаданные, такие как тип содержимого, также могут храниться вместе с файлами. Объект, возвращаемый при доступе к `FileField`, является прокси для GridFS Pymongo.

## [Signals](http://docs.mongoengine.org/guide/signals.html#signals)

## [Text Search](http://docs.mongoengine.org/guide/text-indexes.html)

## [Documents migration](http://docs.mongoengine.org/guide/migration.html)

## [Logging/Monitoring](http://docs.mongoengine.org/guide/logging-monitoring.html)

```python
import logging
from pymongo import monitoring
from mongoengine import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        log.debug("Command {0.command_name} with request id "
                 "{0.request_id} started on server "
                 "{0.connection_id}".format(event))

    def succeeded(self, event):
        log.debug("Command {0.command_name} with request id "
                 "{0.request_id} on server {0.connection_id} "
                 "succeeded in {0.duration_micros} "
                 "microseconds".format(event))

    def failed(self, event):
        log.debug("Command {0.command_name} with request id "
                 "{0.request_id} on server {0.connection_id} "
                 "failed in {0.duration_micros} "
                 "microseconds".format(event))

monitoring.register(CommandLogger())


class Jedi(Document):
    name = StringField()


connect()


log.info('GO!')

log.info('Saving an item through MongoEngine...')
Jedi(name='Obi-Wan Kenobii').save()

log.info('Querying through MongoEngine...')
obiwan = Jedi.objects.first()

log.info('Updating through MongoEngine...')
obiwan.name = 'Obi-Wan Kenobi'
obiwan.save()
```

в результате:

```sh
INFO:root:GO!
INFO:root:Saving an item through MongoEngine...
DEBUG:root:Command insert with request id 1681692777 started on server ('localhost', 27017)
DEBUG:root:Command insert with request id 1681692777 on server ('localhost', 27017) succeeded in 562 microseconds
INFO:root:Querying through MongoEngine...
DEBUG:root:Command find with request id 1714636915 started on server ('localhost', 27017)
DEBUG:root:Command find with request id 1714636915 on server ('localhost', 27017) succeeded in 341 microseconds
INFO:root:Updating through MongoEngine...
DEBUG:root:Command update with request id 1957747793 started on server ('localhost', 27017)
DEBUG:root:Command update with request id 1957747793 on server ('localhost', 27017) succeeded in 455 microseconds
```

## [Mongomock for testing](http://docs.mongoengine.org/guide/mongomock.html)

Смотри еще:

- [документация](https://github.com/MongoEngine/mongoengine)
- [User guide](http://docs.mongoengine.org/guide/index.html)
- [api reference](http://docs.mongoengine.org/apireference.html#)
- [гитхаб](https://github.com/MongoEngine/mongoengine)
- [[mongodb]]
- [mongomock](https://github.com/mongomock/mongomock) Small library for mocking pymongo collection objects for testing purposes
- odmantic (async orm)
  - [docs](https://art049.github.io/odmantic/)
  - [git](https://github.com/art049/odmantic)
- μMongo: sync/async ODM
  - [docs](https://umongo.readthedocs.io/en/latest/)
  - [github](https://github.com/Scille/umongo)
- Ming (orm)
  - [docs](https://ming.readthedocs.io/en/latest/)
- [micromongo](https://pythonhosted.org/micromongo/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[mongodb]: mongodb "MongoDB"
[//end]: # "Autogenerated link references"