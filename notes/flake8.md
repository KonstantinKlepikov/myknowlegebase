---
description: Линтер для python
tags: tests python
title: Flake8
---
Линтер для python. [Ссылка на документацию](https://flake8.pycqa.org/en/latest/index.html)

## Using Flake8

```bash
flake8 path/to/code/to/check.py
# or
flake8 path/to/code/
```

If you only want to see the instances of a specific warning or error, you can select that error like so

```bash
flake8 --select E123,W503 path/to/code/
```

or ignore

```bash
flake8 --ignore E24,W504 path/to/code/
```

example для [[github-action]]:

```bash
# stop the build if there are Python syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

[Все опции](https://flake8.pycqa.org/en/latest/user/options.html)

В [[python-standart-library]] есть модуль [tabnanni](https://docs.python.org/3/library/tabnanny.html?highlight=tabnanny#module-tabnanny), реализующий проверку отступов


[github-action]: github-action "Githunb action"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
