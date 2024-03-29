---
description: Инструменты импорта в python
tags: python-standart-library python
title: Python import tools
---
[importlib](https://docs.python.org/3/library/importlib.html) базовая реализация механизма импорта стандарптной библиотеки. Можно использовать для динамического импорта модулей в процессе выполнения кода (для случаев, когда заранее не известно имя импортируемого модуля), в отличие от `import`, который импортирует модуль при загрузке приложения

Назначение пакета importlib двоякое. Один из них — обеспечить реализацию оператора импорта (и, соответственно, функции `__import__()`) в исходном коде Python. Это обеспечивает реализацию импорта, переносимую на любой интерпретатор Python. Во-вторых, в этом пакете представлены компоненты для реализации собственных настраиваемых объектов (обычно известных как средство импорта) для участия в процессе импорта.

Модуль предоставляет высокоуровневый и низкоуровневый (доступ к загрузчикам) АПИ импорта

[pkgutil](https://docs.python.org/3/library/pkgutil.html?highlight=pkgutil#module-pkgutil) позволяет изменять правила импорта пакетов python и загружать ресурсы, не являющиеся кодом, распространяемых в составе пакетов

[zipimport](https://docs.python.org/3/library/zipimport.html?highlight=zipimport#module-zipimport) предоставляет инструменты загрузки python-кода из zip-архивов

Смотри еще:

- [[python-standart-library]]
- [[setuptools]]
- [[archives-in-python]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[setuptools]: setuptools "Setuptools"
[archives-in-python]: archives-in-python "Архивация в python"
[//end]: # "Autogenerated link references"