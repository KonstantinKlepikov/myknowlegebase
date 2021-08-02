# docker-compose

Let’s start out with a simple python-based multi-container [[docker]] application. This example app is comprised of a web frontend, Redis for caching, and Postgres as our database. With Docker, the web frontend, Redis, and Postgres each run in a separate container.

You can use Docker Compose to define your local development environment, including environment variables, ports you need accessible, and volumes to mount. Everything is defined in `docker-compose.yml`, which is used by the docker-compose CLI.

The following is the `docker-compose.yml` for the application:

```yml
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

```yml
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

The next service is the Postgres database, which opens port 5432 and uses the latest official Postgres image on Docker Hub.

```yml
db:
    image: postgres:latest
    ports:
      - "5432:5432"
```

[[[heroku]]
