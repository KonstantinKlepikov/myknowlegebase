# heroku основная статья

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

[[docker-compose]] is a tool for defining and running a multi-container Docker application. In this article you’ll learn why Docker Compose is great for local development, how you can push your Docker images to Heroku for deployment, and Compose tips and tricks.

[[heroku-piplines]]
[[heroku-variables-config]]
[heroku-postgres](https://devcenter.heroku.com/articles/heroku-postgresql)
[[requirements]]
