---
description: Управление зависимостями и изоляция среды разработки в python с poetry
tags: cli cicd pip python
title: Poetry
---
**Poetry is a tool for dependency management and packaging in python**. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Замена [[requirements]]

Выставляется изолированно от остальной системы для осуществления версионирования зависимостей. В линуксе:

![poetry install](../attachments/2022-10-23-00-20-00.png)

[about installation](https://python-poetry.org/docs/#installation)

После установки можно проверить что записалось в PATH. Если ничего, то прописать путь к poetry `source $HOME/.poetry/env`. Проверит версию `poetry --version`

[Ссылка](https://python-poetry.org/docs/)

## [Basic usage](https://python-poetry.org/docs/basic-usage/#basic-usage)

### Project setup

poetry использует [[toml]] для конфигнов

`poetry new poetry-demo` создает новый poetry project с названием poetry-demo. В нем:

```shell
poetry-demo
├── pyproject.toml
├── README.rst
├── poetry_demo
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_poetry_demo.py
```

Здесб `pyproject.toml` задает архитоектуру проекта и зависимости

```toml
[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = ["Sébastien Eustace <sebastien@eustace.io>"]

[tool.poetry.dependencies]
python = "*"

[tool.poetry.dev-dependencies]
pytest = "^3.4"
```

### Preinitialize project (шаблон проекта)

Размещаем файл `.toml` в нужной папке и делаем инит

```shell
cd pre-existing-project
poetry init
```

### Specifying dependencies

Специфические зависимости прописываются в томле

```toml
[tool.poetry.dependencies]
pendulum = "^1.4"
```

В секции `tool.poetry.repositories` можно прописать репозитории, в которых `poetry` будет искать зависимости. Дефолтный - [[pypy]]

Вместо ручной модификации, можно использовать `poetry add pendulum` - зависимость будет найдена, добавлена в томл со всеми сабзависимости и в правильной ограничивающей версии.

### Using your virtual environment

Окуржение poetry ставится в `{cache-dir}/virtualenvs`.

Можно использовать `poetry run`

Примеры:

`poetry run python your_script.py`
`poetry run pytest`

Другой вариант - создать `poetry shell`. Создание нового шела обязательно. Выйти можно через `exit` или `deactivate` не выходя из шела.

Третий вариант - запустить вручную: `source {path_to_venv}/bin/activate`. Путь можно получить так: `poetry env info --path`, соответственно одной командой: source\`poetry env info --path\`/bin/activate`

[Подробнее тут](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment)

### [Installing dependencies](https://python-poetry.org/docs/basic-usage/#installing-dependencies)

`poetry install` в проекте

Если запускается впервые, то создается `poetry.lock` и все ставится с нуля. Дальше poetry будет сверяться с lock и ставить только отсутствующие или измененные зависимости. Необходимо постоянно комитить лок систему контроля версий, чтобы обновлять версии для установки.

Если нужно установить только зависимости,то тогда `poetry install --no-root`

## [Публикация библиотек с poetry](https://python-poetry.org/docs/libraries/)

## [Команды](https://python-poetry.org/docs/cli/)

Основное - это [install](https://python-poetry.org/docs/cli/#install). Инсталит из `.toml` с учетом `.lock`

- `poetry install`
- `poetry install --no-dev` без дева
- `poetry install --remove-untracked` - не ставить то, что не трекается в lock
- `poetry install --extras "mysql pgsql"` включить экстра зависимости
- `poetry install -E mysql -E pgsql`
- `poetry install --no-root` не инсталится рут-пкет (мой проект)

Апдейт зависимостей в `.lock` через `poetry update`. Можно заапдейтить только часть `poetry update requests toml`

Добавление необходимых зависимостей в `.toml` через `poetry add requests pendulum` - зависимости добавляются, затем инсталлируются.

Опции

- `--dev (-D)`: Add package as development dependency
- `--path`: The path to a dependency
- `--optional` : Add as an optional dependency
- `--dry-run` : Outputs the operations but will not execute anything (implicitly enables --verbose)
- `--lock` : Do not perform install (only update the lockfile)

Удалчерез `poetry remove pendulum`. Посмотреть зависимости `poetry show`

Остальное смотри в доке.

## [Configuration](https://python-poetry.org/docs/configuration/)

## [Repositories](https://python-poetry.org/docs/repositories/)

## [Managing environments](https://python-poetry.org/docs/managing-environments/)

Poetry работает всегда изолированно от глобального питона. При создании окружения poetry использует текущую активированную версию #python. Есть возможность переключаться между различными версиями python - [подробнее](https://python-poetry.org/docs/managing-environments/#switching-between-environments)

[Решение проблемы с путями к питону в vs-code](https://github.com/microsoft/vscode-python/issues/8372)

- `poetry env info` инфа об окружении
- `poetry env list` листинг окружений, ассоциированных с проектом
- `poetry env use python 3.8` использовать определенный питон

Окружения можно снести через `delete`

## [Спецификация зависимостей и их версий в .toml](https://python-poetry.org/docs/dependency-specification/)

## [Состав .toml](https://python-poetry.org/docs/pyproject/)

- `name` имя пакета (проекта) required
- `version` версия required
- `description` required
- `license`
- `authors` required
- `maintainers`
- `readme`
- `homepage`
- `repository`
- `documentation`
- `keywords`
- `classifiers`
- `packages` - список пакетов и модулей, включаемых в финальную версию
- `include` and `exclude` - список паттернов, которые необходимо включить в финальный проект
- `dependencies` and `dev-dependencies`
- `scripts` скрипты, которые необходимо выполнить при инсталяции
- `extras` опциональные зависимости
- `plugins`
- `urls`

[Пример реализации проекта на poetry](https://browniebroke.com/blog/migrating-project-to-poetry/)
[Как использовать poetry](https://elements.heroku.com/buildpacks/moneymeets/python-poetry-buildpack) на [[heroku]], [[heroku-cli]]

## Еще материалы

### How to update Poetry's lock file without upgrading dependencies?

`poetry lock --no-update`

### Как сделать энтри-поинт в проекте с poetry

Пример с [[click]]:

```python
import click

@click.group()
def main():
    """packagename cli"""

@main.command()
def packagefunction():
    """packagefunction subcommand"""
```

```yml
[tool.poetry.scripts]
# command_name = module_for_handler : function_for_handler
<packagename> = '<packagename>:<main>'
```

[Источник на оверфло](https://stackoverflow.com/a/55065934/15966204). [Еще примеры](https://stackoverflow.com/questions/59286983/how-to-run-a-script-using-pyproject-toml-settings-and-poetry) и [еще](https://stackoverflow.com/questions/67476156/pass-commandline-arguments-to-a-python-script-installed-with-poetry). Здесь можно [прочитать почему это может не работать.](https://stackoverflow.com/a/70656210/15966204).

Альтернатива: [[poetrypoet]]

Смотри еще:

- [b'Head' on 'poetry update' or 'poetry lock'](https://github.com/python-poetry/poetry/issues/7523)
- [Document docker poetry best practices](https://github.com/orgs/python-poetry/discussions/1879)
- [[setuptools]]
- [cookiecutter-poetry](https://fpgmaas.github.io/cookiecutter-poetry/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[requirements]: requirements "Requirements.txt"
[toml]: toml "Toml"
[pypy]: pypy "Pypy"
[heroku]: ../lists/heroku "Heroku"
[heroku-cli]: heroku-cli "Heroku-cl"
[click]: click "Click интерфейс командной строки"
[poetrypoet]: poetrypoet "Poetrypoet"
[setuptools]: setuptools "Setuptools"
[//end]: # "Autogenerated link references"