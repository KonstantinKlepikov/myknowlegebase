---
description: Render - cloud hosting.
tags: cicd server
title: Render.com
---
[Heroku Alternatives for Python-based Applications](https://testdriven.io/blog/heroku-alternatives/)

## [render](https://render.com/)

It’s easy to deploy a Web Service on Render. Link your [GitHub](https://render.com/docs/github) or [GitLab](https://render.com/docs/gitlab) repository and click Create Web Service. Render automatically builds and [deploys](https://render.com/docs/deploys) your service every time you push to your repository. Our platform has native support for Node.js, Python, Ruby, Elixir, Go, and Rust. If these don’t work for you, we can also build and deploy anything with a Dockerfile.

Some features of Web Services on Render:

- [Zero downtime deploys](https://render.com/docs/deploys#zero-downtime-deploys)
- Free and [fully-managed TLS certificates](https://render.com/docs/tls)
- [Custom domains](https://render.com/docs/custom-domains) (including wildcards)
- Manual or automatic [scaling](https://render.com/docs/scaling)
- Optional [persistent disks](https://render.com/docs/disks)
- [Pull Request Previews](https://render.com/docs/pull-request-previews)
- [Instant rollbacks](https://render.com/docs/rollbacks)
- HTTP/2
- [DDoS protection](https://render.com/docs/ddos-protection)
- Brotli compression

[plans](https://render.com/pricing#services)

### code deployment

- Select Web Service from the New dropdown in the Render [Dashboard](https://dashboard.render.com/).
- Select the GitHub or GitLab repository to deploy from. You’ll need to connect your [GitHub](https://render.com/docs/github) or [GitLab](https://render.com/docs/gitlab) account to Render if you haven’t already. Both public and private repos are supported.
- Specify the following. Render will autopopulate some values with a best guess based on your code.
  - `Name`: A name for your Web Service
  - `Environment`: The programming language of your code or Docker
  - `Region`: The [geographic region](https://render.com/docs/regions) to deploy to
  - `Branch`: The git branch to build
  - `Build Command`: The command to build your Web Service
  - `Start Command`: The command to start your Web Service
  - `Plan`: The amount of RAM and how many CPUs your Web Service requires. Choose from the [available plans](https://render.com/pricing/#services).
- Within Advanced, you may also specify environment variables, secrets, persistent disk, health check path, and whether or not to auto deploy on every git push.
- Click Create Web Service. Once the build completes, your service starts, and it is listening on a port, you will be able to connect to the service.

Web Services on the free plan are automatically **spun down after 15 minutes of inactivity**. When a new request for a free service comes in, Render spins it up again so it can process the request.

This can cause a **response delay of up to 30 seconds for the first request** that comes in after a period of inactivity.

The free plan **allows for 750 hours of running time per month across all free Web Services in your account and 100 GB of egress bandwidth for each free service**. Bandwidth usage in excess of 100 GB is charged at $0.10/GB.

You can track your free usage and bandwidth in your dashboard on the [Billing page](https://dashboard.render.com/billing#free-plan). We will email you when you’re approaching the free usage limits and also when you exceed them.

When you exceed your free usage limits (i.e., usage hours and/or bandwidth), free services in your account are automatically suspended and can no longer serve traffic until they are upgraded to a paid plan or when free usage is reset at the end of the calendar month, whichever is sooner.

Free usage is reset on the 1st of every month, and all free services suspended for usage limits are automatically resumed.

Other limitation:

- Free Web Services can be restarted at any time.
- Free Web Services cannot scale beyond a single instance, either manually or through [autoscaling](https://render.com/docs/scaling).
- Free Web Services do not support persistent disks.
- Free Web Services do not support web shell access.
- Free Web Services do not support [one-off jobs](https://render.com/docs/jobs).
- Free Web Services cannot listen on these reserved ports: 8008, 8012, 8013, 8022, 9090, 9091.
- Free Web Services and Static Sites can use up to 400 free [build hours](https://render.com/docs/build-limits) per month.
- Builds for free Web Services are typically slower than builds for paid services. Upgrade to a [paid plan](https://render.com/pricing#services) for faster build and deploy times.
- **Not supported [[docker-compose]]!**

### Migrate from [[heroku]] to Render

[guide](https://render.com/docs/migrate-from-heroku)

- [Generate a Dockerfile.render, .render-buildpacks.json, and render.yaml using Render’s Heroku CLI Plugin](https://render.com/docs/migrate-from-heroku#step-1-generate-a-dockerfilerender-and-renderyaml)
- [Create Resources on Render](https://render.com/docs/migrate-from-heroku#step-2-create-resources-on-render)
- [Configure Environment Variables](https://render.com/docs/migrate-from-heroku#step-3-configure-environment-variables)
- [Copy Data From PostgreSQL](https://render.com/docs/migrate-from-heroku#step-4-copy-data-from-postgresql)
- [Update DNS Configuration](https://render.com/docs/migrate-from-heroku#step-5-update-dns-configuration)

### [github integrations](https://render.com/docs/github)

### [Monorepo Support](https://search.google.com/search-console?resource_id=https://konstantinklepikov.github.io/)

like this:

```sh
├── backend
│   ├── app # Generated at build time
│   ├── build
│   │   ├── amd64.sh
│   │   ├── quemu.sh
│   │   └── x86.sh
│   ├── main.go
│   ├── readme.md
│   └── util
│       ├── util.go
│       └── util_test.go
├── community
│   ├── docker
│   │   ├── Dockerfile
│   │   ├── docker-entrypoint.sh
│   │   └── setup.sh
│   └── readme.md
└── frontend
    ├── build # Generated at build time
    ├── components
    │   └── login.js
    ├── index.js
    ├── sample.ts
    └── src
        ├── auth.js
        ├── authn.js
        ├── authz.js
        └── readme.md
```

### python version

By default, Render uses the latest patch version of Python 3.7.

You can customize the Python version for your app by setting the PYTHON_VERSION environment variable to a valid Python version, for example 3.8.2. Supported Python versions are those after 3.7.0. Unreleased versions are not supported natively, but can be deployed using [Render’s Docker support](https://render.com/docs/docker).

Дополнительные ресурсы:

- [Native Environments](https://render.com/docs/native-environments)
- [Monorepo Support](https://render.com/docs/monorepo-support#settings-relative-to-root-directory)
- [Connect GitHub](https://render.com/docs/github)
- [Blueprint Specification](https://render.com/docs/blueprint-spec#environment)
- uvicorn on render - [one](https://community.render.com/t/uvicorn-service-starts-but-site-isnt-deployed/1273), [two](https://community.render.com/t/permission-denied-when-trying-to-deploy-fastapi-app-using-uvicorn/2829)
- [Connecting to MongoDB Atlas](https://render.com/docs/connect-to-mongodb-atlas) (add ip-adreses of web-service to mongo-cloud permissions for visibility of db inside render environment)
- [Web Services](https://render.com/docs/web-services)

Смотри еще:

- [[heroku]]
- [[flyio]]
- [[digital-ocean]]
- [[docker]]


[docker-compose]: docker-compose "Docker compose"
[heroku]: ../lists/heroku "Heroku"
[flyio]: flyio "Fly.io"
[digital-ocean]: ../lists/digital-ocean "Digital ocean"
[docker]: ../lists/docker "Docker"
