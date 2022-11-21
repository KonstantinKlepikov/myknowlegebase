---
description: Основаная статья и список заметок о хостинге heroku
category: list
tags: heroku
title: Heroku
---
[Heroku dev center](https://devcenter.heroku.com/categories/heroku-architecture)

## Dynos

[Dynos and the Dyno Manager](https://devcenter.heroku.com/articles/dynos)

- Web: Web dynos are dynos of the “web” process type that is defined in your Procfile. Only web dynos receive HTTP traffic from the routers.
- Worker: Worker dynos can be of any process type declared in your Procfile, other than “web”. Worker dynos are typically used for background jobs, queueing systems, and timed jobs. You can have multiple kinds of worker dynos in your application. For example, one for urgent jobs and another for long-running jobs. For more information, see Worker Dynos, Background Jobs and Queueing.
- One-off: One-off dynos are temporary dynos that can run detached, or with their input/output attached to your local terminal. They’re loaded with your latest release. They can be used to handle administrative tasks, such as database migrations and console sessions. They can also be used to run occasional background work, as with Heroku Scheduler. For more information, see One-Off Dynos.

To scale horizontally (scale out), add more dynos. For example, adding more web dynos allows you to handle more concurrent HTTP requests, and therefore higher volumes of traffic. To scale vertically (scale up), use bigger dynos. The maximum amount of RAM available to your application depends on the dyno type you use. Both horizontal and vertical scale are features of the professional dynos, and are not available to free or hobby dynos.

[Networking & DNS](https://devcenter.heroku.com/categories/networking-dns)

## [Heroku CLI](https://devcenter.heroku.com/categories/command-line)

[[heroku-cli]]

## [Deployment](https://devcenter.heroku.com/categories/deployment)

[[heroku-release-phase]]

Можно деплоиться с гитхаба, можно [деплоиться через контейнеры](https://devcenter.heroku.com/categories/deploying-with-docker) [[docker]].

Деплой с докером можно реализовать двумя путями:

### [деплой пресобранных контейнеров на heroku](https://devcenter.heroku.com/articles/container-registry-and-runtime)

Make sure you have a working Docker installation (eg. docker ps) and that you’re logged in to Heroku (`heroku login`).

Log in to Container Registry:

`heroku container:login`

Get sample code by cloning an Alpine-based python example:

`git clone https://github.com/heroku/alpinehelloworld.git`

Navigate to the app’s directory and create a Heroku app:

`heroku create`

```shell
Creating salty-fortress-4191... done, stack is heroku-18
https://salty-fortress-4191.herokuapp.com/ | https://git.heroku.com/salty-fortress-4191.git
```

Build the image and push to Container Registry:

`heroku container:push web`

Then release the image to your app:

`heroku container:release web`

Now open the app in your browser:

`heroku open`

[более подробно обо всех нюансах](https://devcenter.heroku.com/articles/container-registry-and-runtime#logging-in-to-the-registry)

### [создание контейнеров с heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)

The `heroku.yml` file is a manifest you can use to define your Heroku app. It allows you to:

- Build `Docker` images on Heroku
- Specify add-ons and config vars to create during app provisioning
- Take advantage of Review Apps when deploying Docker-based applications

Create a `heroku.ym`l file in your application’s root directory. The following example `heroku.yml` specifies the Docker image to build for the app’s web process:

```yml
build:
  docker:
    web: Dockerfile
run:
  web: bundle exec puma -C config/puma.rb
```

In this example, both `heroku.yml` and `Dockerfile` are in the same directory. If the `Dockerfile` lives in a non-root directory, specify the relative path in the `build.docker.web` value, such as `app/Dockerfile`.

If you don’t include a run section, Heroku uses the CMD specified in the Dockerfile.

Commit the file to your repo:

```bash
git add heroku.yml
git commit -m "Add heroku.yml"
```

Set the stack of your app to container:

```bash
heroku stack:set container
```

Push your app to Heroku:

```bash
git push heroku master
```

Your application will be built, and Heroku will use the run command provided in heroku.yml instead of your Procfile.

[Подроюнее про содержание heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#heroku-yml-overview)

## [Local Development with Docker Compose](https://devcenter.heroku.com/articles/local-development-with-docker-compose)

Example [[docker-compose]]. That python application depends on [[postgres]] and [[redis]], which you do not push to Heroku. Instead, use Heroku add-ons in production.

**Use Heroku add-ons in production:**

- For local development: use official Docker images, such as Postgres and Redis.
- For staging and production: use Heroku add-ons, such as [heroku-postgres](https://devcenter.heroku.com/articles/heroku-postgresql) and Heroku Redis.

Using official Docker images locally and Heroku add-ons in production provides you with the best of both worlds:

- Parity: You get parity by using the same services on your local machine as you do in production
- Reduced ops burden: By using add-ons, Heroku – or the add-on provider – takes the ops burden of replication, availability, and backup.

When using Docker Compose for local development, there are a few tips and tricks we think can help make you more successful.

**Create an .env file to avoid checking credentials into source code control**
By using Docker and Docker Compose, you can check your local development environment setup into source code control. To handle sensitive credentials, create a `.env` environment file with your credentials and reference it within your Compose YAML. Your .env should be added to your `.gitignore` and `.dockerignore` files so it is not checked into source code control or included in your [[docker]] image, respectively.

```yml
services:
  web:
    env_file: .env
```

**Mount your code as a volume to avoid image rebuilds**
Any time you make a change to your code, you need to rebuild your Docker image (which is a manual step and can be time consuming). To solve this issue, **mount your code as a volume**. Now rebuilds are no longer necessary when code is changed.

```yml
services:
  web:
    volumes:
      - ./webapp:/opt/webapp
```

**Use hostnames to connect to containers**
By default Compose sets up a single network for your app. When you name a service in your Compose YAML, it creates a hostname that you can then use to connect to the service.

Our services in Compose YAML:

```yml
services:
  web:
  redis:
  db:
```

Our connection strings:

```yml
postgres://db:5432
redis://redis:6379
```

**Running Compose in background mode**
When you execute docker-compose up your project is running in the foreground, displaying the output of your services. You can shut down the services gracefully using `ctrl+c`.

One lesser known option is to use `docker-compose up -d` to start your containers in the background (i.e., detached mode); you can tear down the Compose setup using `docker-compose down`. You check the logs of services running in background mode using `docker-compose logs`.

**Multi-dockerfile project structure**
When you have multiple services, we suggest creating a subdirectory for each Docker image in your project, with the `Dockerfile` stored in each respective directory:

```console
/web/Dockerfile
/redis/Dockerfile
/db/Dockerfile
/worker/Dockerfile
```

We don’t recommend storing all `Dockerfiles` in the project home directory, since it makes distinguishing between services harder.

**Run your containers as a non-root user**
It’s a good security practice to run your containers as a non-root user; but more importantly, containers you push to Heroku will run without root access. By testing your containers locally as a non-root user, you can ensure they will work in your Heroku production environment. Learn more in the container registry documentation.

## [Deployment Integrations](https://devcenter.heroku.com/categories/deployment-integrations)

[Деплой через гитхаб](https://devcenter.heroku.com/articles/github-integration)
Другие интеграции смотри по ссылке

## [Continuous Delivery](https://devcenter.heroku.com/categories/continuous-delivery)

- [[heroku-piplines]] make it easy to maintain separate staging and production environments for your app.
- [[heroku-review]] apps let you try out a GitHub pull request’s changes in an isolated and disposable environment.
- [[Heroku-CI]] automatically runs your app’s test suite on new GitHub pull requests, or when code is merged into your repo’s master branch.
- [[heroku-release-phase]] phase lets you run tasks (such as database migrations) before a new release is deployed.

[Создание пайплайнов](https://devcenter.heroku.com/articles/pipelines)
[review app](https://devcenter.heroku.com/articles/github-integration-review-apps)
[heroku-cl](https://devcenter.heroku.com/articles/heroku-ci)

Heroku CI automatically runs your app’s test suite with every push to your app’s GitHub repository, enabling you to easily review test results before merging or deploying changes to your codebase. Tests execute in a disposable environment that closely resembles your staging and production environments, which helps to ensure that results are accurate and obtained safely.

[Release Phase](https://devcenter.heroku.com/articles/release-phase)

Больше опций и вопросов интеграции в статье [Continuous Delivery](https://devcenter.heroku.com/categories/continuous-delivery)

## [Language Support](https://devcenter.heroku.com/categories/language-support)

## [Databases & Data Management](https://devcenter.heroku.com/categories/data-management)

## [Monitoring & Metrics](https://devcenter.heroku.com/articles/metrics)

## [App Performance](https://devcenter.heroku.com/categories/app-performance)

Аддоны, бестпрактикс, секюритити и прочее смотри в  оглавлении документации

- [[heroku-variables-config]]
- [[requirements]]

Смотир еще:

- [Heroku Alternatives for Python-based Applications](https://testdriven.io/blog/heroku-alternatives/)
- [[flyio]]
- [[render]]
- [[digital-ocean]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[heroku-cli]: ../notes/heroku-cli "Heroku-cl"
[heroku-release-phase]: ../notes/heroku-release-phase "Heroku release phase"
[docker]: docker "Docker"
[docker-compose]: ../notes/docker-compose "Docker compose"
[postgres]: ../notes/postgres "Postgres"
[redis]: ../notes/redis "Redis"
[docker]: docker "Docker"
[heroku-piplines]: ../notes/heroku-piplines "Heroku piplines"
[heroku-review]: ../notes/heroku-review "Heroku review"
[Heroku-CI]: ../notes/heroku-ci "Heroku-CI"
[heroku-release-phase]: ../notes/heroku-release-phase "Heroku release phase"
[heroku-variables-config]: ../notes/heroku-variables-config "Heroku variables config"
[requirements]: ../notes/requirements "Requirements.txt"
[flyio]: ../notes/flyio "Fly.io"
[render]: ../notes/render "Render.com"
[digital-ocean]: digital-ocean "Digital ocean"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[heroku-cli]: ../notes/heroku-cli "Heroku-cl"
[heroku-release-phase]: ../notes/heroku-release-phase "Heroku release phase"
[docker]: docker "Docker"
[docker-compose]: ../notes/docker-compose "Docker compose"
[postgres]: ../notes/postgres "Postgres"
[redis]: ../notes/redis "Redis"
[docker]: docker "Docker"
[heroku-piplines]: ../notes/heroku-piplines "Heroku piplines"
[heroku-review]: ../notes/heroku-review "Heroku review"
[Heroku-CI]: ../notes/heroku-ci "Heroku-CI"
[heroku-release-phase]: ../notes/heroku-release-phase "Heroku release phase"
[heroku-variables-config]: ../notes/heroku-variables-config "Heroku variables config"
[requirements]: ../notes/requirements "Requirements.txt"
[flyio]: ../notes/flyio "Fly.io"
[render]: ../notes/render "Render.com"
[digital-ocean]: digital-ocean "Digital ocean"
[//end]: # "Autogenerated link references"