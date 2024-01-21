---
description: Использование super() в python
tags: python-standart-library python
title: Python super guide
---
Базовый вариант использования

```python
class LoggingDict(dict):
    def __setitem__(self, key, value):
        logging.info('Setting %r to %r' % (key, value))
        super().__setitem__(key, value)
```

Этот класс имеет все те же возможности, что и его родитель, dict , но он расширяет метод `__setitem__`, чтобы создавать записи в журнале при каждом обновлении ключа. После внесения записи в журнал метод использует `super()` для делегирования работы по фактическому обновлению словаря с помощью пары ключ/значение.

Класс, которому делегируется работа указаывать по имени не нужно

```python
class LoggingDict(SomeOtherMapping):            # new base class
    def __setitem__(self, key, value):
        logging.info('Setting %r to %r' % (key, value))
        super().__setitem__(key, value)         # no change needed
```

Какой именно класс будет вызван зависит от того, как образовано дерево родительских классов. В примере ниже оно выглядит так: LoggingOD, LoggingDict, OrderedDict, dict, object - работа будет делегирована нужному нам методу в `OrderedDict`

```python
class LoggingOD(LoggingDict, collections.OrderedDict):
    pass
```

Мы не изменяли исходный код LoggingDict. Вместо этого мы создали подкласс, единственная логика которого состоит в том, чтобы объединить два существующих класса и управлять порядком поиска в них. Порядок поиска реализован через модель MRO

```python
>>> pprint(LoggingOD.__mro__)
(<class '__main__.LoggingOD'>,
 <class '__main__.LoggingDict'>,
 <class 'collections.OrderedDict'>,
 <class 'dict'>,
 <class 'object'>)
 ```

`super()` занимается делегированием вызовов методов некоторому классу в дереве предков экземпляра. Чтобы переупорядочиваемые вызовы методов работали, классы должны разрабатываться совместно. При этом возникают три легко решаемых правила:

- метод, вызываемый `super()`, должен существовать
- вызывающий и вызываемый методы должны иметь совпадающую сигнатуру аргумента
- каждое вхождение метода должно использовать `super()`

Рассмотрим стратегии получения аргументов вызывающего объекта, чтобы они соответствовали сигнатуре вызываемого метода. Это немного сложнее, чем традиционные вызовы методов, когда вызываемый объект известен заранее. При использовании `super()` вызываемый объект неизвестен во время написания класса (поскольку подкласс, написанный позже, может ввести новые классы в MRO).

Один из подходов состоит в том, чтобы придерживаться фиксированной подписи, используя позиционные аргументы. Это хорошо работает с такими методами, как `__setitem__`, которые имеют фиксированную сигнатуру из двух аргументов, ключа и значения.

Более гибкий подход состоит в том, чтобы каждый метод в дереве родителей был разработан совместно, чтобы принимать ключевые аргументы словарь ключевых аргументов, удалять любые аргументы, и перенаправлять оставшиеся аргументы с помощью **kwds, в конечном итоге оставляя словарь пустым. для последнего вызова в цепочке.

Каждый уровень убирает ключевые аргументы, которые ему нужны, чтобы окончательный пустой словарь мог быть отправлен методу, который вообще не ожидает аргументов (например, `object.__init__` в примере ниже не ожидает аргументов)

```python
class Shape:
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)

cs = ColoredShape(color='red', shapename='circle')
```

Следующая проблема - как убедиться, что целевой метод существует. В примере выше мы знаем, что у `object` всегда есть `__init__()` и `object` - всегда последний в цепочке МРО, поэтому любая последовательность из `super().__init__(**kwds)` гарантированно завершается вызовом метода `object.__init__()`. Но так бывает далеко не всегда и `object` может не иметь необходимого нам метода. Для таких случаев требуется написать корневой класс, который гарантированно будет вызываться перед `object` и будет иметь нужный нам метод. Задача такого корневого класса - стать последним в цепочке вызовов, заменив собойс `object`.

```python
class Root:
    def draw(self):
        # the delegation chain stops here
        assert not hasattr(super(), 'draw')

class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        super().draw()

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

cs = ColoredShape(color='blue', shapename='square')
cs.draw()
```

В данном примере, если мы захотим внедрить дополнительные классы, нам придется так-же отнаследовать их от корневого, чтобы ни один из путей в дереве не мог достичь `object` минуя `Root.draw()`. Необходимо написать об этом в документации.

Наконец, для гарантирантий выполнения всей цепочки, каждый делегирующий метод каждого класса должен реализовывать `super()`.

Иногда подкласс может захотеть использовать совместные методы, доступные через множественне наследование со сторонним классом, который не был предназначен для этого (к примеру, в нем не реализован `super()` или не реализован корневой класс). Для этого реализуется класс-адаптер.

```python
class Moveable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        print('Drawing at position:', self.x, self.y)
```

Адаптером для этого класса будет:

```python
class MoveableAdapter(Root):
    def __init__(self, x, y, **kwds):
        self.movable = Moveable(x, y)
        super().__init__(**kwds)
    def draw(self):
        self.movable.draw()
        super().draw()
```

И далее:

```python
class MovableColoredShape(ColoredShape, MoveableAdapter):
    pass

MovableColoredShape(color='red', shapename='triangle',
                    x=10, y=20).draw()
```

## Нюансы

- При создании подклассов встроенной функции, такой как `dict()`, часто необходимо переопределить или расширить несколько методов одновременно. В приведенных выше примерах расширение `__setitem__` не используется другими методами, такими как `dict.update`, поэтому может потребоваться их расширение. Это требование не уникально для `super()`; скорее, оно возникает всякий раз, когда встроенные функции являются подклассами.
- Если класс опирается на один родительский класс, предшествующий другому (например, `LoggingOD` зависит от  `LoggingDict` , следующего перед `OrderedDict`, который стоит перед `dict`), легко добавить утверждения для проверки и документирования предполагаемого порядка разрешения методов:

    ```python
        position = LoggingOD.__mro__.index
        assert position(LoggingDict) < position(OrderedDict)
        assert position(OrderedDict) < position(dict)
    ```

Полный пример кода [тут](https://code.activestate.com/recipes/577720-how-to-use-super-effectively/)

Смотри еще:

- [сорс](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)
- [[python-datamodel]]
- [[python-buildin-functions]]
- [[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-datamodel]: ../lists/python-datamodel "Python datamodel"
[python-buildin-functions]: python-buildin-functions "Python build-in functions"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"