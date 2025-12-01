---
description: Создание матриц с помощью вложенных списков в python
tags: python-standart-library python
title: Creation of list matrix
---
```python
>>> matrix = [[i for i in range(5)] for _ in range(6)]
>>> matrix
[
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4]
]
```

Распаковка

```python
matrix = [
...     [0, 0, 0],
...     [1, 1, 1],
...     [2, 2, 2],
... ]
>>> flat = [num for row in matrix for num in row]
>>> flat
[0, 0, 0, 1, 1, 1, 2, 2, 2]
```

Или проще для восприятия:

```python
>>> matrix = [
...     [0, 0, 0],
...     [1, 1, 1],
...     [2, 2, 2],
... ]
>>> flat = []
>>> for row in matrix:
...     for num in row:
...         flat.append(num)
...
>>> flat
[0, 0, 0, 1, 1, 1, 2, 2, 2]
```

Таже история для словарей

```python
>>> cities = ['Austin', 'Tacoma', 'Topeka', 'Sacramento', 'Charlotte']
>>> temps = {city: [0 for _ in range(7)] for city in cities}
>>> temps
{
    'Austin': [0, 0, 0, 0, 0, 0, 0],
    'Tacoma': [0, 0, 0, 0, 0, 0, 0],
    'Topeka': [0, 0, 0, 0, 0, 0, 0],
    'Sacramento': [0, 0, 0, 0, 0, 0, 0],
    'Charlotte': [0, 0, 0, 0, 0, 0, 0]
}
```

[Источник](https://webdevblog.ru/kogda-ispolzovat-list-comprehension-v-python/)

[[python-standart-library]]


[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
