---
description: Объектные паттерны в python
tags: python-standart-library python
title: Python patterns programming
---
Примеры кода и тесты, демонстрирующие работу паттернов, можно найти [в этом репозитории](https://github.com/faif/python-patterns)

В ряде примеров можно встретить конструкцию `from __future__ import annotations`. Для чего это используется смотри тут: [[from-future-import-annotations]]. Больше про аннотации читай в [[type-annotation]] и [[typing]]

## Delegation

Здесь делегейтору передается делегируемый экземпляр клесса, обрабатывающий запрос. Внутри делегатора мы получаем атрибуты делегируемого класса и реализуем новое поведение для них.

```python
from __future__ import annotations

from typing import Any, Callable


class Delegator:

    def __init__(self, delegate: Delegate):
        self.delegate = delegate

    def __getattr__(self, name: str) -> Any | Callable:
        attr = getattr(self.delegate, name)

        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper


class Delegate:
    def __init__(self):
        self.p1 = 123

    def do_something(self, something: str) -> str:
        return f"Doing {something}"


>>> delegator = Delegator(Delegate())
>>> delegator.p1
123
>>> delegator.p2
Traceback (most recent call last):
...
AttributeError: 'Delegate' object has no attribute 'p2'
>>> delegator.do_something("nothing")
'Doing nothing'
>>> delegator.do_anything()
Traceback (most recent call last):
...
AttributeError: 'Delegate' object has no attribute 'do_anything'
```

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

    def __init__(self) -> None:
        self.translations = {"dog": "σκύλος", "cat": "γάτα"}

    def localize(self, msg: str) -> str:
        """We'll punt if we don't have a translation"""
        return self.translations.get(msg, msg)


class EnglishLocalizer:

    def localize(self, msg: str) -> str:
        return msg


def get_localizer(language: str = "English") -> object:

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
from __future__ import annotations
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

[Простенький пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/3-tier.py) (на самом деле разделение на слои в приложениях реализуются как минимум в модулях)

```python
from typing import Dict, KeysView, Optional, Union


class Data:

    products = {
        "milk": {"price": 1.50, "quantity": 10},
        "eggs": {"price": 0.20, "quantity": 100},
        "cheese": {"price": 2.00, "quantity": 10},
    }

    def __get__(self, obj, klas):

        print("(Fetching from Data Store)")
        return {"products": self.products}


class BusinessLogic:

    data = Data()

    def product_list(self) -> KeysView[str]:
        return self.data["products"].keys()

    def product_information(
        self, product: str
    ) -> Optional[Dict[str, Union[int, float]]]:
        return self.data["products"].get(product, None)


class Ui:

    def __init__(self) -> None:
        self.business_logic = BusinessLogic()

    def get_product_list(self) -> None:
        print("PRODUCT LIST:")
        for product in self.business_logic.product_list():
            print(product)
        print("")

    def get_product_information(self, product: str) -> None:
        product_info = self.business_logic.product_information(product)
        if product_info:
            print("PRODUCT INFORMATION:")
            print(
                f"Name: {product.title()}, "
                + f"Price: {product_info.get('price', 0):.2f}, "
                + f"Quantity: {product_info.get('quantity', 0):}"
            )
        else:
            print(f"That product '{product}' does not exist in the records")

>>> ui = Ui()
>>> ui.get_product_list()
PRODUCT LIST:
(Fetching from Data Store)
milk
eggs
cheese
<BLANKLINE>
>>> ui.get_product_information("cheese")
(Fetching from Data Store)
PRODUCT INFORMATION:
Name: Cheese, Price: 2.00, Quantity: 10
>>> ui.get_product_information("eggs")
(Fetching from Data Store)
PRODUCT INFORMATION:
Name: Eggs, Price: 0.20, Quantity: 100
>>> ui.get_product_information("milk")
(Fetching from Data Store)
PRODUCT INFORMATION:
Name: Milk, Price: 1.50, Quantity: 10
>>> ui.get_product_information("arepas")
(Fetching from Data Store)
That product 'arepas' does not exist in the records
```

### Adapter

Адаптирует один интерфейс к другому. Полезен для интеграции классов, которые несовместимы напрямую из-за разных интерфейсов.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/adapter.py)

```python
from typing import Callable, TypeVar

T = TypeVar("T")


class Dog:
    def __init__(self) -> None:
        self.name = "Dog"

    def bark(self) -> str:
        return "woof!"


class Cat:
    def __init__(self) -> None:
        self.name = "Cat"

    def meow(self) -> str:
        return "meow!"


class Human:
    def __init__(self) -> None:
        self.name = "Human"

    def speak(self) -> str:
        return "'hello'"


class Car:
    def __init__(self) -> None:
        self.name = "Car"

    def make_noise(self, octane_level: int) -> str:
        return f"vroom{'!' * octane_level}"


class Adapter:

    def __init__(self, obj: T, **adapted_methods: Callable):
        """We set the adapted methods in the object's dict."""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object."""
        return getattr(self.obj, attr)

    def original_dict(self):
        return self.obj.__dict__


>>> objects = []
>>> dog = Dog()
>>> print(dog.__dict__)
{'name': 'Dog'}
>>> objects.append(Adapter(dog, make_noise=dog.bark))
>>> objects[0].__dict__['obj'], objects[0].__dict__['make_noise']
(<...Dog object at 0x...>, <bound method Dog.bark of <...Dog object at 0x...>>)
>>> print(objects[0].original_dict())
{'name': 'Dog'}
>>> cat = Cat()
>>> objects.append(Adapter(cat, make_noise=cat.meow))
>>> human = Human()
>>> objects.append(Adapter(human, make_noise=human.speak))
>>> car = Car()
>>> objects.append(Adapter(car, make_noise=lambda: car.make_noise(3)))
>>> for obj in objects:
...    print("A {0} goes {1}".format(obj.name, obj.make_noise()))
A Dog goes woof!
A Cat goes meow!
A Human goes 'hello'
A Car goes vroom!!!
```

### Bridge

Отделяет абстракцию от реализации

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/bridge.py)

```python
# ConcreteImplementor 1/2
class DrawingAPI1:
    def draw_circle(self, x, y, radius):
        print(f"API1.circle at {x}:{y} radius {radius}")


# ConcreteImplementor 2/2
class DrawingAPI2:
    def draw_circle(self, x, y, radius):
        print(f"API2.circle at {x}:{y} radius {radius}")


# Refined Abstraction
class CircleShape:
    def __init__(self, x, y, radius, drawing_api):
        self._x = x
        self._y = y
        self._radius = radius
        self._drawing_api = drawing_api

    # low-level i.e. Implementation specific
    def draw(self):
        self._drawing_api.draw_circle(self._x, self._y, self._radius)

    # high-level i.e. Abstraction specific
    def scale(self, pct):
        self._radius *= pct


>>> shapes = (CircleShape(1, 2, 3, DrawingAPI1()), CircleShape(5, 7, 11, DrawingAPI2()))
>>> for shape in shapes:
...    shape.scale(2.5)
...    shape.draw()
API1.circle at 1:2 radius 7.5
API2.circle at 5:7 radius 27.5
```

### Composite

Позволяет клиентам одинаково воспринимать отдельные объекты и их композиции. Шаблон обрабатывает группу объектов как один экземпляр объекта того же типа.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/composite.py)

```python
from abc import ABC, abstractmethod
from typing import List


class Graphic(ABC):
    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError("You should implement this!")


class CompositeGraphic(Graphic):
    def __init__(self) -> None:
        self.graphics: List[Graphic] = []

    def render(self) -> None:
        for graphic in self.graphics:
            graphic.render()

    def add(self, graphic: Graphic) -> None:
        self.graphics.append(graphic)

    def remove(self, graphic: Graphic) -> None:
        self.graphics.remove(graphic)


class Ellipse(Graphic):
    def __init__(self, name: str) -> None:
        self.name = name

    def render(self) -> None:
        print(f"Ellipse: {self.name}")


>>> ellipse1 = Ellipse("1")
>>> ellipse2 = Ellipse("2")
>>> ellipse3 = Ellipse("3")
>>> ellipse4 = Ellipse("4")
>>> graphic1 = CompositeGraphic()
>>> graphic2 = CompositeGraphic()
>>> graphic1.add(ellipse1)
>>> graphic1.add(ellipse2)
>>> graphic1.add(ellipse3)
>>> graphic2.add(ellipse4)
>>> graphic = CompositeGraphic()
>>> graphic.add(graphic1)
>>> graphic.add(graphic2)
>>> graphic.render()
Ellipse: 1
Ellipse: 2
Ellipse: 3
Ellipse: 4
```

### Decorator

Реализует обертку над объектом, обспечивая дополнительное поведение. В python можно использовать [[python-decorator]]

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/decorator.py)

```python
class TextTag:

    def __init__(self, text):
        self._text = text

    def render(self):
        return self._text


class BoldWrapper(TextTag):

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return f"<b>{self._wrapped.render()}</b>"


class ItalicWrapper(TextTag):

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return f"<i>{self._wrapped.render()}</i>"


>>> simple_hello = TextTag("hello, world!")
>>> special_hello = ItalicWrapper(BoldWrapper(simple_hello))
>>> print("before:", simple_hello.render())
before: hello, world!
>>> print("after:", special_hello.render())
after: <i><b>hello, world!</b></i>
```

### Facade

Один класс используется как API для группы других классов. Предоставляет обобщенный и унифицированный интерфейс для более сложных систем.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py)

```python
class CPU:
    def freeze(self):
        print("Freezing processor.")

    def jump(self, position):
        print("Jumping to:", position)

    def execute(self):
        print("Executing.")


class Memory:
    def load(self, position, data):
        print(f"Loading from {position} data: '{data}'.")


class SolidStateDrive:
    def read(self, lba, size):
        return f"Some data from sector {lba} with size {size}"


class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.ssd = SolidStateDrive()

    def start(self):
        self.cpu.freeze()
        self.memory.load("0x00", self.ssd.read("100", "1024"))
        self.cpu.jump("0x00")
        self.cpu.execute()


>>> computer_facade = ComputerFacade()
>>> computer_facade.start()
Freezing processor.
Loading from 0x00 data: 'Some data from sector 100 with size 1024'.
Jumping to: 0x00
Executing.
```

### Fly weight (приспособленецй)

Позволяет прозрачно повторно использовать уже созданные экзепляры объектов с похожими/идентичными состояниями

Направлен на минимизацию количества объектов, которые нужны приложению во время выполнения. Шаблон производит объекты, которые используется одновременно несколькими контейнерами.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/flyweight.py)

### Front controller

Разделяет логику клиента и объекта, предоставляющего данные, что позволяет контроллировать поведение

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/front_controller.py)

```python
class MobileView:
    def show_index_page(self):
        print("Displaying mobile index page")


class TabletView:
    def show_index_page(self):
        print("Displaying tablet index page")


class Dispatcher:
    def __init__(self):
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()

    def dispatch(self, request):
        if request.type == Request.mobile_type:
            self.mobile_view.show_index_page()
        elif request.type == Request.tablet_type:
            self.tablet_view.show_index_page()
        else:
            print("Cannot dispatch the request")


class RequestController:

    def __init__(self):
        self.dispatcher = Dispatcher()

    def dispatch_request(self, request):
        if isinstance(request, Request):
            self.dispatcher.dispatch(request)
        else:
            print("request must be a Request object")


class Request:

    mobile_type = "mobile"
    tablet_type = "tablet"

    def __init__(self, request):
        self.type = None
        request = request.lower()
        if request == self.mobile_type:
            self.type = self.mobile_type
        elif request == self.tablet_type:
            self.type = self.tablet_type


>>> front_controller = RequestController()
>>> front_controller.dispatch_request(Request('mobile'))
Displaying mobile index page
>>> front_controller.dispatch_request(Request('tablet'))
Displaying tablet index page
>>> front_controller.dispatch_request(Request('desktop'))
Cannot dispatch the request
>>> front_controller.dispatch_request('mobile')
request must be a Request object
```

### Mvc (model->view->controller)

Расширяет предыдущую модель. [Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/mvc.py) с использованием [[abc]]

### Proxy

Объект передает операции кому-то еще. Прокси используется там, где надо добавить в класс функциональность, не меняя его (например добавление журналирования, кешировавния, авторизацию и т.д.)

Субъекты и прокси в паттерне требуют реализации одинаковых интерфейсов.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/structural/proxy.py)

```python
from typing import Union


class Subject:

    def do_the_job(self, user: str) -> None:
        raise NotImplementedError()


class RealSubject(Subject):

    def do_the_job(self, user: str) -> None:
        print(f"I am doing the job for {user}")


class Proxy(Subject):

    def __init__(self) -> None:
        self._real_subject = RealSubject()

    def do_the_job(self, user: str) -> None:
        print(f"[log] Doing the job for {user} is requested.")

        if user == "admin":
            self._real_subject.do_the_job(user)
        else:
            print("[log] I can do the job just for `admins`.")


def client(job_doer: Union[RealSubject, Proxy], user: str) -> None:
    job_doer.do_the_job(user)


>>> proxy = Proxy()
>>> real_subject = RealSubject()
>>> client(proxy, 'admin')
[log] Doing the job for admin is requested.
I am doing the job for admin
>>> client(proxy, 'anonymous')
[log] Doing the job for anonymous is requested.
[log] I can do the job just for `admins`.
>>> client(real_subject, 'admin')
I am doing the job for admin
>>> client(real_subject, 'anonymous')
I am doing the job for anonymous
```

## Поведенческие паттерны

### Chaining method

Продолжимть выполнение операций обратным вызовом следующего метода

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/chaining_method.py)

```python
from __future__ import annotations


class Person:
    def __init__(self, name: str, action: Action) -> None:
        self.name = name
        self.action = action

    def do_action(self) -> Action:
        print(self.name, self.action.name, end=" ")
        return self.action


class Action:
    def __init__(self, name: str) -> None:
        self.name = name

    def amount(self, val: str) -> Action:
        print(val, end=" ")
        return self

    def stop(self) -> None:
        print("then stop")


>>> move = Action('move')
>>> person = Person('Jack', move)
>>> person.do_action().amount('5m').stop()
Jack move 5m then stop
```

### Chain of responsibility

Цепочка последовательнывх обработчиков. (if... elif...elif...else)

Блоки могут быть переставлены реконфигурированы во время выполнения. Отделяет отправителя запроса от принимающего. Принимающий знает только последнего отправителя.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/chain_of_responsibility.py)

### Catalog

Обобщенный метод вызывает специальные методы, основываясь на параметре состояния.

[Пример (и примеры других реализаций)](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/catalog.py)

```python
class Catalog:

    def __init__(self, param: str) -> None:
        self._static_method_choices = {
            "param_value_1": self._static_method_1,
            "param_value_2": self._static_method_2,
        }

        # simple test to validate param value
        if param in self._static_method_choices.keys():
            self.param = param
        else:
            raise ValueError(f"Invalid Value for Param: {param}")

    @staticmethod
    def _static_method_1() -> None:
        print("executed method 1!")

    @staticmethod
    def _static_method_2() -> None:
        print("executed method 2!")

    def main_method(self) -> None:
        self._static_method_choices[self.param]()

>>> test = Catalog('param_value_2')
>>> test.main_method()
executed method 2!
```

### Command

Создаем бандл из аргументов и методов для вызова позже.

Отделяет объект, выдающий задачу от того, кто знает как ее сделать.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/command.py) - пункты в меню, вызывающие один и тот же метод при нажатии.

```python
from typing import Union


class HideFileCommand:

    def __init__(self) -> None:
        # an array of files hidden, to undo them as needed
        self._hidden_files = []

    def execute(self, filename: str) -> None:
        print(f"hiding {filename}")
        self._hidden_files.append(filename)

    def undo(self) -> None:
        filename = self._hidden_files.pop()
        print(f"un-hiding {filename}")


class DeleteFileCommand:

    def __init__(self) -> None:
        # an array of deleted files, to undo them as needed
        self._deleted_files = []

    def execute(self, filename: str) -> None:
        print(f"deleting {filename}")
        self._deleted_files.append(filename)

    def undo(self) -> None:
        filename = self._deleted_files.pop()
        print(f"restoring {filename}")


class MenuItem:

    def __init__(self, command: Union[HideFileCommand, DeleteFileCommand]) -> None:
        self._command = command

    def on_do_press(self, filename: str) -> None:
        self._command.execute(filename)

    def on_undo_press(self) -> None:
        self._command.undo()


>>> item1 = MenuItem(DeleteFileCommand())
>>> item2 = MenuItem(HideFileCommand())
# create a file named `test-file` to work with
>>> test_file_name = 'test-file'
# deleting `test-file`
>>> item1.on_do_press(test_file_name)
deleting test-file
# restoring `test-file`
>>> item1.on_undo_press()
restoring test-file
# hiding `test-file`
>>> item2.on_do_press(test_file_name)
hiding test-file
# un-hiding `test-file`
>>> item2.on_undo_press()
un-hiding test-file
```

### Iterator

Пройти через контейнер и получить доступ к его элементам

В python итераторы реализуются на уровне маг.методов

```python
class Count:
    """Iterator that counts upward forever"""
    def __init__(self, start=0):
        self.num = start
    def __iter__(self):
        return self
    def __next__(self):
        num = self.num
        self.num += 1
        return num
```

смотри [другой пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/iterator_alt.py)

### Mediator

Соединяет другие объекты в одном объекте и действует как прокси. Сокращает число связей в коде.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/mediator.py)

```python
from __future__ import annotations


class ChatRoom:
    """Mediator class"""

    def display_message(self, user: User, message: str) -> None:
        print(f"[{user} says]: {message}")


class User:
    """A class whose instances want to interact with each other"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.chat_room = ChatRoom()

    def say(self, message: str) -> None:
        self.chat_room.display_message(self, message)

    def __str__(self) -> str:
        return self.name


>>> molly = User('Molly')
>>> mark = User('Mark')
>>> ethan = User('Ethan')
>>> molly.say("Hi Team! Meeting at 3 PM today.")
[Molly says]: Hi Team! Meeting at 3 PM today.
>>> mark.say("Roger that!")
[Mark says]: Roger that!
>>> ethan.say("Alright.")
[Ethan says]: Alright.
```

### Memento

Создает вложенный объект (как правило замыкание) - токен, который можно использовать для возврата другого объекта к предыдущему состоянию. [Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/memento.py)

### Observer (наблюдатель)

Обеспечивает обратный вызов для уведомления о событиях

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/observer.py)

```python
from __future__ import annotations
from contextlib import suppress
from typing import Protocol


# define a generic observer type
class Observer(Protocol):
    def update(self, subject: Subject) -> None:
        pass


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self, modifier: Observer | None = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)


class Data(Subject):
    def __init__(self, name: str = "") -> None:
        super().__init__()
        self.name = name
        self._data = 0

    @property
    def data(self) -> int:
        return self._data

    @data.setter
    def data(self, value: int) -> None:
        self._data = value
        self.notify()


class HexViewer:
    def update(self, subject: Data) -> None:
        print(f"HexViewer: Subject {subject.name} has data 0x{subject.data:x}")


class DecimalViewer:
    def update(self, subject: Data) -> None:
        print(f"DecimalViewer: Subject {subject.name} has data {subject.data}")


>>> data1 = Data('Data 1')
>>> data2 = Data('Data 2')
>>> view1 = DecimalViewer()
>>> view2 = HexViewer()
>>> data1.attach(view1)
>>> data1.attach(view2)
>>> data2.attach(view2)
>>> data2.attach(view1)
>>> data1.data = 10
DecimalViewer: Subject Data 1 has data 10
HexViewer: Subject Data 1 has data 0xa
>>> data2.data = 15
HexViewer: Subject Data 2 has data 0xf
DecimalViewer: Subject Data 2 has data 15
>>> data1.data = 3
DecimalViewer: Subject Data 1 has data 3
HexViewer: Subject Data 1 has data 0x3
>>> data2.data = 5
HexViewer: Subject Data 2 has data 0x5
DecimalViewer: Subject Data 2 has data 5
# Detach HexViewer from data1 and data2
>>> data1.detach(view2)
>>> data2.detach(view2)
>>> data1.data = 10
DecimalViewer: Subject Data 1 has data 10
>>> data2.data = 15
DecimalViewer: Subject Data 2 has data 15
```

### Publish subscribe

Источник данных аккумулирует и рассылает данные для неопределенного круга подписчиков

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/publish_subscribe.py)

```python
class Provider:
    def __init__(self):
        self.msg_queue = []
        self.subscribers = {}

    def notify(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        self.subscribers.setdefault(msg, []).append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers[msg].remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            for sub in self.subscribers.get(msg, []):
                sub.run(msg)
        self.msg_queue = []


class Publisher:
    def __init__(self, msg_center):
        self.provider = msg_center

    def publish(self, msg):
        self.provider.notify(msg)


class Subscriber:
    def __init__(self, name, msg_center):
        self.name = name
        self.provider = msg_center

    def subscribe(self, msg):
        self.provider.subscribe(msg, self)

    def unsubscribe(self, msg):
        self.provider.unsubscribe(msg, self)

    def run(self, msg):
        print(f"{self.name} got {msg}")


>>> message_center = Provider()
>>> fftv = Publisher(message_center)
>>> jim = Subscriber("jim", message_center)
>>> jim.subscribe("cartoon")
>>> jack = Subscriber("jack", message_center)
>>> jack.subscribe("music")
>>> gee = Subscriber("gee", message_center)
>>> gee.subscribe("movie")
>>> vani = Subscriber("vani", message_center)
>>> vani.subscribe("movie")
>>> vani.unsubscribe("movie")
# Note that no one subscribed to `ads`
# and that vani changed their mind
>>> fftv.publish("cartoon")
>>> fftv.publish("music")
>>> fftv.publish("ads")
>>> fftv.publish("movie")
>>> fftv.publish("cartoon")
>>> fftv.publish("cartoon")
>>> fftv.publish("movie")
>>> fftv.publish("blank")
>>> message_center.update()
jim got cartoon
jack got music
gee got movie
jim got cartoon
jim got cartoon
gee got movie
```

### Registry

Позволяет отслеживать все подклассы исходного класса. Реализуется через метаклассы - смотри [[abc]]

Пример

```python
class RegistryHolder(type):

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        """Here the name of the class is used as key but it could be any class
        parameter.
        """
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class BaseRegisteredClass(metaclass=RegistryHolder):
    """Any class that will inherits from BaseRegisteredClass will be included
    inside the dict RegistryHolder.REGISTRY, the key being the name of the
    class and the associated value, the class itself.
    """


# Before subclassing
>>> sorted(RegistryHolder.REGISTRY)
['BaseRegisteredClass']
>>> class ClassRegistree(BaseRegisteredClass):
...    def __init__(self, *args, **kwargs):
...        pass
# After subclassing
>>> sorted(RegistryHolder.REGISTRY)
['BaseRegisteredClass', 'ClassRegistree']
```

### Specification

Бизнес логика может быть повторно использована с помощью рекомбенации и булевой логики.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/specification.py) реализуется чсерез [[abc]]

### State

Реализация логики в виде дискретного числа потенциальных состояний и следующего состояния, в которое можно перейти.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/state.py)

```python
class State:
    """Base state. This is to share functionality"""

    def scan(self):
        """Scan the dial to the next station"""
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print(f"Scanning... Station is {self.stations[self.pos]} {self.name}")


class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Switching to FM")
        self.radio.state = self.radio.fmstate


class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Switching to AM")
        self.radio.state = self.radio.amstate


class Radio:
    """A radio. It has a scan button, and an AM/FM toggle switch."""

    def __init__(self):
        """We have an AM state and an FM state"""
        self.amstate = AmState(self)
        self.fmstate = FmState(self)
        self.state = self.amstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()


>>> radio = Radio()
>>> actions = [radio.scan] * 2 + [radio.toggle_amfm] + [radio.scan] * 2
>>> actions *= 2

>>> for action in actions:
...    action()
Scanning... Station is 1380 AM
Scanning... Station is 1510 AM
Switching to FM
Scanning... Station is 89.1 FM
Scanning... Station is 103.9 FM
Scanning... Station is 81.3 FM
Scanning... Station is 89.1 FM
Switching to AM
Scanning... Station is 1250 AM
Scanning... Station is 1380 AM
```

Маленькая ремарка: на мой взгляд этот паттерн и несколько аналогичных вышеобозначенных, нежизнеспособны в python по ряду причин:

- громоздкость
- росто сложности по мере роста числа реализаций
- плохая передача/наследование структурной информации между объектами на уровне кода (потребуется значительный объем работы для того, чтобы разобраться как это устроено). Особенно это заметно в данном примере

### Strategy

Реализует выбор операций над одними и теми же данными. Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми. Стратегия позволяет алгоритму изменяться независимо от клиентов, которые его используют.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/strategy.py). В данном примере реализован класс-валидатор и несколько дисконтных стратегий. Мы валидируем применеение стратегий, чтобы не допустить непримлемое снижение цены.

```python
from __future__ import annotations
from typing import Callable


class DiscountStrategyValidator:  # Descriptor class for check perform
    @staticmethod
    def validate(obj: Order, value: Callable) -> bool:
        try:
            if obj.price - value(obj) < 0:
                raise ValueError(
                    f"Discount cannot be applied due to negative price resulting. {value.__name__}"
                )
        except ValueError as ex:
            print(str(ex))
            return False
        else:
            return True

    def __set_name__(self, owner, name: str) -> None:
        self.private_name = f"_{name}"

    def __set__(self, obj: Order, value: Callable = None) -> None:
        if value and self.validate(obj, value):
            setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.private_name, None)

    def __get__(self, obj: object, objtype: type = None):
        return getattr(obj, self.private_name)


class Order:
    discount_strategy = DiscountStrategyValidator()

    def __init__(self, price: float, discount_strategy: Callable = None) -> None:
        self.price: float = price
        self.discount_strategy = discount_strategy

    def apply_discount(self) -> float:
        if self.discount_strategy:
            discount = self.discount_strategy(self)
        else:
            discount = 0

        return self.price - discount

    def __repr__(self) -> str:
        return f"<Order price: {self.price} with discount strategy: {getattr(self.discount_strategy,'__name__',None)}>"


def ten_percent_discount(order: Order) -> float:
    return order.price * 0.10


def on_sale_discount(order: Order) -> float:
    return order.price * 0.25 + 20


>>> order = Order(100, discount_strategy=ten_percent_discount)
>>> print(order)
<Order price: 100 with discount strategy: ten_percent_discount>
>>> print(order.apply_discount())
90.0
>>> order = Order(100, discount_strategy=on_sale_discount)
>>> print(order)
<Order price: 100 with discount strategy: on_sale_discount>
>>> print(order.apply_discount())
55.0
>>> order = Order(10, discount_strategy=on_sale_discount)
Discount cannot be applied due to negative price resulting. on_sale_discount
>>> print(order)
<Order price: 10 with discount strategy: None>
```

В данном примере реализован дескриптор (смотри [[python-descriptors]]).  `__set_name__` вызывается сразу после того, как определен класс-владелец. Затем, при создании экземпляра класса владельца функция расчета скидки вызывается первый раз, чтобы провалидировать ее параметры валидатором дескриптора и сохранить в дескрипторе объект функции для дальнейшего вызова. При вызове метода `apply_discount()` мы обращаемся к дескриптору, чтобы применить скидку или не сделать ничего.

### Template

Объект определяет структуру и принимает подключаемые компоненты

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/template.py)

```python
def get_text():
    return "plain-text"


def get_pdf():
    return "pdf"


def get_csv():
    return "csv"


def convert_to_text(data):
    print("[CONVERT]")
    return f"{data} as text"


def saver():
    print("[SAVE]")


def template_function(getter, converter=False, to_save=False):
    data = getter()
    print(f"Got `{data}`")

    if len(data) <= 3 and converter:
        data = converter(data)
    else:
        print("Skip conversion")

    if to_save:
        saver()

    print(f"`{data}` was processed")


>>> template_function(get_text, to_save=True)
Got `plain-text`
Skip conversion
[SAVE]
`plain-text` was processed
>>> template_function(get_pdf, converter=convert_to_text)
Got `pdf`
[CONVERT]
`pdf as text` was processed
>>> template_function(get_csv, to_save=True)
Got `csv`
Skip conversion
[SAVE]
`csv` was processed
```

### Visitor (посетитель)

Реализует обратный вызов для всех объектов коллекции

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/behavioral/visitor.py)

```python
class Node:
    pass


class A(Node):
    pass


class B(Node):
    pass


class C(A, B):
    pass


class Visitor:
    def visit(self, node, *args, **kwargs):
        meth = None
        for cls in node.__class__.__mro__:
            meth_name = "visit_" + cls.__name__
            meth = getattr(self, meth_name, None)
            if meth:
                break

        if not meth:
            meth = self.generic_visit
        return meth(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        print("generic_visit " + node.__class__.__name__)

    def visit_B(self, node, *args, **kwargs):
        print("visit_B " + node.__class__.__name__)


>>> a, b, c = A(), B(), C()
>>> visitor = Visitor()
>>> visitor.visit(a)
generic_visit A
>>> visitor.visit(b)
visit_B B
>>> visitor.visit(c)
visit_B C
```

## Другие паттерны

### Три способа инъекции зависимостей

Внедрение зависимостей — это метод, при котором один объект предоставляет зависимости (сервисы) другому объекту (клиенту). Это позволяет отделять объекты: нет необходимости изменять клиентский код если возникла потребность изменить код сервиса.

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/dependency_injection.py)

```python
import datetime
from typing import Callable

class ConstructorInjection:
    def __init__(self, time_provider: Callable) -> None:
        self.time_provider = time_provider

    def get_current_time_as_html_fragment(self) -> str:
        current_time = self.time_provider()
        current_time_as_html_fragment = '<span class="tinyBoldText">{}</span>'.format(
            current_time
        )
        return current_time_as_html_fragment


class ParameterInjection:
    def __init__(self) -> None:
        pass

    def get_current_time_as_html_fragment(self, time_provider: Callable) -> str:
        current_time = time_provider()
        current_time_as_html_fragment = '<span class="tinyBoldText">{}</span>'.format(
            current_time
        )
        return current_time_as_html_fragment


class SetterInjection:
    """Setter Injection"""

    def __init__(self) -> None:
        pass

    def set_time_provider(self, time_provider: Callable):
        self.time_provider = time_provider

    def get_current_time_as_html_fragment(self):
        current_time = self.time_provider()
        current_time_as_html_fragment = '<span class="tinyBoldText">{}</span>'.format(
            current_time
        )
        return current_time_as_html_fragment


def production_code_time_provider() -> str:
    """
    Production code version of the time provider (just a wrapper for formatting
    datetime for this example).
    """
    current_time = datetime.datetime.now()
    current_time_formatted = f"{current_time.hour}:{current_time.minute}"
    return current_time_formatted


def midnight_time_provider() -> str:
    """Hard-coded stub"""
    return "24:01"


>>> time_with_ci1 = ConstructorInjection(midnight_time_provider)
>>> time_with_ci1.get_current_time_as_html_fragment()
'<span class="tinyBoldText">24:01</span>'
>>> time_with_ci2 = ConstructorInjection(production_code_time_provider)
>>> time_with_ci2.get_current_time_as_html_fragment()
'<span class="tinyBoldText">...</span>'
>>> time_with_pi = ParameterInjection()
>>> time_with_pi.get_current_time_as_html_fragment(midnight_time_provider)
'<span class="tinyBoldText">24:01</span>'
>>> time_with_si = SetterInjection()
>>> time_with_si.get_current_time_as_html_fragment()
Traceback (most recent call last):
...
AttributeError: 'SetterInjection' object has no attribute 'time_provider'
>>> time_with_si.set_time_provider(midnight_time_provider)
>>> time_with_si.get_current_time_as_html_fragment()
'<span class="tinyBoldText">24:01</span>'
```

### Blackboard

В шаблоне Blackboard несколько специализированных подсистем (источников данных) собирают свои знания для построения, возможно, частичного или приблизительного решения. Таким образом, подсистемы работают вместе для решения проблемы, где решение представляет собой сумму решений подсистем. [Пример](https://github.com/faif/python-patterns/blob/master/patterns/other/blackboard.py)

### graph search

Варианты поиска путей в графе на оснвое поиска в глубину, а так-же кратчайшие пути через поиск в глубину и в ширину. [Пример](https://github.com/faif/python-patterns/blob/master/patterns/other/graph_search.py)

```python

class GraphSearch:

    def __init__(self, graph):
        self.graph = graph

    def find_path_dfs(self, start, end, path=None):
        path = path or []

        path.append(start)
        if start == end:
            return path
        for node in self.graph.get(start, []):
            if node not in path:
                newpath = self.find_path_dfs(node, end, path[:])
                if newpath:
                    return newpath

    def find_all_paths_dfs(self, start, end, path=None):
        path = path or []
        path.append(start)
        if start == end:
            return [path]
        paths = []
        for node in self.graph.get(start, []):
            if node not in path:
                newpaths = self.find_all_paths_dfs(node, end, path[:])
                paths.extend(newpaths)
        return paths

    def find_shortest_path_dfs(self, start, end, path=None):
        path = path or []
        path.append(start)

        if start == end:
            return path
        shortest = None
        for node in self.graph.get(start, []):
            if node not in path:
                newpath = self.find_shortest_path_dfs(node, end, path[:])
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def find_shortest_path_bfs(self, start, end):
        queue = [start]
        dist_to = {start: 0}
        edge_to = {}

        if start == end:
            return queue

        while len(queue):
            value = queue.pop(0)
            for node in self.graph[value]:
                if node not in dist_to.keys():
                    edge_to[node] = value
                    dist_to[node] = dist_to[value] + 1
                    queue.append(node)
                    if end in edge_to.keys():
                        path = []
                        node = end
                        while dist_to[node] != 0:
                            path.insert(0, node)
                            node = edge_to[node]
                        path.insert(0, start)
                        return
```

### Hiearchical state machine

[Пример](https://github.com/faif/python-patterns/blob/master/patterns/other/hsm/hsm.py)

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[from-future-import-annotations]: from-future-import-annotations "From future import annotations"
[type-annotation]: type-annotation "Аннотация типов в python"
[typing]: typing "Typing"
[abc]: abc "Abc"
[python-decorator]: python-decorator "Python decorator"
[python-descriptors]: python-descriptors "Python descriptors"
[python-standart-library]: ..%2Flists%2Fpython-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"