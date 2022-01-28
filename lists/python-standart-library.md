---
description: Нюансы работы со стандартной библиотекой в python
tags: python-standart-library
category: list
---
# Стандартная библиотека python и полезные ресурсы

## Стандартная библиотека

- [[python-glossary]]
- [[python-datamodel]]
- [[python-namespaces]] о пространстве имен в python
- [[python-filesystem]] работа с файлами
- [[python-interptetator-and-env-utils]] взаимодействие с интерпретатором и окружением в python
- [[python-decorator]]
- [[python-descriptors]]
- [[python-patterns]]
- [[abc]] абстрактные базовые классы
- [[try-except]] про ошибки в python

### Support

- [[type-annotation]]
- [[typing]] модуль typing
- [[python-logging]]
- [[argparsing]]
- [[atexit-and-sched]]

### Date and time

- [[date-and-time-in-python]]
- [[datetime]]
- [[time]]
- [[calendar]]

### Math and func

- [[mathematic-in-python]]
- [[functools]]
- [[itertools]]
- [[enumerate]]
- [[chainmap]]
- [[counter]]
- [[deque]]
- [[defaultdict]]
- [[ordereddict]]
- [[heapq]]
- [[bisect]]
- [[queue]]

### Data

- [[data-storage-python]] pickle, shelve, dbm
- [[archives-in-python]] архивация
- [[python-cryptography]]

### Proceses and threads

- [[multiprocess]] процессы в python
- [[threading]] управления параллельными вычислениями
- [[asyncio]]
- [[asyncio-transports-and-protocols]]
- [[contextvars]]

### Apps

- [[email-tools-python]]
- [[nets-with-python]] сети и интернет

### Development tools

- [[pydoc]]
- [[doctest]]
- [[unittest]]
- [[trace]]
- [[traceback]]
- [[cgitb]]
- [[inspect]]
- [[profile]]
- [[timeit]]
- [[pdb-python-debugger]]
- [tabnanni](https://docs.python.org/3/library/tabnanny.html?highlight=tabnanny#module-tabnanny) проверка неоднозначного использования пробелов (смотри еще [[flake8]])
- [compileall](https://docs.python.org/3/library/compileall.html?highlight=compileall#module-compileall) поиск и компиляция файлов в `.pyc`
- [pyclbr](https://docs.python.org/3/library/pyclbr.html?highlight=pyclbr#module-pyclbr) предоставляет ограниченную информацию о функциях, классах и методах, определенных в модуле, написанном на Python. Информации достаточно для реализации обозревателя модулей. Информация извлекается из исходного кода, а не путем импорта модуля, поэтому этот модуль безопасно использовать с ненадежным кодом. Это ограничение делает невозможным использование этого модуля с модулями, не реализованными в Python, включая все стандартные и дополнительные расширения.
- [[venv]]
- [[warnings]]
- [[dis]]

Смотри так-же [python packaging user guide](https://packaging.python.org/en/latest/)

### Ссылки на статьи

- [Когда использовать List Comprehension в Python](https://webdevblog.ru/kogda-ispolzovat-list-comprehension-v-python/)
- [Списковые включения в примерах](https://codecamp.ru/blog/python-list-comprehensions/)
- [Временная сложность структур python](https://wiki.python.org/moin/TimeComplexity)
- [Yo, I heard you like decorators](https://www.bbayles.com/index/decorator_factory)

## Полезные сторонние библиотечки

- [Pipelines](https://returns.readthedocs.io/en/latest/pages/pipeline.html) several tools to make functional programming composition easy, readable, pythonic, and useful
- [xdot.py](https://github.com/jrfonseca/xdot.py) is an interactive viewer for graphs written in Graphviz's dot language
- [objgraph](https://github.com/mgedmin/objgraph) is a module that lets you visually explore Python object graphs
- [gprof2dot](https://github.com/jrfonseca/gprof2dot) is a Python script to convert the output from many profilers into a dot graph
- [AnyIO](https://anyio.readthedocs.io/en/stable/) AnyIO is an asynchronous networking and concurrency library that works on top of either asyncio or trio. It implements trio-like structured concurrency (SC) on top of asyncio, and works in harmony with the native SC of trio itself
- [Pyodide](https://pyodide.org/en/stable/usage/quickstart.html#try-it-online) in a REPL directly in your browser (no installation needed)
- [bpython](https://github.com/bpython/bpython/) fancy interface to the Python interactive interpreter
- [ptpython](https://github.com/prompt-toolkit/ptpython) is an advanced Python REPL
- [devdocs](https://github.com/freeCodeCamp/devdocs) combines multiple developer documentations in a clean and organized web UI with instant search, offline support, mobile version, dark theme, keyboard shortcuts, and more
- [radon](https://radon.readthedocs.io/en/latest/) is a Python tool which computes various code metrics
- [buildbot](http://docs.buildbot.net/current/index.html#) is a continuous integration framework written in Python
- [Twisted](https://github.com/twisted/twisted) is an event-based framework for internet applications, supporting Python 3.6+
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) Pure python QR Code generator
- [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) is a flexible forms validation and rendering library for Python web development

## Смотри еще

- [[remove-dict-key-python]]
- [[calling-finction-by-name-python]]
- [[creation-of-list-matrix]]
- [[full-path-to-current-directory]]
- [[convert-dcit-to-dataclass]]
- [[from-future-import-annotations]]
- [[python-sorting]]
- [[2021-12-20-daily-note]] про приоритет операторов при сравнении, порядок импорта модулей и пактов, и пара нюансов со встроенными функциями
- [[2021-12-21-daily-note]] про форматирование f-строк
- [[2021-12-26-daily-note]] парсинг csv, html, работа с pandas
- [[numpy]]
- [[pandas]]
- [[feedparser]]
- [[fastapi]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-glossary]: ../notes/python-glossary "Python glossary"
[python-datamodel]: python-datamodel "Python datamodel"
[python-namespaces]: ../notes/python-namespaces "Python namespaces"
[python-filesystem]: ../notes/python-filesystem "Работа с файлами"
[python-interptetator-and-env-utils]: ../notes/python-interptetator-and-env-utils "Утилиты взаимодействия с интерпретатором и окружением в python"
[python-decorator]: ../notes/python-decorator "Python decorator"
[python-descriptors]: ../notes/python-descriptors "Python descriptors"
[python-patterns]: ../notes/python-patterns "Python patterns"
[abc]: ../notes/abc "Abc"
[try-except]: ../notes/try-except "Try-except-raise"
[type-annotation]: ../notes/type-annotation "Анотация типов в python"
[typing]: ../notes/typing "Typing"
[python-logging]: python-logging "Python logging"
[argparsing]: ../notes/argparsing "Arguments parsing in python"
[atexit-and-sched]: ../notes/atexit-and-sched "Atexit и sched"
[date-and-time-in-python]: ../notes/date-and-time-in-python "Date and time in python"
[datetime]: ../notes/datetime "Datetime"
[time]: ../notes/time "Time"
[calendar]: ../notes/calendar "Calendar"
[mathematic-in-python]: ../notes/mathematic-in-python "Mathematic in python"
[functools]: ../notes/functools "Functools"
[itertools]: ../notes/itertools "Itertools"
[enumerate]: ../notes/enumerate "Enum"
[chainmap]: ../notes/chainmap "ChainMap"
[counter]: ../notes/counter "Counter - счетчик хешируемых объектов"
[deque]: ../notes/deque "Deque - двухсторонние очереди"
[defaultdict]: ../notes/defaultdict "Defaultdict словарь с возвратом значения по умолчанию"
[ordereddict]: ../notes/ordereddict "OrderedDict упорядоченный словарь с опцией сравнения по порядку"
[heapq]: ../notes/heapq "Heapq - двоичная куча"
[bisect]: ../notes/bisect "Bisect - сортирвоанные списки"
[queue]: ../notes/queue "Queue - очереди и стеки"
[data-storage-python]: ../notes/data-storage-python "Pickle, shelve, dbm"
[archives-in-python]: ../notes/archives-in-python "Архивация в python"
[python-cryptography]: ../notes/python-cryptography "Криптография в python"
[multiprocess]: ../notes/multiprocess "Управление процессами в python"
[threading]: ../notes/threading "Threading"
[asyncio]: ../notes/asyncio "Asyncio"
[asyncio-transports-and-protocols]: ../notes/asyncio-transports-and-protocols "Asyncio transports and protocols"
[contextvars]: ../notes/contextvars "Contextvars"
[email-tools-python]: ../notes/email-tools-python "Email tools in python"
[nets-with-python]: ../notes/nets-with-python "Nets and internet with python"
[pydoc]: ../notes/pydoc "Pydoc"
[doctest]: ../notes/doctest "Doctest"
[unittest]: ../notes/unittest "Unittest"
[trace]: ../notes/trace "Trace"
[traceback]: ../notes/traceback "Traceback"
[cgitb]: ../notes/cgitb "Cgitb"
[inspect]: ../notes/inspect "Inspect"
[profile]: ../notes/profile "Profile"
[timeit]: ../notes/timeit "Timeit"
[pdb-python-debugger]: ../notes/pdb-python-debugger "Pdb python debugger"
[flake8]: ../notes/flake8 "Flake8"
[venv]: ../notes/venv "Venv"
[warnings]: ../notes/warnings "Warnings"
[dis]: ../notes/dis "Dis"
[remove-dict-key-python]: ../notes/remove-dict-key-python "Как удалить ключ словаря в python"
[calling-finction-by-name-python]: ../notes/calling-finction-by-name-python "Вызов функции по ее строковому имени в python"
[creation-of-list-matrix]: ../notes/creation-of-list-matrix "Creation of list matrix"
[full-path-to-current-directory]: full-path-to-current-directory "Full path to current directory"
[convert-dcit-to-dataclass]: ../notes/convert-dcit-to-dataclass "Convert dict to dataclass or namedtuple"
[from-future-import-annotations]: ../notes/from-future-import-annotations "From future import annotations"
[python-sorting]: ../notes/python-sorting "Python sorting"
[2021-12-20-daily-note]: ../posts/2021-12-20-daily-note "Операторы сравнения, запуск модуля с аругментами и др.тонкости python"
[2021-12-21-daily-note]: ../posts/2021-12-21-daily-note "Formatted string literals specificators"
[2021-12-26-daily-note]: ../posts/2021-12-26-daily-note "Немного трюков с python: работа с csv, парсинг html и другое"
[numpy]: ../notes/numpy "Numpy"
[pandas]: ../notes/pandas "Pandas"
[feedparser]: ../notes/feedparser "Feedparser - rss и atom парсинг"
[fastapi]: ../notes/fastapi "Fastapi"
[//end]: # "Autogenerated link references"