---
description: Click - командная строка в python
---
# Click интерфейс командной строки

```shell
pip install click
```

## Базовая концепция

Клик базируется на декларации команд через декораторы. Функция становится инструментом командной строки, когда снабжена декоратором `@click.command()`

```python
import click

@click.command()
def hello():
    click.echo('Hello World!')

if __name__ == '__main__':
    hello()
```

`@click.eshoe()` используется вместо стандартного `print()` для поддержки разных окружений, чтобы не сломать реализацию, если конфигурация нарушена.

Поддерживаются вложенные команды через декоратор `@click.group()`

```python
@click.group()
def cli():
    pass

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.command()
def dropdb():
    click.echo('Dropped the database')

cli.add_command(initdb)
cli.add_command(dropdb)
```

или для простых скриптов

```python
@click.group()
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')

if __name__ == '__main__':
    cli()
```

Так-же команды могут регистрироваться в группы позже

```python
@click.command()
def greet():
    click.echo("Hello, World!")

@click.group()
def group():
    pass

group.add_command(greet)
```

Добавление аргументов и опций производится через `@click.option()` и `@click.argument()`

```python
@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo(f"Hello {name}!")
```

```bash
$ python hello.py --help
Usage: hello.py [OPTIONS] NAME

Options:
  --count INTEGER  number of greetings
  --help           Show this message and exit.
```

## Поддержка интеграции с [[setuptools]]

[Читай доку](https://click.palletsprojects.com/en/8.0.x/setuptools/)

## Параметры

Доступны два типа параметров - опции и аргументы. Рекомендуется использовать аргументы исключительно для таких вещей, как переход к подкомандам или ввод имен файлов/URL-адресов, а опции использовать для всего остального.

Для опций доступно:

- автоматическое дополнение для пропущенных опций
- булевы значения
- опции могут быть добавлены из переменных окружения (аругменты нет)
- опции полностью задокументированы и будут отображены с вызовом `--help` флага

Типы параметров определены в самом click. [Смотри доки](https://click.palletsprojects.com/en/8.0.x/parameters/#parameter-types). Кроме того, можно [задать кастомные типы параметров](https://click.palletsprojects.com/en/8.0.x/parameters/#implementing-custom-types)

## Опции

Имена опций могут быть использованы как аргументы при вызове декорированной функции. Порядок выбора имен:

- если имя не имеет префикса, оно используется как имя аргумента и не используется как имя опции в командной строке
- если хотя бы одно имя снабжено двойными черточками - первое из таких используется как имя опции
- в остальных случаях используется первое имя с одинарной черточкой

При ээтом большие буквы конвертятся в маленькие, а избыточные черточки игнорируются:

- "-f", "--foo-bar", the name is `foo_bar`
- "-x", the name is `x`
- "-f", "--filename", "dest", the name is `dest`
- "--CamelCase", the name is `camelcase`
- "-f", "-fb", the name is `f`
- "--f", "--foo-bar", the name is `f`
- "---f", the name is `f`

```python
@click.command()
@click.option('-s', '--string-to-echo')
def echo(string_to_echo):
    click.echo(string_to_echo)
```

```python
@click.command()
@click.option('-s', '--string-to-echo', 'string')
def echo(string):
    click.echo(string)
```

### Наиболее базовые опции - это [опции значений](https://click.palletsprojects.com/en/8.0.x/options/#basic-value-options)

Можно определить тип, обязательность параметра, показ дефолтных значений при запросе через `--help`. Кроме того, можно определить в качестве имен параметров заррезервированные имена

```python
@click.command()
@click.option('--from', '-f', 'from_')
@click.option('--to', '-t')
def reserved_param_name(from_, to):
    click.echo(f"from {from_} to {to}")
```

### Можно передавать несколько значений опции

```python
@click.command()
@click.option('--pos', nargs=2, type=float)
def findme(pos):
    a, b = pos
    click.echo(f"{a} / {b}")
```

Кроме того, [можно использовать кортежи](https://click.palletsprojects.com/en/8.0.x/options/#tuples-as-multi-value-options) и [множественные опции по одному имени](https://click.palletsprojects.com/en/8.0.x/options/#multiple-options)

```python
@click.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo(f"Verbosity: {verbose}")
```

```bash
$ commit -m foo -m bar
foo
bar
```

### [Булевы флаги](https://click.palletsprojects.com/en/8.0.x/options/#boolean-flags) используют определение двух имен через слеш

```python
import sys

@click.command()
@click.option('--shout/--no-shout', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

```bash
$ info --shout
LINUX!!!!111
$ info --no-shout
linux
$ info
linux
```

Если требуется только одно состояние флага, то можно так:

```python
import sys

@click.command()
@click.option('--shout', is_flag=True)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

### [Переключатель опций](https://click.palletsprojects.com/en/8.0.x/options/#feature-switches)

```python
import sys

@click.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def info(transformation):
    click.echo(getattr(sys.platform, transformation)())
```

```bash
$ info --upper
LINUX
$ info --lower
linux
$ info
LINUX
```

### [Опция выбора опций](https://click.palletsprojects.com/en/8.0.x/options/#choice-options)

Можно передать список (или кортеж), из которого можно выбрать значение опции

```python
@click.command()
@click.option('--hash-type',
              type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
def digest(hash_type):
    click.echo(hash_type)
```

## [Ввод](https://click.palletsprojects.com/en/8.0.x/options/#prompting)

```python
@click.command()
@click.option('--name', prompt=True)
def hello(name):
    click.echo(f"Hello {name}!")
```

Или так:

```python
@click.command()
@click.option('--name', prompt='Your name please')
def hello(name):
    click.echo(f"Hello {name}!")
```

Ввод пародей [тоже реализован](https://click.palletsprojects.com/en/8.0.x/options/#password-prompts)

[Еще про опции ввода](https://click.palletsprojects.com/en/8.0.x/options/#dynamic-defaults-for-prompts)

### [Колбеки](https://click.palletsprojects.com/en/8.0.x/options/#callbacks-and-eager-options)

### [Запрос согласия для опасных операций](https://click.palletsprojects.com/en/8.0.x/options/#yes-parameters)

### [Значения из переменных окружения](https://click.palletsprojects.com/en/8.0.x/options/#values-from-environment-variables)

Есть несколько способов. Во первых можно реализовать через `auto_envvar_prefix=` самой функции

```python
@click.command()
@click.option('--username')
def greet(username):
    click.echo(f'Hello {username}!')

if __name__ == '__main__':
    greet(auto_envvar_prefix='GREETER')
```

Второй вариант - вручную добавить в декоратор черех `envvar=`

```python
@click.command()
@click.option('--username', envvar='USERNAME')
def greet(username):
   click.echo(f"Hello {username}!")

if __name__ == '__main__':
    greet()
```

Можно использовать [множественные переменные](https://click.palletsprojects.com/en/8.0.x/options/#multiple-values-from-environment-values)

### [Другие префиксы](https://click.palletsprojects.com/en/8.0.x/options/#other-prefix-characters)

### [Опция ренжа](https://click.palletsprojects.com/en/8.0.x/options/#range-options)

### [Валидация](https://click.palletsprojects.com/en/8.0.x/options/#callbacks-for-validation)

### [Опциональные значения](https://click.palletsprojects.com/en/8.0.x/options/#optional-value)

## [Аргументы](https://click.palletsprojects.com/en/8.0.x/arguments/)

Работауют идентично опциям, но являются позиционными. поддерживают лишь часть функционала и не документируются.

```python
@click.command()
@click.argument('filename')
def touch(filename):
    """Print FILENAME."""
    click.echo(filename)
```

```bash
$ touch foo.txt
foo.txt
```

Варианты использования:

- [переменные](https://click.palletsprojects.com/en/8.0.x/arguments/#variadic-arguments)
- [аргументы файлов](https://click.palletsprojects.com/en/8.0.x/arguments/#file-arguments)
- [аргументы путей файлов](https://click.palletsprojects.com/en/8.0.x/arguments/#file-path-arguments)
- [использование переменных окружения](https://click.palletsprojects.com/en/8.0.x/arguments/#environment-variables)
- [аргументы-опции](https://click.palletsprojects.com/en/8.0.x/arguments/#option-like-arguments)

## [Команды и группы](https://click.palletsprojects.com/en/8.0.x/commands/#commands-and-groups)

Это одна из главных фичей пакета - возможность собирать несколько аргументво в бандлы. Реализуется через `command`, `group` и `multicommand`

Что доступно:

- передача контекста между командами
- создание собственных групп команд
- мерж групп команд между собой
- цепочки мультикоманд
- пайплайны мультикоманд
- переопределение дефолтных значений
- дефолтные значения для разных контекстов

[Документация](https://click.palletsprojects.com/en/8.0.x/)

## [Документирование для --help](https://click.palletsprojects.com/en/8.0.x/documentation/)

## [Дополнительные паттерны](https://click.palletsprojects.com/en/8.0.x/advanced/#advanced-patterns)

- алиасы команд
- модификация параметров
- приведение токенов к правильному формату
- вызов других команд из команд
- определения порядка колбеков
- передача неизвестных опций в следующий контекст
- доступ к глобальному контексту
- определение источника параметра (логирование)
- управление ресурсами группы команд

## [Как все это тестировать](https://click.palletsprojects.com/en/8.0.x/testing/)

## [Дополнительные утилиты](https://click.palletsprojects.com/en/8.0.x/utils/)

- вывод в stdout
- ANSI colors
- пагинация
- очистка страницы
- получение отдельных знаков из терминала (к примеру y/n)
- press any key
- запуск редактора
- запуск приложения
- вывод названия файла
- использование стандартного потока
- открытие файла через контекстный менеджер
- поиск папки приложения
- прогресс-бар

Больше информации обо всем [в документации проекта](https://click.palletsprojects.com/en/8.0.x/) или на [github](https://github.com/pallets/click)

Смотри так-же:

- [[argparsing]]
- [[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[setuptools]: setuptools "Setuptools"
[argparsing]: argparsing "Arguments parsing in python"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"