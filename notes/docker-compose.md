# docker-compose

Is a tool for defining and running a multi-container Docker application. In this article you’ll learn why Docker Compose is great for local development, how you can push your Docker images to Heroku for deployment, and Compose tips and tricks.

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

The next service is the [[postgress]] database, which opens port 5432 and uses the latest official Postgres image on Docker Hub.

```yml
db:
    image: postgres:latest
    ports:
      - "5432:5432"
```

This section defines our [[redis]] service, which opens port 6379 and uses the official Redis image on Docker Hub.

```yml
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
