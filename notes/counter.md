---
description: collection.Counter в стандартной библиотеке python
tags: python-standart-library
---
# Counter - счетчик хешируемых объектов

Начиная с 3.7 - сабкласс `dict` упорядоченый и поддерживает операции. связанные с порядком.

Инициализировать можно, передав последовательность для подсчета или словарь значение:количество или через присвоение аргументам. Одинаковые имена словаря естественно не поддерживаются :)

```python
import collections
collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
collections.Counter({'a': 2, 'b': 3, 'c': 1})
collections.Counter(a=2, b=3, c=1)
```

Можно создать пустой каунтер и заполнить его позже методом `update()`

```python
c = collections.Counter()
c.update('abcdaab')
c.update({'a': 1, 'd': 5})
```

При этом значения счетчиков будут увеличены в соответствии с переданными данными, а не заменены. Доступ к значениям счетчика можно получить по API словаря

```python
c = collections.Counter({'a': 2, 'b': 3, 'c': 1})
print(c['a'])
>>> 2
```

При этом исключение `KeyError` не поднимается, если такого ключа нет, а возвращается значение 0.

Счетчик можно установить непосредственно по API словаря. При этом установка значения в 0 не удаляет элемент из каунтера. Для удаления надо использорвать `del`

```python
c['sausage'] = 0
del c['sausage']  
```

## Методы

`elements()` возвращает итератор имен элементов в порядке добавления и в количестве, равном значению счетчика. Значения, равные 0 и меньше не возвращаются

```python
c = Counter(a=4, e=2, c=0, d=-2, b=1)
list(c.elements())
>>> ['a', 'a', 'a', 'a', 'e', 'e', 'b']
```

`most_common([n])` наиболее часто встречаемый элемент(-ы) - список кортежей (элемент, счетчик)

`subtract([iterable-or-mapping])` разница с заменой

```python
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
priint(c.subtract(d))
>>> Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
```

Помимо этого доступны мат.операции, а так-же операции +=, -+, &=, |=. При этом создаются новые объекты, в которых элементы с нулевым или отрицательным значением счетчика отбрасываются

```python
c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')
c1 + c2
c1 - c2
c1 & c2
c1 | c2
```

`total()` позволяет посчитать сумму всех значений счетчика

Наиболее распространенные паттерны

```python
c.total()                       # total of all counts
c.clear()                       # reset all counts
list(c)                         # list unique elements
set(c)                          # convert to a set
dict(c)                         # convert to a regular dictionary
c.items()                       # convert to a list of (elem, cnt) pairs
Counter(dict(list_of_pairs))    # convert from a list of (elem, cnt) pairs
c.most_common()[:-n-1:-1]       # n least common elements
+c                              # remove zero and negative counts
```

[Ссылка на документацию](https://docs.python.org/3/library/collections.html#counter-objects)

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"