---
description: Нюансы работы со стандартной библиотекой python и связанными пакетами
tags: python-standart-library python
category: list
title: Стандартная библиотека python и полезные ресурсы
---
## Стандартная библиотека

- [[python-glossary]]
- [[python-datamodel]]
- [[python-namespaces]] о пространстве имен в python
- [[python-buildin-functions]]
- [[python-filesystem]] работа с файлами
- [[python-interptetator-and-env-utils]] взаимодействие с интерпретатором и окружением в python
- [[python-decorator]]
- [[python-dataclasses]]
- [[python-descriptors]]
- [[python-iterators-example]]
- [[python-patterns]]
- [[abc]] абстрактные базовые классы
- [[try-except]] про ошибки в python
- [[python-complexity]]
- [[python-super-guide]]
- [os and Path/PurePath equivalent](https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module)

### Support

- [[type-annotation]]
- [[typing]] модуль typing
- [[python-logging]]
- [[argparsing]]
- [[atexit-and-sched]]
- [[regex-examples]]

### Date and time

- [[date-and-time-in-python]]
- [[datetime]]
- [[time]]
- [[calendar]]

### Math and func

- [[mathematic-in-python]]
- [[functools]]
- [[itertools]] смотри так-же [[more-itertools]]
- [[enumerate]]
- [[chainmap]]
- [[counter]]
- [[deque]]
- [[defaultdict]]
- [[ordereddict]]
- [[heapq]]
- [[bisect]]
- [[queue]]
- [ordered-set](https://github.com/rspeer/ordered-set)

### Data

- [[data-storage-python]] pickle, shelve, dbm
- [[archives-in-python]] архивация
- [[python-cryptography]]
- [[python-reading-and-writing-files]]

### Proceses and threads

- [[multiprocess]] процессы в python
- [[threading]] управления параллельными вычислениями
- [[asyncio]]
- [[asyncio-transports-and-protocols]]
- [[contextvars]]

### Apps

- [[email-tools-python]]
- [[nets-with-python]] сети и интернет
- [[urllibparse]]

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
- [[python-import-tools]]
- [[setuptools]]

Смотри так-же [python packaging user guide](https://packaging.python.org/en/latest/)

### Ссылки на статьи

- [Когда использовать List Comprehension в Python](https://webdevblog.ru/kogda-ispolzovat-list-comprehension-v-python/)
- [Списковые включения в примерах](https://codecamp.ru/blog/python-list-comprehensions/)
- [Временная сложность структур python](https://wiki.python.org/moin/TimeComplexity)
- [Yo, I heard you like decorators](https://www.bbayles.com/index/decorator_factory)
- [Асинхронный python без головной боли](https://habr.com/ru/post/667630/)

## Полезные сторонние библиотечки

### Code struction

- [xdot.py](https://github.com/jrfonseca/xdot.py) is an interactive viewer for graphs written in Graphviz's dot language
- [objgraph](https://github.com/mgedmin/objgraph) is a module that lets you visually explore Python object graphs
- [gprof2dot](https://github.com/jrfonseca/gprof2dot) is a Python script to convert the output from many profilers into a dot graph

## Files and objects

- [https://pypdf2.readthedocs.io/en/latest/#](https://pypdf2.readthedocs.io/en/latest/) PyPDF2 is a free and open source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. PyPDF2 can retrieve text and metadata from PDFs as well
- [[more-itertools]]
- [ordered-set](https://github.com/rspeer/ordered-set)
- [[PIL]]
- [natsort](https://github.com/SethMMorton/natsort) Simple yet flexible natural sorting in Python

### REPL and docks

- [Pyodide](https://pyodide.org/en/stable/usage/quickstart.html#try-it-online) in a REPL directly in your browser (no installation needed)
- [bpython](https://github.com/bpython/bpython/) fancy interface to the Python interactive interpreter
- [ptpython](https://github.com/prompt-toolkit/ptpython) is an advanced Python REPL
- [devdocs](https://github.com/freeCodeCamp/devdocs) combines multiple developer documentations in a clean and organized web UI with instant search, offline support, mobile version, dark theme, keyboard shortcuts, and more
- [radon](https://radon.readthedocs.io/en/latest/) is a Python tool which computes various code metrics

### Async

- [AnyIO](https://anyio.readthedocs.io/en/stable/) AnyIO is an asynchronous networking and concurrency library that works on top of either asyncio or trio. It implements trio-like structured concurrency (SC) on top of asyncio, and works in harmony with the native SC of trio itself
- [asyncclick](https://github.com/python-trio/asyncclick) смотри [[click]]
- [asyncer](https://asyncer.tiangolo.com/) is a small library built on top of AnyIO. It has a small number of utility functions that allow working with async, await, and concurrent code in a more convenient way
- [gevent](https://github.com/gevent/gevent) gevent is a coroutine -based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libev or libuv event loop

### Other

- [buildbot](http://docs.buildbot.net/current/index.html#) is a continuous integration framework written in Python
- [Twisted](https://github.com/twisted/twisted) is an event-based framework for internet applications, supporting Python 3.6+
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) Pure python QR Code generator
- [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) is a flexible forms validation and rendering library for Python web development
- [Pipelines](https://returns.readthedocs.io/en/latest/pages/pipeline.html) several tools to make functional programming composition easy, readable, pythonic, and useful
- [dotmap](https://github.com/drgrib/dotmap) Dot access dictionary with dynamic hierarchy creation and ordered iteration
- [[PIL]]
- [[imagehash]]
- [[returns]] Make your functions return something meaningful, typed, and safe!
- [shedule](https://github.com/dbader/schedule) Python job scheduling for humans.

### [[python-public-api]]

## Смотри еще

- [[remove-dict-key-python]]
- [[calling-finction-by-name-python]]
- [[2022-04-26-daily-note]] как заменить запятые на точки в сложных строках, содержащих смешанные цифры и другие знаки
- [[how-to-bump-version-and-changelog-for-python-project]]
- [[2022-11-07-daily-note]] Кастомные классы от python-словаря
- [[2022-12-09-daily-note]] Несколько трюков в python - классы и словари

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-glossary]: ../notes/python-glossary "Python glossary"
[python-datamodel]: python-datamodel "Python datamodel"
[python-namespaces]: ../notes/python-namespaces "Python namespaces"
[python-buildin-functions]: ../notes/python-buildin-functions "Python build-in functions"
[python-filesystem]: ../notes/python-filesystem "Работа с файлами в python"
[python-interptetator-and-env-utils]: ../notes/python-interptetator-and-env-utils "Утилиты взаимодействия с интерпретатором и окружением в python"
[python-decorator]: ../notes/python-decorator "Python decorator"
[python-dataclasses]: ../notes/python-dataclasses "Python dataclasses"
[python-descriptors]: ../notes/python-descriptors "Python descriptors"
[python-iterators-example]: ../notes/python-iterators-example "Python iterators"
[python-patterns]: ../notes/python-patterns "Python patterns programming"
[abc]: ../notes/abc "Abc"
[try-except]: ../notes/try-except "Try except raise"
[python-complexity]: ../notes/python-complexity "Python time complexity"
[python-super-guide]: ../notes/python-super-guide "Python super guide"
[type-annotation]: ../notes/type-annotation "Аннотация типов в python"
[typing]: ../notes/typing "Typing"
[python-logging]: python-logging "Python logging"
[argparsing]: ../notes/argparsing "Arguments parsing in python"
[atexit-and-sched]: ../notes/atexit-and-sched "Atexit и sched"
[regex-examples]: ../notes/regex-examples "Примеры использования модуля re в python"
[date-and-time-in-python]: ../notes/date-and-time-in-python "Date and time in python"
[datetime]: ../notes/datetime "Datetime"
[time]: ../notes/time "Time"
[calendar]: ../notes/calendar "Calendar"
[mathematic-in-python]: ../notes/mathematic-in-python "Mathematic in python"
[functools]: ../notes/functools "Functools"
[itertools]: ../notes/itertools "Itertools"
[more-itertools]: ../notes/more-itertools "More itertools"
[enumerate]: ../notes/enumerate "Enum"
[chainmap]: ../notes/chainmap "ChainMap"
[counter]: ../notes/counter "Counter - счетчик хешируемых объектов"
[deque]: ../notes/deque "Deque - двухсторонние очереди"
[defaultdict]: ../notes/defaultdict "Defaultdict словарь с возвратом значения по умолчанию"
[ordereddict]: ../notes/ordereddict "OrderedDict упорядоченный словарь с опцией сравнения по порядку"
[heapq]: ../notes/heapq "Heapq - двоичная куча"
[bisect]: ../notes/bisect "Bisect - сортирвоанные списки"
[queue]: ../notes/queue "queue"
[data-storage-python]: ../notes/data-storage-python "Pickle, shelve, dbm"
[archives-in-python]: ../notes/archives-in-python "Архивация в python"
[python-cryptography]: ../notes/python-cryptography "Криптография в python"
[python-reading-and-writing-files]: ../notes/python-reading-and-writing-files "Режимы чтения и записи файлов"
[multiprocess]: ../notes/multiprocess "Управление процессами в python"
[threading]: ../notes/threading "Threading"
[asyncio]: ../notes/asyncio "Asyncio"
[asyncio-transports-and-protocols]: ../notes/asyncio-transports-and-protocols "Asyncio transports and protocols"
[contextvars]: ../notes/contextvars "Contextvars"
[email-tools-python]: ../notes/email-tools-python "Email tools in python"
[nets-with-python]: ../notes/nets-with-python "Nets and internet with python"
[urllibparse]: ../notes/urllibparse "Urllib.parse - парсинг урлов в компоненты"
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
[python-import-tools]: ../notes/python-import-tools "Python import tools"
[setuptools]: ../notes/setuptools "Setuptools"
[PIL]: ../notes/PIL "Pillow - обработка изображений"
[click]: ../notes/click "Click интерфейс командной строки"
[imagehash]: ../notes/imagehash "imagehash - хеширование изображений"
[returns]: ../notes/returns "returns"
[python-public-api]: ../notes/python-public-api "Публичные АПИ к сервисам на python"
[remove-dict-key-python]: ../notes/remove-dict-key-python "Как удалить ключ словаря в python"
[calling-finction-by-name-python]: ../notes/calling-finction-by-name-python "Вызов функции по ее строковому имени в python"
[2022-04-26-daily-note]: ../posts/2022-04-26-daily-note "git remote stop tracking and replace comma to dot by re"
[how-to-bump-version-and-changelog-for-python-project]: ../notes/how-to-bump-version-and-changelog-for-python-project "How to bump vershion and changelog for python project"
[2022-11-07-daily-note]: ../posts/2022-11-07-daily-note "Кастомные классы от python-словаря"
[2022-12-09-daily-note]: ../posts/2022-12-09-daily-note "Some python tricks 2 - классы и словари"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[python-glossary]: ../notes/python-glossary "Python glossary"
[python-datamodel]: python-datamodel "Python datamodel"
[python-namespaces]: ../notes/python-namespaces "Python namespaces"
[python-buildin-functions]: ../notes/python-buildin-functions "Python build-in functions"
[python-filesystem]: ../notes/python-filesystem "Работа с файлами в python"
[python-interptetator-and-env-utils]: ../notes/python-interptetator-and-env-utils "Утилиты взаимодействия с интерпретатором и окружением в python"
[python-decorator]: ../notes/python-decorator "Python decorator"
[python-dataclasses]: ../notes/python-dataclasses "Python dataclasses"
[python-descriptors]: ../notes/python-descriptors "Python descriptors"
[python-iterators-example]: ../notes/python-iterators-example "Python iterators"
[python-patterns]: ../notes/python-patterns "Python patterns programming"
[abc]: ../notes/abc "Abc"
[try-except]: ../notes/try-except "Try except raise"
[python-complexity]: ../notes/python-complexity "Python time complexity"
[python-super-guide]: ../notes/python-super-guide "Python super guide"
[type-annotation]: ../notes/type-annotation "Аннотация типов в python"
[typing]: ../notes/typing "Typing"
[python-logging]: python-logging "Python logging"
[argparsing]: ../notes/argparsing "Arguments parsing in python"
[atexit-and-sched]: ../notes/atexit-and-sched "Atexit и sched"
[regex-examples]: ../notes/regex-examples "Примеры использования модуля re в python"
[date-and-time-in-python]: ../notes/date-and-time-in-python "Date and time in python"
[datetime]: ../notes/datetime "Datetime"
[time]: ../notes/time "Time"
[calendar]: ../notes/calendar "Calendar"
[mathematic-in-python]: ../notes/mathematic-in-python "Mathematic in python"
[functools]: ../notes/functools "Functools"
[itertools]: ../notes/itertools "Itertools"
[more-itertools]: ../notes/more-itertools "More itertools"
[enumerate]: ../notes/enumerate "Enum"
[chainmap]: ../notes/chainmap "ChainMap"
[counter]: ../notes/counter "Counter - счетчик хешируемых объектов"
[deque]: ../notes/deque "Deque - двухсторонние очереди"
[defaultdict]: ../notes/defaultdict "Defaultdict словарь с возвратом значения по умолчанию"
[ordereddict]: ../notes/ordereddict "OrderedDict упорядоченный словарь с опцией сравнения по порядку"
[heapq]: ../notes/heapq "Heapq - двоичная куча"
[bisect]: ../notes/bisect "Bisect - сортирвоанные списки"
[queue]: ../notes/queue "queue"
[data-storage-python]: ../notes/data-storage-python "Pickle, shelve, dbm"
[archives-in-python]: ../notes/archives-in-python "Архивация в python"
[python-cryptography]: ../notes/python-cryptography "Криптография в python"
[python-reading-and-writing-files]: ../notes/python-reading-and-writing-files "Режимы чтения и записи файлов"
[multiprocess]: ../notes/multiprocess "Управление процессами в python"
[threading]: ../notes/threading "Threading"
[asyncio]: ../notes/asyncio "Asyncio"
[asyncio-transports-and-protocols]: ../notes/asyncio-transports-and-protocols "Asyncio transports and protocols"
[contextvars]: ../notes/contextvars "Contextvars"
[email-tools-python]: ../notes/email-tools-python "Email tools in python"
[nets-with-python]: ../notes/nets-with-python "Nets and internet with python"
[urllibparse]: ../notes/urllibparse "Urllib.parse - парсинг урлов в компоненты"
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
[python-import-tools]: ../notes/python-import-tools "Python import tools"
[setuptools]: ../notes/setuptools "Setuptools"
[more-itertools]: ../notes/more-itertools "More itertools"
[PIL]: ../notes/PIL "Pillow - обработка изображений"
[click]: ../notes/click "Click интерфейс командной строки"
[PIL]: ../notes/PIL "Pillow - обработка изображений"
[imagehash]: ../notes/imagehash "imagehash - хеширование изображений"
[returns]: ../notes/returns "returns"
[python-public-api]: ../notes/python-public-api "Публичные АПИ к сервисам на python"
[remove-dict-key-python]: ../notes/remove-dict-key-python "Как удалить ключ словаря в python"
[calling-finction-by-name-python]: ../notes/calling-finction-by-name-python "Вызов функции по ее строковому имени в python"
[2022-04-26-daily-note]: ../posts/2022-04-26-daily-note "git remote stop tracking and replace comma to dot by re"
[how-to-bump-version-and-changelog-for-python-project]: ../notes/how-to-bump-version-and-changelog-for-python-project "How to bump vershion and changelog for python project"
[2022-11-07-daily-note]: ../posts/2022-11-07-daily-note "Кастомные классы от python-словаря"
[2022-12-09-daily-note]: ../posts/2022-12-09-daily-note "Some python tricks 2 - классы и словари"
[//end]: # "Autogenerated link references"