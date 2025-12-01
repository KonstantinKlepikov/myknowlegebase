---
description: Генерация справки в runtime встроенными средствами python
tags: python-standart-library python
title: Pydoc
---
Через командную строку так: `pytdoc <modulename>`

В формате html: `pytdoc -w <modulename>`

После этого формируется файл в текущем каталоге, после чего можно запустить сервер с докой: `pydoc -p 5000`

Кроме этого, модуль зобавляет в `__builtins__` функцию `help()` передав которой навзание модуля можно получить информацию в интерактивной облочке

Смотри еще:

- [докумсентация](https://docs.python.org/3/library/pydoc.html)
- [[python-standart-library]]


[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
