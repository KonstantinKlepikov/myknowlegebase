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

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[abc]: abc "Abc"
[python-decorator]: python-decorator "Python decorator"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"