---
description: Docker compose определение и запуск многоконтейнерных приложений
tags: docker
---
# Docker compose

[Основаня статья](https://docs.docker.com/compose/)

Compose - это инструмент для определения и запуска многоконтейнерных приложений Docker. В Compose вы используете файл YAML для настройки служб вашего приложения. Затем с помощью одной команды вы создаете и запускаете все службы из своей конфигурации. Чтобы узнать больше обо всех функциях Compose, см. [Список функций](https://docs.docker.com/compose/#features).

Compose работает во всех средах: production, staging, development, testing а так-же CI workflows. Вы можете узнать больше о каждом случае в разделе [Common Use Cases](https://docs.docker.com/compose/#common-use-cases). 

Использование Compose - это, по сути, трехэтапный процесс:

1. определите среды вашего приложения с помощью `Dockerfile`, чтобы его можно было воспроизвести где угодно.
2. Определите службы, составляющие ваше приложение, в docker-compose.yml, чтобы их можно было запускать вместе в изолированной среде.
3. Запустите `docker compose up`, и [Docker compose comands](https://docs.docker.com/compose/cli-command/) запустит все ваше приложение.

Docker-compose.yml выглядит так:

```yaml
version: "3.9"  # optional since v1.27.0
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
      - logvolume01:/var/log
    links:
      - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```

[Дока compose](https://docs.docker.com/compose/#compose-documentation)

[инстал](https://docs.docker.com/compose/install/)

## [Пример использования](https://docs.docker.com/compose/gettingstarted/)

### Step 1: setup

Создать папку проекта

```shell
mkdir composetest
cd composetest
```

Создать файл приложения

```python
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

Создать [[requirements]].txt

```shell
flask
redis
```

### Step 2: Create a Dockerfile

```docker
# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

Это дает:

- Build an image starting with the Python 3.7 image.
- Set the working directory to /code.
- Set environment variables used by the flask command.
- Install gcc and other dependencies
- Copy requirements.txt and install the Python dependencies.
- Add metadata to the image to describe that the container is listening on port 5000
- Copy the current directory . in the project to the workdir . in the image.
- Set the default command for the container to flask run.

Подробнее о [[dockerfile-learn]]

### Step 3: Define services in a Compose file

`docker-compose.yml`

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
  redis:
    image: "redis:alpine"
```

В данном случае определили два сервиса - web и [[redis]]

Web-сервис использует image, созданный из Dockerfile в текущем каталоге. Затем он связывает контейнер и хост-машину через открытый порт 5000. В этом примере службы используется порт по умолчанию для веб-сервера Flask, 5000.

Redis-сервис использует публичный [[redis]] image полученный из Docker Hub registry.

### Step 4: Build and run your app with Compose

```shell
docker-compose up
```

Compose развернет имеджи и стартанет сервисы. Теперь можно посмотреть открытый порт локально: http://localhost:5000/ или http://127.0.0.1:5000

Можно посмотреть что запущено

```shell
docker image ls
```

И остановить приложение

```shell
docker-compose down
```

### Step 5: Edit the Compose file to add a bind mount

Зададим привязку [[docker-bind-mound]] для web-сервиса

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
  redis:
    image: "redis:alpine"
```

Новый ключ томов монтирует каталог проекта (текущий каталог) на хосте в /code внутрm контейнера, что позволяет вам изменять код на лету, без необходимости перестраивать образ. Ключ среды устанавливает переменную среды FLASK_ENV, которая сообщает flask run о запуске в режиме разработки и перезагрузке кода при изменении. Этот режим следует использовать только в разработке.

### Step 6: Re-build and run the app with Compose

```shell
docker-compose up
```

### Step 7: Update the application

По той причине, что папка приложения смонтирована в контейнер, мы можем править ее содержимое и видеть изменеения мгновенно.

### Step 8: Experiment with some other commands

Detached mode - запуск сервисов в фоне

```shell
docker-compose up -d
```

Просмотр того, что в текущий момент запущено

```shell
docker-compose ps
```

[Полный список команд](https://docs.docker.com/compose/reference/)

Далее:

- [Переменные в файлах compose](https://docs.docker.com/compose/environment-variables/)
- [environment файл](https://docs.docker.com/compose/env-file/)
- [использование профайлов для сервисов](https://docs.docker.com/compose/profiles/)
- [поддержка GPU](https://docs.docker.com/compose/gpu-support/)
- [шаринг настроек между проектами и файлами](https://docs.docker.com/compose/extends/)
- [построение сетей в compose2](https://docs.docker.com/compose/networking/)
- [как работать с compose на проде](https://docs.docker.com/compose/production/)
- [контроль запуска и остановки для compose](https://docs.docker.com/compose/startup-order/)

## Еще один пример для compose - веб сервис и база данных

The following is the `docker-compose.yml` for the application:

```yaml
version: '2'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    env_file: .env
    depends_on:
      - db
    volumes:
      - ./webapp:/opt/webapp
  db:
    image: postgres:latest
    ports:
      - "5432:5432"
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

The first section defines the web service. It opens port 5000, sets environment variables defined in .env, and mounts our local code directory as a volume.

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    env_file: .env
    depends_on:
      - db
    volumes:
      - ./webapp:/opt/webapp
```

The next service is the [[postgres]] database, which opens port 5432 and uses the latest official Postgres image on Docker Hub.

```yaml
db:
    image: postgres:latest
    ports:
      - "5432:5432"
```

This section defines our [[redis]] service, which opens port 6379 and uses the official Redis image on Docker Hub.

```yaml
redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

Now that the local development environment is defined in `docker-compose.yml`, you can spin up all three services with one command:

```bash
docker-compose up
```

The following command confirms that all three containers are running:

```console
docker ps
CONTAINER ID        IMAGE                COMMAND
8e422ff92239        python_web           "/bin/sh -c 'python a"
4ac9ecc8a2a3        python_db            "/docker-entrypoint.s"
2cbc8febd074        redis:alpine         "docker-entrypoint.sh"
```

Using Docker and defining your local development environment with Docker Compose provides you with a number of benefits:

- By running Redis and Postgres in a Docker container, you don’t have to install or maintain the software on your local machine
- Your entire local development environment can be checked into source control, making it easier for other developers to collaborate on a project
- You can spin up the entire local development environment with one command: docker-compose up

Docker-compose поддерживается на [[heroku]]

[официальная документация](https://docs.docker.com/compose/)

Читай еще про [[docker-swarm-rocks]]

Про то как отправлять стек образов в [[digital-ocean-container-registry]] чиатй тут [[2021-08-27-daily-note]]

В конце этой заметки про ошибку синтаксиса в некоторых командах для compose: [[2021-09-07-daily-note]]

[Environment variables in Compose](https://docs.docker.com/compose/environment-variables/#substitute-environment-variables-in-compose-files). [Env files для compose v2](https://docs.docker.com/compose/compose-file/compose-file-v2/#env_file). Можно так (будут доступны все переменные, при совпадении последняя ихз последнего энва в списке):

```yml
env_file:
  - ./common.env
  - ./apps/web.env
  - /opt/runtime_opts.env
```

[//begin]: # "Autogenerated link references for markdown compatibility"
[requirements]: requirements "Requirements.txt"
[dockerfile-learn]: dockerfile-learn "Dockerfile"
[redis]: redis "Redis"
[redis]: redis "Redis"
[docker-bind-mound]: docker-bind-mound "Docker bind mount"
[postgres]: postgres "Postgres"
[redis]: redis "Redis"
[heroku]: ../lists/heroku "Heroku"
[docker-swarm-rocks]: docker-swarm-rocks "Docker swarm rocks"
[digital-ocean-container-registry]: digital-ocean-container-registry "Digital ocean container registry"
[2021-08-27-daily-note]: ../posts/2021-08-27-daily-note "Как добавить контейнеры на Digital Ocean registry с помощью docker-compose"
[2021-09-07-daily-note]: ../posts/2021-09-07-daily-note "Как устроен github packages, подводные камни интеграции с digital ocean и другими сервисами"
[//end]: # "Autogenerated link references"