---
description: Генератор python проектов
title: Cookiecutter python
tags: templating
---
Cookiecutter создает проекты из cookiecutter шаблонов проектов, например, проекты пакетов Python из шаблонов пакетов Python 3.7, 3.8, 3.9., 3.10

- [Документация](https://cookiecutter.readthedocs.io/en/stable/index.html#)
- [готовые шаблоны на github](https://github.com/search?q=cookiecutter&type=Repositories)
- [cookiecutter-poetry](https://fpgmaas.github.io/cookiecutter-poetry/)

### [Install](https://cookiecutter.readthedocs.io/en/stable/installation.html)

`python3 -m pip install --user cookiecutter`

### Usage

Сколнировать репозиторий шаблона и поправить `cookiecutter.json`

- можно устаревший на базе python 3.6-3.8 и setup.py: `git clone git@github.com:audreyr/cookiecutter-pypackage.git` ([ссылка](https://github.com/audreyfeldroy/cookiecutter-pypackage)). [Документация](https://cookiecutter-pypackage.readthedocs.io/en/latest/)
- можно с [[poetry]], [[github-action]] и precommit: `git clone git@github.com:fpgmaas/cookiecutter-poetry.git` ([ссылка](https://github.com/fpgmaas/cookiecutter-poetry)). [Документация](https://fpgmaas.github.io/cookiecutter-poetry/).

Сгенерировать проект из шаблона ([опции командной строки тут](https://cookiecutter.readthedocs.io/en/stable/cli_options.html)):

`cookiecutter cookiecutter-pypackage/` или можно напрямую сгенерировать зи репо `cookiecutter git@github.com:fpgmaas/cookiecutter-poetry.git`. Источниками шаблонов могут быть открытые или приватные репозитории, а так-же зазипованыне файлы.

[Tutorial](https://cookiecutter.readthedocs.io/en/stable/tutorials/index.html)

Преокт создается из файлов каталога `{{ cookiecutter.project_slug }}` с соответствующей подстановкой переменныхопределенных в `cookiecutter.json` с помощью пользовательского ввода.

### [Advanced Usage](https://cookiecutter.readthedocs.io/en/stable/advanced/index.html)

- [Using Pre/Post-Generate Hooks](https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html) запускает питоньи скрипты непосредственно перед и после сборки из шблона. Повзояляе контрллировать пространство файлов проекта.
- [User Config](https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html). Если вы часто используете Cookiecutter, вам будет полезно иметь файл конфигурации пользователя. По умолчанию Cookiecutter пытается получить настройки из файла `.cookiecutterrc` в вашем домашнем каталоге.
- [Calling Cookiecutter Functions From Python](https://cookiecutter.readthedocs.io/en/stable/advanced/calling_from_python.html). Это полезно, если, например, вы пишете веб-фреймворк и вам нужно предоставить разработчикам инструмент, похожий на django-admin.py startproject или npm init.
- [Injecting Extra Context](https://cookiecutter.readthedocs.io/en/stable/advanced/injecting_context.html)
- [Suppressing Command-Line Prompts](https://cookiecutter.readthedocs.io/en/stable/advanced/suppressing_prompts.html)
- [Templates in Context Values](https://cookiecutter.readthedocs.io/en/stable/advanced/templates_in_context.html). Значения (но не ключи) файла `cookiecutter.json` также могут являться шаблонами [[Jinja2]]. Значения из подсказок пользователя добавляются в контекст немедленно, так что одно значение контекста может быть получено из предыдущих значений. Этот подход потенциально может сэкономить пользователю много нажатий клавиш, предоставляя более разумные значения по умолчанию.
- Private Variables. Cookiecutter позволяет определять частные переменные, добавляя подчеркивание к имени переменной. Пользователю не требуется заполнять эти переменные. Они могут либо не отображаться с использованием предваряющего символа подчеркивания, либо визуализироваться с добавлением двойного подчеркивания.
- Copy without Render
- Replay Project Generation
- Choice Variables
- Dictionary Variables
- Template Extensions
- Organizing cookiecutters in directories
- Working with line-ends special symbols LF/CRLF
- Local Extensions

### More examples

- [Create your own Cookiecutter template](https://raphael.codes/blog/create-your-own-cookiecutter-template/)
- [Extending our Cookiecutter template](https://raphael.codes/blog/extending-our-cookiecutter-template/)
- [Wrapping up our Cookiecutter template](https://raphael.codes/blog/wrapping-up-our-cookiecutter-template/)

## Другие шаблонизаторы

### [CookieTemple](https://cookietemple.readthedocs.io/en/latest/)

- Dependency Management
  - [[poetry]]
- Documentation
  - Sphinx
  - Darglint to manage documentation linting
- Testing
  - [[pytest]]
  - Nox for cross platform testing
  - Codecoverage.yml for managing coverage
- [[github]]
  - Pull request
  - Feature request
  - Bug
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - updating docs
    - Dependabot dependency upgrades
    - syncs the project with their template updates as well
    - Has master branch protection enabled
    - Uses Pre-commit to fix everything before you push to GitHub
- [[makefile]]
  - Separate for Windows and Linux
- [[docker]] Dockerfile
  - Very basic, uses alpine Python distribution
- Type checking
  - [[mypy]]
- Security
  - Bandit for scanning vulnerabilities
- Other stuff
  - [[flake8]]
  - black
  - isort

### [CookieCutter Poetry](https://github.com/fpgmaas/cookiecutter-poetry)

- Dependency Management
  - [[poetry]]
- Documentation
  - MkDocs with Material Theme
  - ❌ No Darglint
- Testing
  - [[pytest]]
  - [[tox]] for cross platform testing
  - ❌ No Codecoverage
- [[github]]
  - Pull request
  - Feature request
  - Bug
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - updating docs
    - ❌ No Dependabot
    - ❌ No master branch protection enabled
    - ❌ Doesn't have Pre-Commit
- [[makefile]]
  - ❌ Not separate for Windows and Linux
- [[docker]] Dockerfile
  - ✅ Much better Dockerfile than cookietemple above, highly optimized
- Type checking
  - [[mypy]]
- Security
  - ❌ No sign of Bandit here
- Other stuff
  - [[flake8]]
  - black
  - isort

### [Wolt Python Package Cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter)

- Dependency Management
  - [[poetry]]
- Documentation
  - MkDocs Material (Both the above projects had a lot more into their documentation than this one)
  - ❌ No Darglint
  - ✅ This one has something both of the above ones dont. It is using python-kacl to automatically manage CHANGELOG
- Testing
  - [[pytest]]
  - ❌ No sign of [[tox]] or Nox
  - Codecoverage.yml for managing coverage
- [[github]]
  - Pull request
  - ❌ No Feature request Template
  - ❌ No Bug Template
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - updating docs
    - ❌ No Dependabot for dependency upgrades. Manages them manually which I think is not a good idea.
    - ❌ No master branch protection
    - Uses Pre-commit to fix everything before you push to GitHub
- ❌ No Makefile
- ❌ No Dockerfile
- Type checking
  - [[mypy]]
- Security
  - ❌ No Bandit
- Other stuff
  - [[flake8]]
  - black
  - isort
  - Uses cruft to keep templates automatically upto date

### [Python Project Template By Rucha Bruno](https://github.com/rochacbruno/python-project-template)

- Dependency Management
  - ✅ Uses setup tools by default but you can switch to [[puetry]] if you want
- Documentation
  - MkDocs
  - ❌ No sign of Darglint
  - ✅ This one also manages CHANGELOG automatically using gitchangelog
- Testing
  - [[pytest]]
  - No need for nox or [[tox]] in this one as they are manually testing it on each OS using the matrix strategy
  - Codecoverage.yml for managing coverage
- [[github]]
  - Pull request
  - Feature request
  - Bug
  - ✅ Adds a funding page too
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - ❌ Coudnt find where docs are getting updated
    - ❌ No sign of dependabot
    - ❌ No master branch protection
    - ❌ No sign of precommit
- [[makefile]]
  - ❌ Not separate for Windows and Linux
- Containerfile

[//begin]: # "Autogenerated link references for markdown compatibility"
[poetry]: poetry "Poetry"
[github-action]: github-action "Githunb action"
[Jinja2]: jinja2 "Jinja2 python"
[pytest]: pytest "Pytest"
[github]: ..%2Ftag%2Fgithub "Tag: github"
[makefile]: makefile "Makefile"
[docker]: ..%2Flists%2Fdocker "Docker"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[tox]: tox "Tox"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[poetry]: poetry "Poetry"
[github-action]: github-action "Githunb action"
[Jinja2]: jinja2 "Jinja2 python"
[poetry]: poetry "Poetry"
[pytest]: pytest "Pytest"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[makefile]: makefile "Makefile"
[docker]: ../lists/docker "Docker"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[poetry]: poetry "Poetry"
[pytest]: pytest "Pytest"
[tox]: tox "Tox"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[makefile]: makefile "Makefile"
[docker]: ../lists/docker "Docker"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[poetry]: poetry "Poetry"
[pytest]: pytest "Pytest"
[tox]: tox "Tox"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[pytest]: pytest "Pytest"
[tox]: tox "Tox"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[makefile]: makefile "Makefile"
[//end]: # "Autogenerated link references"