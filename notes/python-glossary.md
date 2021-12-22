---
description: Некоторые сложные термины и понятия в python
tags: python-standart-library
---
# Python glossary

В этой заметке небольшая подборка терминов, которые мне кажутся сложными и которые легче запомнить, описав своими словами со ссылками на источники.

## abstract base class

Абстрактные базовые классы дополняют утиную типизацию, предоставляя способ определения интерфейсов, когда другие методы, такие как `hasattr()`, были бы негромоздкими. ABC вводят виртуальные подклассы, которые не наследуются от класса, но по-прежнему распознаются `isinstance()` и `issubclass()`. Python имеет множество встроенных ABC, от которых можно отнаследоваться:

- структуры данных в модуле `collection.abc`
- числа в `numeric`
- потоки в модуле `io` см. [[python-filesystem]]
- средства поиска и загрузчиков импорта `importlib.abc`
- ряд модулей реализуют свои собственные абстрактные классы для ряда задач, к примеру [[asyncio]] и [[threading]]

Можно создавать свои собственные абстрактные классы с помощью модуля `abc`

Смотри подробнее [[abc]]

## bytecode

Исходный код Python компилируется в байт-код, внутреннее представление программы Python в интерпретаторе CPython. Байт-код также кэшируется в файлах `.pyc`, поэтому второй раз выполнение того же файла происходит быстрее (можно избежать перекомпиляции из исходного кода в байт-код). Виртуальная машина python выполняет машинный код, соответствующий байт-коду. Не ожидается, что байт-коды будут работать между разными виртуальными машинами Python или будут стабильными между выпусками Python. Список инструкций по байт-коду можно найти в документации к модулю [dis](https://docs.python.org/3/library/dis.html#python-bytecode-instructions).

## callback

Функция-подпрограмма, которая передается другой функции в качестве аргумента для выполнения в будущем. Довольно часто используется, к примеру, в [[asyncio]]

## class

- **переменная класса** определяется на уровне класса и не предназначена для изменения на уровне экземпляра

## context variable

Переменная, которая может иметь разные значения в зависимости от контекста. Это похоже на локальное хранилище потока, в котором каждый поток выполнения может иметь разные значения переменной. Однако с переменными контекста может быть несколько контекстов в одном потоке выполнения, и основное использование переменных контекста - отслеживать переменные в параллельных асинхронных задачах. [Contextvars](https://docs.python.org/3/library/contextvars.html#module-contextvars). [[contextvars]]

## descriptor

Любой объект, который определяет методы `__get__()`, `__set__()` или `__delete__()`. Когда атрибут класса является дескриптором, его особое поведение привязки запускается при поиске атрибута. Обычно при использовании a.b для получения, установки или удаления атрибута выполняется поиск объекта с именем b в словаре классов для a, но если b является дескриптором, вызывается соответствующий метод дескриптора. Подробнее читай тут [[python-descriptors]]

[Глоссарий в документации python](https://docs.python.org/3/glossary.html#glossary)

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[python-filesystem]: python-filesystem "Работа с файлами"
[asyncio]: asyncio "Asyncio"
[threading]: threading "Threading"
[abc]: abc "Abc"
[asyncio]: asyncio "Asyncio"
[contextvars]: contextvars "Contextvars"
[python-descriptors]: python-descriptors "Python descriptors"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"