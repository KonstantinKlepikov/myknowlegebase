---
description: Нативное решение для управления кластром контенеров. Docker swarm
tags: docker
title: Docker swarm
---
Нативное решение [[docker]] для разворачивания и управления кластером контейнеров. Аналог, рекомендуемый для [[fastapi]] - [[docker-swarm-rocks]]

## Create a swarm

[ссылка](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/)

Если используется `docker-machine`, то подключиться к серваку по ssh (в примере `manager1`)

```sh
docker-machine ssh manager1
```

Инициализировать swarm ([подробнее про команду](https://docs.docker.com/engine/reference/commandline/swarm_init/))

```sh
docker swarm init --advertise-addr <MANAGER-IP>
```

Посмотреть - как все прошло:

```sh
docker info
```

Посмотреть инфу по нодам

```sh
docker node ls
```

## [Пример деплоя на сворм](https://docs.docker.com/engine/swarm/services/)

Тут важно - связка с регистри (если используется). В примере связка с реигстри создается как сервис.

```sh
docker login registry.example.com

docker service create \
--with-registry-auth \
--name my_service \
registry.example.com/acme/my_image:latest
```

`--with-registry-auth` обеспечивает передачу об аутентификации в частном регистри в контекст сворма.

Деплой происходит с помозью `docker stack depoy` ([ссылка на доку](https://docs.docker.com/engine/reference/commandline/stack_deploy/))

Вот так

```sh
docker stack deploy [OPTIONS] STACK
```

Или так с реигстри:

```sh
docker stack deploy --with-registry-auth STACK
```

[Пример смотри тут](http://littlebigextra.com/installing-docker-images-private-repositories-docker-swarm/)

## Swarm: Get Node Ip and Container IP from service

To get the node IP address you can use below command:

```bash
{% raw %}
docker node inspect self --format '{{.Status.Addr}}'
{% endraw %}
```

To get the service IP address, Just add service-id in the end, like:

```bash
{% raw %}
docker node inspect self --format '{{.Status.Addr}}' service-id
{% endraw %}
```

To get the container IP address, use:

```bash
{% raw %}
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container-id
{% endraw %}
```

[Ссылка](https://stackoverflow.com/a/56071286/15966204)

## Полезные материалы

- [How to Create a Cluster of Docker Containers with Docker Swarm and DigitalOcean on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-create-a-cluster-of-docker-containers-with-docker-swarm-and-digitalocean-on-ubuntu-16-04)
- [Create a Docker Swarm Cluster on DigitalOcean](https://lunar.computer/posts/docker-swarm-digitalocean/)
- [[docker-swarm-restart-containeers]]
- [[docker-solutions]] вопросы и решеиня по докеру

[[terraform]] - это [[digital-ocean]] docker swarm manager

[//begin]: # "Autogenerated link references for markdown compatibility"
[docker]: ../lists/docker "Docker"
[fastapi]: fastapi "Fastapi"
[docker-swarm-rocks]: docker-swarm-rocks "Docker swarm rocks"
[docker-swarm-restart-containeers]: docker-swarm-restart-containeers "Docker swarm restart services"
[docker-solutions]: docker-solutions "docker solutions"
[terraform]: terraform "Terraform"
[digital-ocean]: ../lists/digital-ocean "Digital ocean"
[//end]: # "Autogenerated link references"