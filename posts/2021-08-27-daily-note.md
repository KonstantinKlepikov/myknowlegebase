---
title: Как добавить контейнеры на Digital Ocean registry с помощью docker-compose
description: Немного про оркестрацию c docker и github
category: post
---
Нам понадобится создать [[github-action]] и иметь доступ к [[digital-ocean-container-registry]]. Тут есть ряд нюансов:

- на бесплатном тарифе в закрытых репозиториях нет [[github-environment-variables]]. Только [[github-secrets]]. Переменные окружения доступны только на тарифе enterprize
- на [[digital-ocean-container-registry]] на бесплатном тарифе помимо ограничений по объему, [ограничено число контейнеров](https://docs.digitalocean.com/products/container-registry/) (только 1). На следующем тарифе только 5. В этом контексте пожалуй лучше использовать [[github-packages]], котоыре при тех же ограничениях по объему никак не лимитированы по количеству контейнров... к тому же на публичных репозиториях нет и ограничений по объему
- потребуется [[digital-ocean-doctl]] - [вот тут](https://cloud.digitalocean.com/account/api/tokens) надо создать персональный acces tocken для doctl на github

Нам понадобится workflow в репозитории на github, в котором мы сделаем следующее:

- установим среду
- соберем контейнеры
- соединимся с [[digital-ocean-container-registry]]
- отправим туда контейнеры

Руководствоваться можно [вот этой статьей](https://docs.digitalocean.com/products/kubernetes/how-to/deploy-using-github-actions/)

Поставить `doctl` можно с помощью [вот такого](https://github.com/digitalocean/action-doctl) экшена из маркетплейса github. В данном случае в зашифрованную переменную как раз и помещен ключ, созданный на DO для доступа через cli `doctl`

```yml
- name: Install doctl
  uses: digitalocean/action-doctl@v2
  with:
    token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
```

Собирать контейнеры мы будем внутри github action jobs, для этого нам потребуется сначала собрать из исходников. размещенных в репозитории. а затем отправить в registry результат сборки. Чтобы понять где окажется image после сбьорки, это нужно сообщить в `docker-compose.yml`, [например так](https://stackoverflow.com/a/53418591/15966204) (локально):

```yml
version: '3'
services:
  build-1:
    build:
      context: ./build-1
    image: user/project-1
  build-2:
    build:
      context: ./build-2
    image: user/project-2
```

Естественно, если контейнеры будут нелокально, то необходимо указать адреса registry в сети, в нашем случае на [[digital-ocean]]. Соответственно сборку мы туда отправим с помощтью `docker compose push`, который обратиться к `docker-compose.yml` и увидит там эти адреса. [Подробнее о docker compose push](https://docs.docker.com/engine/reference/commandline/compose_push/)

Сложностью может оказаться то, что мы можем захотеть размещать стек как локально, так и удаленно. Можно использовать переменные окружения для задания пути ([смотри статью](https://medium.com/@stoyanov.veseline/pushing-docker-images-to-a-private-registry-with-docker-compose-d2797097751))

```yml
version: '3'

services:
  myapp:
    image: ${REGISTRY_HOST}/myproject/myapp:latest
    build: ./services/myapp
```

В этом случаем ожно задать переменные и использовать [[dot-env]] - переменные из `.env` файлов. Для [[fastapi-template-deployment]] это будет выглядеть так (на примере фронта) в `docker-compose.yml`:

```yml
  frontend:
    image: '${DOCKER_IMAGE_FRONTEND?Variable not set}:${TAG-latest}'
    build:
      context: ./frontend
      args:
        FRONTEND_ENV: ${FRONTEND_ENV-production}
```

Тогда мы можем выполнить сначала билд, а затем пуш, с помощью скрипта, выполняющего рекурсивно другой скрипт (так реализовано у tiangolo):

```sh
#! /usr/bin/env sh

# Exit in case of error
set -e

TAG=${TAG?Variable not set} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
sh ./scripts/build.sh

docker-compose -f docker-compose.yml push
```

```sh
#! /usr/bin/env sh

# Exit in case of error
set -e

TAG=${TAG?Variable not set} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
docker-compose \
-f docker-compose.yml \
build
```

А остальные переменные мы пропишем через `.env` в `docker-compose.yml` вот так:

```yml
env_file:
    - .env
```

Тут две пробелмы - надо либо держать зоопарк `.env` для разных стадий проекта. К тому же, если мы хотим собирать контейнеры на github, то надо как-то передать эти `.env` в репозиторий (а там пароли/ключи, что нежелательно). Вариант решения - задать пароли/ключи с помощью секретов на github, а остальные переменные прописать в отдельном `env`, который передавать в репозиторий. Наконец, чтобы получить правильный файл переменных окружения перед сборкой и пушем, можно сам файл переменных собирать в workflow, к примеру с помощью [экшена из маркетплейса гитхаб](https://github.com/KonstantinKlepikov/create-envfile)

```yml
name: Create envfile

on: [push]

jobs:

  create-envfile:
 
    runs-on: ubuntu-18.04
 
    steps:
    - name: Make envfile
      uses: SpicyPizza/create-envfile@v1
      with:
        envkey_DEBUG: false
        envkey_SOME_API_KEY: "123456abcdef"
        envkey_SECRET_KEY: ${{ secrets.SECRET_KEY }}
        some_other_variable: foobar
        directory: <directory_name>
        file_name: .env
```

Данная конкретная реализация пока работает неправильно - ключ `directory` не реализован. Если в проекте должно быть несколько энвов в разных папках, их можно создавать в руте и копироват ьв нужную папку с помощью [такого вот экшена](https://github.com/canastro/copy-action) (ну или подобного).

[Еще одна полезная штука](https://github.com/falti/dotenv-action) - прочитать `.env` и передать переменные в build шаг. В принципе это можно сделать обычным питоньим скриптом.

[//begin]: # "Autogenerated link references for markdown compatibility"
[github-action]: ../notes/github-action "Githunb action"
[digital-ocean-container-registry]: ../notes/digital-ocean-container-registry "Digital ocean container registry"
[github-environment-variables]: ../notes/github-environment-variables "Github environment variables"
[github-secrets]: ../notes/github-secrets "Github secrets"
[digital-ocean-container-registry]: ../notes/digital-ocean-container-registry "Digital ocean container registry"
[github-packages]: ../notes/github-packages "Github packages"
[digital-ocean-doctl]: ../notes/digital-ocean-doctl "Digital ocean doctl"
[digital-ocean-container-registry]: ../notes/digital-ocean-container-registry "Digital ocean container registry"
[digital-ocean]: ../lists/digital-ocean "Digital ocean"
[dot-env]: ../notes/dot-env "Dot-env"
[fastapi-template-deployment]: ../notes/fastapi-template-deployment "Fastapi template deployment"
[//end]: # "Autogenerated link references"