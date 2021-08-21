---
description: Шаблон приложения на fastapi. Backend
---
# Fastapi-template-backend

Backend Requirements

- [[docker]]
- [[docker-compose-with-gcloud-authentication]]
- [[poetry]]
  
Frontend Requirements: [[Node.js]] (with [[npm]]).

**Backend local development**
Start the stack with Docker Compose:

`docker-compose up -d` - это запускается из корня проекта (в backend и глубже ходить не надо)

Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

PGAdmin, PostgreSQL web administration: http://localhost:5050

Flower, administration of Celery tasks: http://localhost:5555

[[traefik]] UI, to see how the routes are being handled by the proxy: http://localhost:8080

To check the logs, run:

`docker-compose logs`

To check the logs of a specific service, add the name of the service, e.g.:

`docker-compose logs backend`

If your Docker is not running in localhost (the URLs above wouldn't work) check the sections below on Development with Docker Toolbox and Development with a custom IP.

**Backend local development, additional details**
General workflow

From ./backend/app/ you can install all the dependencies with:

`$ poetry install`

Then you can start a shell session with the new environment with:

`$ poetry shell`

- `./backend/app/app/models/` SQLAlchemy models
- `./backend/app/app/schemas/` Pydantic schemas
- `./backend/app/app/api/` API endpoints
- `./backend/app/app/crud/` CRUD (Create, Read, Update, Delete). 

The easiest might be to copy the ones for Items (models, endpoints, and CRUD utils) and update them to your needs.

Add and modify tasks to the Celery worker in `./backend/app/app/worker.py`.

If you need to install any additional package to the worker, add it to the file `./backend/app/celeryworker.dockerfile`.

**Docker Compose Override**
During development, you can change Docker Compose settings that will only affect the local development environment, in the file `docker-compose.override.yml`.

The changes to that file only affect the local development environment, not the production environment. So, you can add "temporary" changes that help the development workflow.

To get inside the container with a bash session you can start the stack with:

`$ docker-compose up -d`
and then exec inside the running container:

`$ docker-compose exec backend bash` запускается так-же из корня
You should see an output like:

`root@7f2607af31c3:/app#`
that means that you are in a bash session inside your container, as a root user, under the /app directory.

There you can use the script /start-reload.sh to run the debug live reloading server. You can run that script from inside the container with:

`$ bash /start-reload.sh`
...it will look like:

`root@7f2607af31c3:/app# bash /start-reload.sh`
and then hit enter. That runs the live reloading server that auto reloads when it detects code changes.

Nevertheless, if it doesn't detect a change but a syntax error, it will just stop with an error. But as the container is still alive and you are in a Bash session, you can quickly restart it after fixing the error, running the same command ("up arrow" and "Enter").

...this previous detail is what makes it useful to have the container alive doing nothing and then, in a Bash session, make it run the live reload server.

**Backend tests**
To test the backend run:

`$ DOMAIN=backend sh ./scripts/test.sh`
The file `./scripts/test.sh` has the commands to generate a testing `docker-stack.yml` file, start the stack and test it.

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

If you use GitLab CI the tests will run automatically.

**Local tests**
Start the stack with this command:

`DOMAIN=backend sh ./scripts/test-local.sh`
The ./backend/app directory is mounted as a "host volume" inside the docker container (set in the file docker-compose.dev.volumes.yml). You can rerun the test on live code:

`docker-compose exec backend /app/tests-start.sh`

**Test running stack**
If your stack is already up and you just want to run the tests, you can use:

`docker-compose exec backend /app/tests-start.sh`
That `/app/tests-start.sh` script just calls pytest after making sure that the rest of the stack is running. If you need to pass extra arguments to pytest, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

`docker-compose exec backend bash /app/tests-start.sh -x`

**Test Coverage**
Because the test scripts forward arguments to pytest, you can enable test coverage HTML report generation by passing `--cov-report=html`

To run the local tests with coverage HTML reports:

DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
To run the tests in a running stack with coverage HTML reports:

`docker-compose exec backend bash /app/tests-start.sh --cov-report=html`

**Live development with Python Jupyter Notebooks**
If you know about Python Jupyter Notebooks, you can take advantage of them during local development.

The `docker-compose.override.yml` file sends a variable env with a value dev to the build process of the Docker image (during local development) and the Dockerfile has steps to then install and configure Jupyter inside your Docker container.

So, you can enter into the running Docker container:

`docker-compose exec backend bash`
And use the environment variable `$JUPYTER` to run a Jupyter Notebook with everything configured to listen on the public port (so that you can use it from your browser).

It will output something like:

```bash
root@73e0ec1f1ae6:/app# $JUPYTER
[I 12:02:09.975 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:02:10.317 NotebookApp] Serving notebooks from local directory: /app
[I 12:02:10.317 NotebookApp] The Jupyter Notebook is running at:
[I 12:02:10.317 NotebookApp] http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
[I 12:02:10.317 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 12:02:10.317 NotebookApp] No web browser found: could not locate runnable browser.
[C 12:02:10.317 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

you can copy that URL and modify the "host" to be localhost or the domain you are using for development (e.g. local.dockertoolbox.tiangolo.com), in the case above, it would be, e.g.:

http://localhost:8888/token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
and then open it in your browser.

You will have a full Jupyter Notebook running inside your container that has direct access to your database by the container name (db), etc. So, you can just run sections of your backend code directly, for example with VS Code Python Jupyter Interactive Window or Hydrogen.

**Migrations**
**As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with alembic commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository**.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

Start an interactive session in the backend container:

`$ docker-compose exec backend bash`
If you created a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`, that Python module (base.py) that imports all the models will be used by Alembic.

After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

`$ alembic revision --autogenerate -m "Add column last_name to User model"`
**Commit to the git repository the files generated in the alembic directory.**

After creating the revision, run the migration in the database (this is what will actually change the database):

`$ alembic upgrade head`
If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

`Base.metadata.create_all(bind=engine)`
and comment the line in the file `prestart.sh` that contains:

`$ alembic upgrade head`
If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (.py Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

**Development in localhost with a custom domain**
You might want to use something different than localhost as the domain. For example, if you are having problems with cookies that need a subdomain, and Chrome is not allowing you to use localhost.

In that case, you have two options: you could use the instructions to modify your system hosts file with the instructions below in Development with a custom IP or you can just use localhost.tiangolo.com, it is set up to point to localhost (to the IP 127.0.0.1) and all its subdomains too. And as it is an actual domain, the browsers will store the cookies you set during development, etc.

If you used the default CORS enabled domains while generating the project, localhost.tiangolo.com was configured to be allowed. If you didn't, you will need to add it to the list in the variable BACKEND_CORS_ORIGINS in the .env file.

To configure it in your stack, follow the section Change the development "domain" below, using the domain localhost.tiangolo.com.

After performing those steps you should be able to open: http://localhost.tiangolo.com and it will be server by your stack in localhost.

Check all the corresponding available URLs in the section at the end.

**Development with a custom IP**
If you are running Docker in an IP address different than 127.0.0.1 (localhost) and 192.168.99.100 (the default of Docker Toolbox), you will need to perform some additional steps. That will be the case if you are running a custom Virtual Machine, a secondary Docker Toolbox or your Docker is located in a different machine in your network. See template documentation.

**Change the development "domain"**
If you need to use your local stack with a different domain than localhost, you need to make sure the domain you use points to the IP where your stack is set up. See the different ways to achieve that in the sections above (i.e. using Docker Toolbox with `local.dockertoolbox.tiangolo.com`, using `localhost.tiangolo.com` or using `dev.fastapi-template.herokuapp.com`).

To simplify your Docker Compose setup, for example, so that the API docs (Swagger UI) knows where is your API, you should let it know you are using that domain for development. You will need to edit 1 line in 2 files.

Open the file located at `./.env`. It would have a line like:

`DOMAIN=localhost`
Change it to the domain you are going to use, e.g.:

`DOMAIN=localhost.tiangolo.com`
That variable will be used by the Docker Compose files.

Now open the file located at `./frontend/.env`. It would have a line like:

`VUE_APP_DOMAIN_DEV=localhost`
Change that line to the domain you are going to use, e.g.:

`VUE_APP_DOMAIN_DEV=localhost.tiangolo.com`
That variable will make your frontend communicate with that domain when interacting with your backend API, when the other variable VUE_APP_ENV is set to development.

After changing the two lines, you can re-start your stack with:

`docker-compose up -d`
and check all the corresponding available URLs in the section at the end.

Состав бекенда темплейта [[fastapi]]
[[fastapi-template-vue-frontend]]

```bash
📦backend
 ┣ 📂app
 ┃ ┣ 📂alembic
 ┃ ┃ ┣ 📂versions
 ┃ ┃ ┃ ┣ 📜.keep
 ┃ ┃ ┃ ┗ 📜d4867f3a4c0a_first_revision.py
 ┃ ┃ ┣ 📜README
 ┃ ┃ ┣ 📜env.py
 ┃ ┃ ┗ 📜script.py.mako
 ┃ ┣ 📂app
 ┃ ┃ ┣ 📂api
 ┃ ┃ ┃ ┣ 📂api_v1
 ┃ ┃ ┃ ┃ ┣ 📂endpoints
 ┃ ┃ ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┃ ┃ ┣ 📜items.py
 ┃ ┃ ┃ ┃ ┃ ┣ 📜login.py
 ┃ ┃ ┃ ┃ ┃ ┣ 📜users.py
 ┃ ┃ ┃ ┃ ┃ ┗ 📜utils.py
 ┃ ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┃ ┗ 📜api.py
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┗ 📜deps.py
 ┃ ┃ ┣ 📂core
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜celery_app.py
 ┃ ┃ ┃ ┣ 📜config.py
 ┃ ┃ ┃ ┗ 📜security.py
 ┃ ┃ ┣ 📂crud
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜base.py
 ┃ ┃ ┃ ┣ 📜crud_item.py
 ┃ ┃ ┃ ┗ 📜crud_user.py
 ┃ ┃ ┣ 📂db
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜base.py
 ┃ ┃ ┃ ┣ 📜base_class.py
 ┃ ┃ ┃ ┣ 📜init_db.py
 ┃ ┃ ┃ ┗ 📜session.py
 ┃ ┃ ┣ 📂email-templates
 ┃ ┃ ┃ ┣ 📂build
 ┃ ┃ ┃ ┃ ┣ 📜new_account.html
 ┃ ┃ ┃ ┃ ┣ 📜reset_password.html
 ┃ ┃ ┃ ┃ ┗ 📜test_email.html
 ┃ ┃ ┃ ┗ 📂src
 ┃ ┃ ┃ ┃ ┣ 📜new_account.mjml
 ┃ ┃ ┃ ┃ ┣ 📜reset_password.mjml
 ┃ ┃ ┃ ┃ ┗ 📜test_email.mjml
 ┃ ┃ ┣ 📂models
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜item.py
 ┃ ┃ ┃ ┗ 📜user.py
 ┃ ┃ ┣ 📂schemas
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜item.py
 ┃ ┃ ┃ ┣ 📜msg.py
 ┃ ┃ ┃ ┣ 📜token.py
 ┃ ┃ ┃ ┗ 📜user.py
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┃ ┣ 📂api
 ┃ ┃ ┃ ┃ ┣ 📂api_v1
 ┃ ┃ ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┃ ┃ ┣ 📜test_celery.py
 ┃ ┃ ┃ ┃ ┃ ┣ 📜test_items.py
 ┃ ┃ ┃ ┃ ┃ ┣ 📜test_login.py
 ┃ ┃ ┃ ┃ ┃ ┗ 📜test_users.py
 ┃ ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┃ ┣ 📂crud
 ┃ ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┃ ┣ 📜test_item.py
 ┃ ┃ ┃ ┃ ┗ 📜test_user.py
 ┃ ┃ ┃ ┣ 📂utils
 ┃ ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┃ ┣ 📜item.py
 ┃ ┃ ┃ ┃ ┣ 📜user.py
 ┃ ┃ ┃ ┃ ┗ 📜utils.py
 ┃ ┃ ┃ ┣ 📜.gitignore
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┗ 📜conftest.py
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜backend_pre_start.py
 ┃ ┃ ┣ 📜celeryworker_pre_start.py
 ┃ ┃ ┣ 📜initial_data.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜tests_pre_start.py
 ┃ ┃ ┣ 📜utils.py
 ┃ ┃ ┗ 📜worker.py
 ┃ ┣ 📂scripts
 ┃ ┃ ┣ 📜format-imports.sh
 ┃ ┃ ┣ 📜format.sh
 ┃ ┃ ┣ 📜lint.sh
 ┃ ┃ ┣ 📜test-cov-html.sh
 ┃ ┃ ┗ 📜test.sh
 ┃ ┣ 📜.coverage
 ┃ ┣ 📜.flake8
 ┃ ┣ 📜.gitignore
 ┃ ┣ 📜alembic.ini
 ┃ ┣ 📜mypy.ini
 ┃ ┣ 📜poetry.lock
 ┃ ┣ 📜prestart.sh
 ┃ ┣ 📜pyproject.toml
 ┃ ┣ 📜tests-start.sh
 ┃ ┗ 📜worker-start.sh
 ┣ 📜.gitignore
 ┣ 📜backend.dockerfile
 ┗ 📜celeryworker.dockerfile
 ```

[//begin]: # "Autogenerated link references for markdown compatibility"
[docker]: ../lists/docker "Docker"
[docker-compose-with-gcloud-authentication]: docker-compose-with-gcloud-authentication "Docker-compose-with-gcloud-authentication"
[poetry]: poetry "Poetry"
[npm]: ../lists/npm "Npm"
[traefik]: traefik "Traefik"
[fastapi]: ../lists/fastapi "Fastapi"
[fastapi-template-vue-frontend]: fastapi-template-vue-frontend "Fastapi frontend development"
[//end]: # "Autogenerated link references"