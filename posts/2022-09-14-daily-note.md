---
title: Some python tricks 1 - custom exceptions, dataclasses, dot accessing to dict and annotations
description: Some tricks for custom exceptions, dataclasses, dot accessing to dict and annotations
category: post
---
## translate in Python to transliterate Cyrillic

[source](https://stackoverflow.com/a/14173535/15966204)

## How call ipython from virtualenv

`python -m IPython`

## Proper way to declare custom exceptions in modern Python

```python
class ValidationError(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors
```

[source](https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python)

## Accessing dict keys like an attribute

[discussion](https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute)

example:

```python
class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
```

[source](https://stackoverflow.com/a/32107024/15966204)

[dotmap](https://github.com/drgrib/dotmap) Dot access dictionary with dynamic hierarchy creation and ordered iteration

## How to annotate a type that's a class object (instead of a class instance)

```python
from typing import Type
class Foo: ...
class Bar(Foo): ...
class Baz: ...
some_class: Type[Foo]
some_class = Foo # ok
some_class = Bar # ok
some_class = Baz # error
some_class = Foo() # error
```

[source](https://stackoverflow.com/a/43457817/15966204)

## Types annotations for classes with dynamic attribute names

[example that not solve problem](https://stackoverflow.com/questions/68213424/types-annotations-for-classes-with-dynamic-attribute-names)

## How to return dictionary keys as a list in Python

```python
>>> newdict = {1:0, 2:0, 3:0}
>>> [*newdict]
[1, 2, 3]
```

[source](https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python)

Смотри еще:

- [[type-annotation]]


[type-annotation]: ../notes/type-annotation "Аннотация типов в python"
