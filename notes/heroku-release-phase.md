---
description: Фаза релиза на heroku
tags: heroku
title: Heroku release phase
---
[Статья](https://devcenter.heroku.com/articles/release-phase)

```shell
release: ./release-tasks.sh
web: gunicorn myproject.wsgi
```

или

```shell
release: python manage.py migrate
web: gunicorn myproject.wsgi
```

Для [[alembic]]

```shell
release: alembic upgrade head
```

Релиз выполняется, когда:

- successful app build
- change to the value of a config var (unless the config var is associated with an add-on)
- pipeline promotion
- rollback
- release via the platform API
- Provisioning a new add-on

![release](../attachments/2021-04-27-00-43-41.png)

- [[heroku]]
- [[heroku-piplines]]
- [[requirements]]


[alembic]: alembic "Alembic"
[heroku]: ../lists/heroku "Heroku"
[heroku-piplines]: heroku-piplines "Heroku piplines"
[requirements]: requirements "Requirements.txt"
