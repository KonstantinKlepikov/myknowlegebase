---
description: Про ошибки и исключения в python
tags: python-standart-library python
title: Try except raise
---
Сначала выполняется `try` (код между ключевыми словами `try` и `except`).

Если не возникает исключение, `except` пропускается и выполнение оператора `try` завершается.

Если во время выполнения `try` возникает исключение, остальная часть кода пропускается. Затем, если тип исключения соответствует исключению, названному в `except`, выполняется код в `except`, а затем выполнение продолжается после блока `try` / `except`.

Если возникает исключение, которое не соответствует исключению, указанному в `except`, оно передается во внешние операторы `try`; если обработчик не найден, это состояние является необработанным исключением, и выполнение программы останавливается с сообщениемоб ошибки.

У оператора `try` может быть более одного предложения `except`. Будет выполнено **не более одного обработчика исключений**. Обработчики обрабатывают только исключения, которые возникают в соответствующем `try`, а не в других обработчиках того же оператора `try`. `except` может содержать несколько исключений в виде кортежа.

```python
... except (RuntimeError, TypeError, NameError):
...     pass
```

Оператор `try` / `except` имеет необязательный `else`, который, если присутствует, должен быть определен после всех `except`. Это полезно для кода, который должен выполняться, если не возникло исключений и позволяет избежать случайного перехвата исключений, которые не были вызваны в теле `try` / `except`

Когда возникает исключение, с ним может быть связано значение, также известное как аргумент исключения. Наличие и тип аргумента зависят от типа исключения. В предложении `except` может быть указана переменная после имени исключения. Переменная привязана к экземпляру исключения с аргументами, хранящимися в `instance.args`. Для удобства в экземпляре исключения определяется `__str__()`, поэтому аргументы могут выводиться напрямую, без ссылки на `.args`. Можно также сначала создать экземпляр исключения перед его возбуждением и добавить к нему любые атрибуты по желанию.

```python
>>> try:
...     raise Exception('spam', 'eggs')
... except Exception as inst:
...     print(type(inst))    # the exception instance
...     print(inst.args)     # arguments stored in .args
...     print(inst)          # __str__ allows args to be printed directly,
...                          # but may be overridden in exception subclasses
...     x, y = inst.args     # unpack args
...     print('x =', x)
...     print('y =', y)
...
<class 'Exception'>
('spam', 'eggs')
('spam', 'eggs')
x = spam
y = eggs
```

Обработчики исключений обрабатывают исключения не только в том случае, если они возникают сразу в `try`, но также и в тех случаях, когда они возникают внутри функций, которые вызываются (даже косвенно) в `try`.

Оператор `raise` позволяет вызвать указанное исключение. Единственный аргумент оператора указывает на возникшее исключение. Это должен быть либо экземпляр исключения, либо класс исключения (класс, производный от `Exception`). Если передан класс исключения, он будет неявно создан путем вызова его конструктора без аргументов.

Поднятое исключение можно распространить

```python
>>> try:
...     raise NameError('HiThere')
... except NameError:
...     print('An exception flew by!')
...     raise
...
An exception flew by!
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: HiThere
```

Оператор `from` позволяет выстраивать цепочки исключений

```python
>>> def func():
...     raise ConnectionError
...
>>> try:
...     func()
... except ConnectionError as exc:
...     raise RuntimeError('Failed to open database') from exc
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "<stdin>", line 2, in func
ConnectionError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
RuntimeError: Failed to open database
```

Цепь исключений можно отключить используя `from None`

```python
>>> try:
...     open('database.sqlite')
>>> except OSError:
...     raise RuntimeError from None

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
RuntimeError
```

Наконец в `try` необязательные действия по очистке, которые должны выполняться при любых обстоятельствах.

```python
>>> try:
...     raise KeyboardInterrupt
... finally:
...     print('Goodbye, world!')
...
Goodbye, world!
KeyboardInterrupt
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
```

Если присутствует `finally`, оно выполняться как последняя задача перед завершением оператора `try`. `finally` выполняется независимо от того, вызывает ли оператор `try` исключение.

Нюансы:

- Если исключение возникает во время выполнения `try`, исключение может быть обработано в `except`. Если исключение не обрабатывается `except`, исключение повторно возникает после выполнения `finally`.
- Исключение может произойти во время выполнения `except` или `else`. Опять же, исключение повторно будет поднято после выполнения `finally`.
- Если `finally` выполняет оператор break, continue или `return`, исключения не возникают повторно.
- Если `try` достигает оператора `break`, `continue` или `return`, то `finally` будет выполняться непосредственно перед выполнением оператора `break`, `continue` или `return`.
- Если `finally` включает оператор `return`, возвращаемое значение будет значением из оператора `return finally`, а не значением из оператора `return try`.

```python
>>> def divide(x, y):
...     try:
...         result = x / y
...     except ZeroDivisionError:
...         print("division by zero!")
...     else:
...         print("result is", result)
...     finally:
...         print("executing finally clause")
...
>>> divide(2, 1)
result is 2.0
executing finally clause
>>> divide(2, 0)
division by zero!
executing finally clause
>>> divide("2", "1")
executing finally clause
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in divide
TypeError: unsupported operand type(s) for /: 'str' and 'str'
```

Основная задача `finally` - закрывать коннекшены и дескрипторы файлов, вне зависимости от эксепшенов.

Кроме всего перечисленного, для исключения можно определять пользовательские классы, наследуясь от стандартных.

- [[python-standart-library]]
- [[trace]]
- [[traceback]]
- [[2022-09-14-daily-note]] custom exception question

[Оригинальная статья в документации](https://docs.python.org/3/tutorial/errors.html)

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[trace]: trace "Trace"
[traceback]: traceback "Traceback"
[2022-09-14-daily-note]: ../posts/2022-09-14-daily-note "Some python tricks 1 - custom exceptions, dataclasses, dot accessing to dict and annotations"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[trace]: trace "Trace"
[traceback]: traceback "Traceback"
[2022-09-14-daily-note]: ../posts/2022-09-14-daily-note "Some python tricks 1 - custom exceptions, dataclasses, dot accessing to dict and annotations"
[//end]: # "Autogenerated link references"