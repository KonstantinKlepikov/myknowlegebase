---
description: collection.OrderedDict в стандартной библиотеке python
tags: python-standart-library python
title: OrderedDict упорядоченный словарь с опцией сравнения по порядку
---
Начиная с 3.6 словари в python упорядочены. OrderedDict позволяет сравниваться не только по эквивалентности вхождения, но и с учетом порядка

```python
import collections

d1 = {}
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = {}
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'
print(d1 == d2)
>>> True

d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = collections.OrderedDict()
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'

print(d1 == d2)
>>> False
```

Метод `move_to_end` позволяет перемещать ключи в конец или в начало словаря

```python
d = OrderedDict.fromkeys('abcde')
d.move_to_end('b')
print(''.join(d.keys()))
>>> 'acdeb'
d.move_to_end('b', last=False)
print(''.join(d.keys()))
>>> 'bacde'
```

[Документация](https://docs.python.org/3/library/collections.html#ordereddict-objects)

[[python-standart-library]]


[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
