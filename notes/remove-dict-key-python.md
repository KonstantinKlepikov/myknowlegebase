---
description: How remove a key from a Python dictionary
tags: python-standart-library python
title: Как удалить ключ словаря в python
---
```python
my_dict.pop('key', None)
```

Это вернет `my_dict[key]`, если ключ есть. Если ключа нет, будет возвращен `None`. Если второй параметр не задан, а ключа нет - будет поднята ошибка `KeyError`.

Еще можно так:

```python
del my_dict['key']
```

В этом случае так-же следует ожидать `KeyError`

[[python-standart-library]]


[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
