---
description: Объектные паттерны в python
---
# Python patterns

Примеры кода и тесты, демонстрирующие работу паттернов, можно найти [в этом репозитории](https://github.com/faif/python-patterns)

## Порождающие паттерны

### Builder

Необходим для разделения спецификации объекта и его представления. В python реализован [[abc]]

[Пример без abc](https://github.com/faif/python-patterns/blob/master/patterns/creational/builder.py)

```python
# Abstract Building
class Building:
    def __init__(self):
        self.build_floor()
        self.build_size()

    def build_floor(self):
        raise NotImplementedError

    def build_size(self):
        raise NotImplementedError

    def __repr__(self):
        return "Floor: {0.floor} | Size: {0.size}".format(self)


# Concrete Buildings
class House(Building):
    def build_floor(self):
        self.floor = "One"

    def build_size(self):
        self.size = "Big"


class Flat(Building):
    def build_floor(self):
        self.floor = "More than One"

    def build_size(self):
        self.size = "Small"


>>> house = House()
>>> house
Floor: One | Size: Big
>>> flat = Flat()
>>> flat
Floor: More than One | Size: Small
```

### Factory

Объект для создания других объектов

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/creational/factory.py)

```python
class GreekLocalizer:
    """A simple localizer a la gettext"""

    def __init__(self) -> None:
        self.translations = {"dog": "σκύλος", "cat": "γάτα"}

    def localize(self, msg: str) -> str:
        """We'll punt if we don't have a translation"""
        return self.translations.get(msg, msg)


class EnglishLocalizer:
    """Simply echoes the message"""

    def localize(self, msg: str) -> str:
        return msg


def get_localizer(language: str = "English") -> object:

    """Factory"""
    localizers = {
        "English": EnglishLocalizer,
        "Greek": GreekLocalizer,
    }

    return localizers[language]()


# Create our localizers
>>> e, g = get_localizer(language="English"), get_localizer(language="Greek")
# Localize some text
>>> for msg in "dog parrot cat bear".split():
...     print(e.localize(msg), g.localize(msg))
dog σκύλος
parrot parrot
cat γάτα
bear bear
```

### Abstract Factory

Реализует интерфейцс создлания связанного/зависимого объекта без непосредственного определения его класса. Идея - абстрагированное создание объектов в зависимсоти от бизнес-логики с определенным поведением. В python это можно сделать на [[abc]]

[Пример без abc](https://github.com/faif/python-patterns/blob/master/patterns/creational/abstract_factory.py)

### Borg (Monostate pattern)

Синеглтон с общим состоянием инстансев. Порождает несколько экземпляров, разделяющих общее состояние.

В python атрибут инстанса сохраняется в `__dict__` и каждый инстанс имеет свой собственный `__dict__`. Мы можем внести в эти словари изменеения или полностью переопределить их, чтобы поведение экзепляров отвечало нашим задачам.

Используется, к примеру, для управления коннектом к БД.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/creational/borg.py)

```python
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class YourBorg(Borg):
    def __init__(self, state=None):
        super().__init__()
        if state:
            self.state = state
        else:
            # initiate the first instance with default state
            if not hasattr(self, "state"):
                self.state = "Init"

    def __str__(self):
        return self.state


>>> rm1 = YourBorg()
>>> rm2 = YourBorg()
>>> rm1.state = 'Idle'
>>> rm2.state = 'Running'
>>> print('rm1: {0}'.format(rm1))
rm1: Running
>>> print('rm2: {0}'.format(rm2))
rm2: Running
# When the `state` attribute is modified from instance `rm2`,
# the value of `state` in instance `rm1` also changes
>>> rm2.state = 'Zombie'
>>> print('rm1: {0}'.format(rm1))
rm1: Zombie
>>> print('rm2: {0}'.format(rm2))
rm2: Zombie
# Even though `rm1` and `rm2` share attributes, the instances are not the same
>>> rm1 is rm2
False
# New instances also get the same shared state
>>> rm3 = YourBorg()
>>> print('rm1: {0}'.format(rm1))
rm1: Zombie
>>> print('rm2: {0}'.format(rm2))
rm2: Zombie
>>> print('rm3: {0}'.format(rm3))
rm3: Zombie
# A new instance can explicitly change the state during creation
>>> rm4 = YourBorg('Running')
>>> print('rm4: {0}'.format(rm4))
rm4: Running
# Existing instances reflect that change as well
>>> print('rm3: {0}'.format(rm3))
rm3: Running
```

### Lazy evaluation (ленивые вычисления) property pattern

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/creational/lazy_evaluation.py)

### Pool

Создание и поддержание группы экземпларов одного типа. Используется когджа создавать объект затратно, но надо создавать часто. При этом мы понимаем, что одновременно задейстивыовано лишь несколько объектов из пула.

Pool может кешировать экземпляры и отдавать их по требованию, избегая дорогостоящего создания. Если в пуле пусто - создается новый объект.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/creational/pool.py)

```python
class ObjectPool:
    def __init__(self, queue, auto_get=False):
        self._queue = queue
        self.item = self._queue.get() if auto_get else None

    def __enter__(self):
        if self.item is None:
            self.item = self._queue.get()
        return self.item

    def __exit__(self, Type, value, traceback):
        if self.item is not None:
            self._queue.put(self.item)
            self.item = None

    def __del__(self):
        if self.item is not None:
            self._queue.put(self.item)
            self.item = None


>>> import queue
>>> def test_object(queue):
...    pool = ObjectPool(queue, True)
...    print('Inside func: {}'.format(pool.item))
>>> sample_queue = queue.Queue()
>>> sample_queue.put('yam')
>>> with ObjectPool(sample_queue) as obj:
...    print('Inside with: {}'.format(obj))
Inside with: yam
>>> print('Outside with: {}'.format(sample_queue.get()))
Outside with: yam
>>> sample_queue.put('sam')
>>> test_object(sample_queue)
Inside func: sam
>>> print('Outside func: {}'.format(sample_queue.get()))
Outside func: sam
if not sample_queue.empty():
    print(sample_queue.get())
```

### Prototype

Используется фабрика, которая возвращает клон прототипа, если создавать экземпляры дорого.

Сокращает количество сабклассов - вместо этого создаются объекты за счет копирования прототипа во время выполнения.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/creational/prototype.py)

```python
from typing import Any


class Prototype:
    def __init__(self, value: str = "default", **attrs: Any) -> None:
        self.value = value
        self.__dict__.update(attrs)

    def clone(self, **attrs: Any) -> Prototype:
        """Clone a prototype and update inner attributes dictionary"""
        # Python in Practice, Mark Summerfield
        # copy.deepcopy can be used instead of next line.
        obj = self.__class__(**self.__dict__)
        obj.__dict__.update(attrs)
        return obj


class PrototypeDispatcher:
    def __init__(self):
        self._objects = {}

    def get_objects(self) -> dict[str, Prototype]:
        """Get all objects"""
        return self._objects

    def register_object(self, name: str, obj: Prototype) -> None:
        """Register an object"""
        self._objects[name] = obj

    def unregister_object(self, name: str) -> None:
        """Unregister an object"""
        del self._objects[name]


>>> dispatcher = PrototypeDispatcher()
>>> prototype = Prototype()
>>> d = prototype.clone()
>>> a = prototype.clone(value='a-value', category='a')
>>> b = a.clone(value='b-value', is_checked=True)
>>> dispatcher.register_object('objecta', a)
>>> dispatcher.register_object('objectb', b)
>>> dispatcher.register_object('default', d)
>>> [{n: p.value} for n, p in dispatcher.get_objects().items()]
[{'objecta': 'a-value'}, {'objectb': 'b-value'}, {'default': 'default'}]
>>> print(b.category, b.is_checked)
a True
```

## Структурные паттерны

### 3-iter

Разделяет представлоение, процессинг приложения и менеджмент данных

### Adapter

Адаптирует один интерфейс к другому. Полезен для интеграции классов, которые несовместимы напрямую из-за разных интерфейсов.

### Bridge

Отделяет абстракцию от реализации

### Composite

Позволяет клиентам одинаково воспринимать отдлельные объекты и их композиции. Шаблон обрабатывает группу объектов как один экземпляр объекта того же типа.

### Decorator

### Facade

Один класс используется как API для группы других классов. Предоставляет обобщенный и унифицированный интерфейс для более сложных систем.

### Fly weight (приспособленецй)

Позволяет прозрачно повторно использовать уже созданные экзепляры объектов с похожими/идентичными состояниями

Направлен на минимизацию количества объектов, которые нужны приложению во время выполнения. Шаблон производит объекты, которые используется одновременно несколькими контейнерами.

### Mvc (model->view->controller)

### Proxy

Объект передает операции кому-то еще. Прокси используется там, где надо добавить в класс функциональность, не меняя ее (например добавление журналирования, кешировавния, авторизацию и т.д.)

Субъекты и прокси в паттерне требуют реализации одинаковых интерфейсов.

## Поведенческие паттерны

### Chaining method

Продолжимть выполнение операций обратным вызовом следующего метода

### Chain of responsibility

Цепочка последовательнывх обработчиков. (if... elif...elif...else)

Блоки могут быть переставлены реконфигурированы во время выполнения. Отделяет отправителя запроса от принимающего. Принимающий знает только последнего отправителя.

### Catalog

Обобщенный метод вызывает специальные методы, основываясь на параметре состояния.

### Command

Создаем бандл из аргументов и методов для вызова позже.

Отделяет объект, выдающий задачу от того, кто знает как ее сделать. Пример - пункты в меню, вызывающие один и тот же метод при нажатии.

### Iterator

Пройти через контейнер и получить доступ к его элементам

### Mediator

Соединяет другие объектыф в одном объекте и действует как прокси. Сокращает чяисло связей в коде.

### Memnento

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[abc]: abc "Abc"
[abc]: abc "Abc"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"