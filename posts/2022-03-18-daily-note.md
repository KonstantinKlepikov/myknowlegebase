---
title: Работа с alembic и БД в docker, вопросы с poetry, linux и общие вопросы про python
description: Заметка про БД в докер, алембик, поэтри и несколько вопросов работы с python
category: post
---
## Database and alembic

### How to autogenerate and apply migrations with alembic when the database runs in a container

```yml
services:
  db:
    image: postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=username
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=database
    networks:
      - app-network
  app:
    build: .
    command: bash -c "cd app/database && alembic upgrade head && cd ../.. && python app/main.py"
    volumes:
      - .:/code
    ports:
      - "5000:5000"
    depends_on:
      - db
    networks:
      - app-network
networks:
  app-network:
```

### Change default postgres port

```shell
>export PGHOST=localhost

>export PGPORT=5432
```

### Multiple databases in docker and docker-compose

```yml
version: '3.0'

services:

  db:
    image: postgres
    environment:
      - POSTGRES_DB
      - POSTGRES_USER
      - POSTGRES_PASSWORD
    ports:
      - ${POSTGRES_DEV_PORT}:5432
    volumes:
      - app-volume:/var/lib/postgresql/data

  db-test:
    image: postgres
    environment:
      - POSTGRES_DB
      - POSTGRES_USER
      - POSTGRES_PASSWORD
    ports:
      - ${POSTGRES_TEST_PORT}:5432
    # Notice I don't even use a volume here since I don't care to persist test data between runs

volumes:
  app-volume: #
```

[more solution](https://stackoverflow.com/a/46668342/15966204)

## [[docker]]

### Container exited with code 0 when run from docker-compose

```shell
#!/bin/sh
# ... do other pre-launch setup ...
# Run the CMD
exec "$@"
```

[Подробное объяснение](https://stackoverflow.com/a/61695237/15966204)

## [[poetry]]

### Transfer dependency to --dev in poetry

You can move the corresponding line in the pyproject.toml from the [tool.poetry.dependencies] section to [tool.poetry.dev-dependencies] by hand and run poetry lock --no-update afterwards.

You can also `poetry add -D dep` and `poetry remove dep` in either order. Just be sure to use the same version constraint. Poetry stops/warns you if you use different constraints as they'd conflict.

## [[notes/linux]]

### [How to generate a random string](https://unix.stackexchange.com/questions/230673/how-to-generate-a-random-string)

`openssl rand -base64 12`

`openssl rand -hex 12`

## [[python-standart-library]]

- [How to remove query string from a url](https://stackoverflow.com/questions/51093564/how-to-remove-query-string-from-a-url)
- [pytest cannot import module while python can](https://stackoverflow.com/questions/41748464/pytest-cannot-import-module-while-python-can)
- [How can I find an element by CSS class with XPath](https://stackoverflow.com/questions/1604471/how-can-i-find-an-element-by-css-class-with-xpath) (смотри еще [[xpath]])
- [What's the difference between eval, exec, and compile](https://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile#:~:text=Basically%2C%20eval%20is%20used%20to,only%20for%20its%20side%20effects.)


[docker]: ../lists/docker "Docker"
[poetry]: ../notes/poetry "Poetry"
[notes/linux]: ../notes/linux "Linux"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[xpath]: ../notes/xpath "XPath в scrapy"
