---
title: Postgres Initialization scripts and unzip with init
description: Как запускать инициализирующие скрипты при старте контейнера с postgres и немного о pytest
category: post
---
## [[postgres]] Initialization scripts

Контейнер [[postgres]] [имеет](https://hub.docker.com/_/postgres?tab=description) встроенный способ инициализации состояния во время запуска. Если вы хотите выполнить дополнительную инициализацию в образе, [производном от данного](https://hub.docker.com/_/postgres), добавьте один или несколько сценариев `*.sql`, `*.sql.gz` или `*.sh` в /`docker-entrypoint-initdb.d` (при необходимости создав каталог). После того, как точка входа вызовет `initdb` для создания пользователя и базы данных postgres по умолчанию, она запустит любые файлы `*.sql`, запустит любые исполняемые сценарии `*.sh` и отыщет любые неисполняемые сценарии `*.sh`, найденные в этом каталоге, для дальнейшей инициализации перед запуском службы. Cценарии в `/docker-entrypoint-initdb.d` запускаются, только если вы запускаете контейнер с пустым каталогом данных; любая ранее существовавшая база данных останется нетронутой при запуске контейнера.

## unzip automatically with pg_restore

```python
if ext == 'gz':
   command = 'gunzip -c {} -k | pg_restore -U {} -h {} -p {}' \
             '-d {}'.format(file, user, server, port, new_dbname)
elif ext == 'bz2':
   command = 'bunzip2 -c {} -k | pg_restore -U {} -h {} -p {}' \
             '-d {}'.format(file, user, server, port, new_dbname)
elif ext == 'zip':
   command = 'unzip -p {} | pg_restore -U {} -h {} -p {} ' \
             '-d {}'.format(file, user, server, port, new_dbname)
else:
   command = 'pg_restore -U {} -h {} -p {} -d {} {}'.format(user,
                server, port, new_dbname, file)
```

[source](https://stackoverflow.com/a/23569855/15966204)

## [[pytest]] how to get the current test's name from the setup method

```python
class TestClass:

    @pytest.mark.parametrize("arg", ["a"])
    def test_stuff(self, request, arg):
        print("originalname:", request.node.originalname)
        print("name:", request.node.name)
        print("nodeid:", request.node.nodeid)

originalname: test_stuff
name: test_stuff[a]
nodeid: relative/path/to/test_things.py::TestClass::test_stuff[a]
```

[source](https://stackoverflow.com/a/68804077/15966204)

or how to find the test ID for parametrized tests during execution of the test

```python
os.environ.get('PYTEST_CURRENT_TEST')
```

[source](https://stackoverflow.com/a/67052616/15966204)

[//begin]: # "Autogenerated link references for markdown compatibility"
[postgres]: ../notes/postgres "Postgres"
[pytest]: ../notes/pytest "Pytest"
[//end]: # "Autogenerated link references"