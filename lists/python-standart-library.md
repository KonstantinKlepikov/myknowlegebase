---
description: Нюансы работы со стандартной библиотекой python и связанными пакетами
tags: python-standart-library python
category: list
title: Стандартная библиотека python и полезные ресурсы
---
## Стандартная библиотека

- [[notes/python-glossary]]
- [[lists/python-datamodel]]
- [[notes/python-namespaces]] о пространстве имен в python
- [[notes/python-buildin-functions]]
- [[notes/python-filesystem]] работа с файлами
- [[notes/python-interptetator-and-env-utils]] взаимодействие с интерпретатором и окружением в python
- [[notes/python-decorator]]
- [[notes/python-dataclasses]]
- [[notes/python-descriptors]]
- [[notes/python-iterators-example]]
- [[notes/python-patterns]]
- [[notes/abc]] абстрактные базовые классы
- [[notes/try-except]] про ошибки в python
- [[notes/python-complexity]]
- [[notes/python-super-guide]]
- [os and Path/PurePath equivalent](https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module)

### Support

- [[notes/type-annotation]]
- [[notes/typing]] модуль typing
- [[lists/python-logging]]
- [[notes/argparsing]]
- [[notes/atexit-and-sched]]
- [[notes/regex-examples]]

### Date and time

- [[notes/date-and-time-in-python]]
- [[notes/datetime]]
- [[notes/time]]
- [[notes/calendar]]
- [Generate list of months between interval](https://stackoverflow.com/a/65776598/15966204)
- [Creating a range of dates in Python](https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python)
- [RFC 1123 Date Representation in Python](https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python)

### Math and func

- [[notes/mathematic-in-python]]
- [[notes/functools]]
- [[notes/itertools]] смотри так-же [[notes/more-itertools]]
- [[notes/enumerate]]
- [[notes/chainmap]]
- [[notes/counter]]
- [[notes/deque]]
- [[notes/defaultdict]]
- [[notes/ordereddict]]
- [[notes/heapq]]
- [[notes/bisect]]
- [[notes/queue]]
- [ordered-set](https://github.com/rspeer/ordered-set)

### Data

- [[notes/data-storage-python]] pickle, shelve, dbm
- [[notes/archives-in-python]] архивация
- [[notes/python-cryptography]]
- [[notes/python-reading-and-writing-files]]
- [Python in-memory zip library](https://stackoverflow.com/questions/2463770/python-in-memory-zip-library)

### Proceses and threads

- [[notes/multiprocess]] процессы в python
- [[notes/threading]] управления параллельными вычислениями
- [[notes/asyncio]]
- [[notes/asyncio-transports-and-protocols]]
- [[notes/contextvars]]

### Apps

- [[notes/email-tools-python]]
- [[notes/nets-with-python]] сети и интернет
- [[notes/urllibparse]]

### Development tools

- [[notes/pydoc]]
- [[notes/doctest]]
- [[notes/unittest]]
- [[notes/trace]]
- [[notes/traceback]]
- [[notes/cgitb]]
- [[notes/inspect]]
- [[notes/profile]]
- [[notes/timeit]]
- [[notes/pdb-python-debugger]]
- [tabnanni](https://docs.python.org/3/library/tabnanny.html?highlight=tabnanny#module-tabnanny) проверка неоднозначного использования пробелов (смотри еще [[notes/flake8]])
- [compileall](https://docs.python.org/3/library/compileall.html?highlight=compileall#module-compileall) поиск и компиляция файлов в `.pyc`
- [pyclbr](https://docs.python.org/3/library/pyclbr.html?highlight=pyclbr#module-pyclbr) предоставляет ограниченную информацию о функциях, классах и методах, определенных в модуле, написанном на Python. Информации достаточно для реализации обозревателя модулей. Информация извлекается из исходного кода, а не путем импорта модуля, поэтому этот модуль безопасно использовать с ненадежным кодом. Это ограничение делает невозможным использование этого модуля с модулями, не реализованными в Python, включая все стандартные и дополнительные расширения.
- [[notes/venv]]
- [[notes/warnings]]
- [[notes/dis]]
- [[notes/python-import-tools]]
- [[notes/setuptools]]

Смотри так-же [python packaging user guide](https://packaging.python.org/en/latest/)

### Ссылки на статьи

- [Когда использовать List Comprehension в Python](https://webdevblog.ru/kogda-ispolzovat-list-comprehension-v-python/)
- [Списковые включения в примерах](https://codecamp.ru/blog/python-list-comprehensions/)
- [Временная сложность структур python](https://wiki.python.org/moin/TimeComplexity)
- [Yo, I heard you like decorators](https://www.bbayles.com/index/decorator_factory)
- [Асинхронный python без головной боли](https://habr.com/ru/post/667630/)
- 19 способов сделать сокет-сервер на Python. Эволюционный подход. [Часть 1. Введение](https://habr.com/ru/articles/676110/), [Часть 2. Блокирующие сокеты и многозадачность](https://habr.com/ru/articles/676118/), [Часть 3. Первый подход к асинхронности](https://habr.com/ru/articles/676124/)

## Книги и руководства

- [Python Design Patterns](https://python-patterns.guide/)

## Полезные сторонние библиотечки

### Code struction

- [xdot.py](https://github.com/jrfonseca/xdot.py) is an interactive viewer for graphs written in Graphviz's dot language
- [objgraph](https://github.com/mgedmin/objgraph) is a module that lets you visually explore Python object graphs
- [gprof2dot](https://github.com/jrfonseca/gprof2dot) is a Python script to convert the output from many profilers into a dot graph
- [Python to PlantUML](https://pypi.org/project/py2puml/) Generate PlantUML class diagrams to document your Python application

## Files and objects

- [https://pypdf2.readthedocs.io/en/latest/#](https://pypdf2.readthedocs.io/en/latest/) PyPDF2 is a free and open source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. PyPDF2 can retrieve text and metadata from PDFs as well
- [[notes/more-itertools]]
- [ordered-set](https://github.com/rspeer/ordered-set)
- [[notes/PIL]]
- [natsort](https://github.com/SethMMorton/natsort) Simple yet flexible natural sorting in Python
- [[notes/imagehash]]

### REPL and docks

- [Pyodide](https://pyodide.org/en/stable/usage/quickstart.html#try-it-online) in a REPL directly in your browser (no installation needed)
- [bpython](https://github.com/bpython/bpython/) fancy interface to the Python interactive interpreter
- [ptpython](https://github.com/prompt-toolkit/ptpython) is an advanced Python REPL
- [devdocs](https://github.com/freeCodeCamp/devdocs) combines multiple developer documentations in a clean and organized web UI with instant search, offline support, mobile version, dark theme, keyboard shortcuts, and more
- [radon](https://radon.readthedocs.io/en/latest/) is a Python tool which computes various code metrics

### Async

- [AnyIO](https://anyio.readthedocs.io/en/stable/) AnyIO is an asynchronous networking and concurrency library that works on top of either asyncio or trio. It implements trio-like structured concurrency (SC) on top of asyncio, and works in harmony with the native SC of trio itself
- [asyncclick](https://github.com/python-trio/asyncclick) смотри [[notes/click]]
- [asyncer](https://asyncer.tiangolo.com/) is a small library built on top of AnyIO. It has a small number of utility functions that allow working with async, await, and concurrent code in a more convenient way
- [gevent](https://github.com/gevent/gevent) gevent is a coroutine -based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libev or libuv event loop
- [[notes/async_property]]
- [[notes/async-lru]]

### Profiling

- [memray](https://github.com/bloomberg/memray) is a memory profiler for Python. It can track memory allocations in Python code, in native extension modules, and in the Python interpreter itself. It can generate several different types of reports to help you analyze the captured memory usage data. While commonly used as a CLI tool, it can also be used as a library to perform more fine-grained profiling tasks.

### Other

- [buildbot](http://docs.buildbot.net/current/index.html#) is a continuous integration framework written in Python
- [Twisted](https://github.com/twisted/twisted) is an event-based framework for internet applications, supporting Python 3.6+
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) Pure python QR Code generator
- [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) is a flexible forms validation and rendering library for Python web development
- [Pipelines](https://returns.readthedocs.io/en/latest/pages/pipeline.html) several tools to make functional programming composition easy, readable, pythonic, and useful
- [dotmap](https://github.com/drgrib/dotmap) Dot access dictionary with dynamic hierarchy creation and ordered iteration
- [[notes/returns]] Make your functions return something meaningful, typed, and safe!
- [shedule](https://github.com/dbader/schedule) Python job scheduling for humans.
- [[notes/blinker]]
- [[notes/dependency-injection]]
- [ruff](https://astral.sh/blog/ruff-v0.4.0) extremely fast Python linter and formatter, written in [[lists/rust]]
- [Advanced Python Scheduler](https://apscheduler.readthedocs.io/en/master/index.html#)
- [Testcontainers Python](https://github.com/testcontainers/testcontainers-python) facilitates the use of Docker containers for functional and integration testing

### [[notes/python-public-api]]

## Смотри еще

- [[notes/remove-dict-key-python]]
- [[notes/calling-finction-by-name-python]]
- [[2022-04-26-daily-note]] как заменить запятые на точки в сложных строках, содержащих смешанные цифры и другие знаки
- [[notes/how-to-bump-version-and-changelog-for-python-project]]
- [[2022-11-07-daily-note]] Кастомные классы от python-словаря
- [[2022-12-09-daily-note]] Несколько трюков в python - классы и словари

[notes/python-glossary]: ../notes/python-glossary "Python glossary"
[lists/python-datamodel]: python-datamodel "Python datamodel"
[notes/python-namespaces]: ../notes/python-namespaces "Python namespaces"
[notes/python-buildin-functions]: ../notes/python-buildin-functions "Python build-in functions"
[notes/python-filesystem]: ../notes/python-filesystem "Работа с файлами в python"
[notes/python-interptetator-and-env-utils]: ../notes/python-interptetator-and-env-utils "Утилиты взаимодействия с интерпретатором и окружением в python"
[notes/python-decorator]: ../notes/python-decorator "Python decorator"
[notes/python-dataclasses]: ../notes/python-dataclasses "Python dataclasses"
[notes/python-descriptors]: ../notes/python-descriptors "Python descriptors"
[notes/python-iterators-example]: ../notes/python-iterators-example "Python iterators"
[notes/python-patterns]: ../notes/python-patterns "Python patterns programming"
[notes/abc]: ../notes/abc "Abc"
[notes/try-except]: ../notes/try-except "Try except raise"
[notes/python-complexity]: ../notes/python-complexity "Python time complexity"
[notes/python-super-guide]: ../notes/python-super-guide "Python super guide"
[notes/type-annotation]: ../notes/type-annotation "Аннотация типов в python"
[notes/typing]: ../notes/typing "Typing"
[lists/python-logging]: python-logging "Python logging"
[notes/argparsing]: ../notes/argparsing "Arguments parsing in python"
[notes/atexit-and-sched]: ../notes/atexit-and-sched "Atexit и sched"
[notes/regex-examples]: ../notes/regex-examples "Примеры использования модуля re в python"
[notes/date-and-time-in-python]: ../notes/date-and-time-in-python "Date and time in python"
[notes/datetime]: ../notes/datetime "Datetime"
[notes/time]: ../notes/time "Time"
[notes/calendar]: ../notes/calendar "Calendar"
[notes/mathematic-in-python]: ../notes/mathematic-in-python "Mathematic in python"
[notes/functools]: ../notes/functools "Functools"
[notes/itertools]: ../notes/itertools "Itertools"
[notes/more-itertools]: ../notes/more-itertools "More itertools"
[notes/enumerate]: ../notes/enumerate "Enum"
[notes/chainmap]: ../notes/chainmap "ChainMap"
[notes/counter]: ../notes/counter "Counter - счетчик хешируемых объектов"
[notes/deque]: ../notes/deque "Deque - двухсторонние очереди"
[notes/defaultdict]: ../notes/defaultdict "Defaultdict словарь с возвратом значения по умолчанию"
[notes/ordereddict]: ../notes/ordereddict "OrderedDict упорядоченный словарь с опцией сравнения по порядку"
[notes/heapq]: ../notes/heapq "Heapq - двоичная куча"
[notes/bisect]: ../notes/bisect "Bisect - сортирвоанные списки"
[notes/queue]: ../notes/queue "queue"
[notes/data-storage-python]: ../notes/data-storage-python "Pickle, shelve, dbm"
[notes/archives-in-python]: ../notes/archives-in-python "Архивация в python"
[notes/python-cryptography]: ../notes/python-cryptography "Криптография в python"
[notes/python-reading-and-writing-files]: ../notes/python-reading-and-writing-files "Режимы чтения и записи файлов"
[notes/multiprocess]: ../notes/multiprocess "Управление процессами в python"
[notes/threading]: ../notes/threading "Threading"
[notes/asyncio]: ../notes/asyncio "Asyncio"
[notes/asyncio-transports-and-protocols]: ../notes/asyncio-transports-and-protocols "Asyncio transports and protocols"
[notes/contextvars]: ../notes/contextvars "Contextvars"
[notes/email-tools-python]: ../notes/email-tools-python "Email tools in python"
[notes/nets-with-python]: ../notes/nets-with-python "Nets and internet with python"
[notes/urllibparse]: ../notes/urllibparse "Urllib.parse - парсинг урлов в компоненты"
[notes/pydoc]: ../notes/pydoc "Pydoc"
[notes/doctest]: ../notes/doctest "Doctest"
[notes/unittest]: ../notes/unittest "Unittest"
[notes/trace]: ../notes/trace "Trace"
[notes/traceback]: ../notes/traceback "Traceback"
[notes/cgitb]: ../notes/cgitb "Cgitb"
[notes/inspect]: ../notes/inspect "Inspect"
[notes/profile]: ../notes/profile "Profile"
[notes/timeit]: ../notes/timeit "Timeit"
[notes/pdb-python-debugger]: ../notes/pdb-python-debugger "Pdb python debugger"
[notes/flake8]: ../notes/flake8 "Flake8"
[notes/venv]: ../notes/venv "Venv"
[notes/warnings]: ../notes/warnings "Warnings"
[notes/dis]: ../notes/dis "Dis"
[notes/python-import-tools]: ../notes/python-import-tools "Python import tools"
[notes/setuptools]: ../notes/setuptools "Setuptools"
[notes/PIL]: ../notes/PIL "Pillow - обработка изображений"
[notes/imagehash]: ../notes/imagehash "imagehash - хеширование изображений"
[notes/click]: ../notes/click "Click интерфейс командной строки"
[notes/async_property]: ../notes/async_property "async_property"
[notes/async-lru]: ../notes/async-lru "async-lru"
[notes/returns]: ../notes/returns "returns"
[notes/blinker]: ../notes/blinker "blinker сигналы в python"
[notes/dependency-injection]: ../notes/dependency-injection "Dependency injection"
[lists/rust]: rust "Ресурсы по языку программирования Rust"
[notes/python-public-api]: ../notes/python-public-api "Публичные АПИ к сервисам на python"
[notes/remove-dict-key-python]: ../notes/remove-dict-key-python "Как удалить ключ словаря в python"
[notes/calling-finction-by-name-python]: ../notes/calling-finction-by-name-python "Вызов функции по ее строковому имени в python"
[2022-04-26-daily-note]: ../posts/2022-04-26-daily-note "git remote stop tracking and replace comma to dot by re"
[notes/how-to-bump-version-and-changelog-for-python-project]: ../notes/how-to-bump-version-and-changelog-for-python-project "How to bump vershion and changelog for python project"
[2022-11-07-daily-note]: ../posts/2022-11-07-daily-note "Кастомные классы от python-словаря"
[2022-12-09-daily-note]: ../posts/2022-12-09-daily-note "Some python tricks 2 - классы и словари"
