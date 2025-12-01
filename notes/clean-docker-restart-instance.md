---
description: Как перезапустить докер стек без артефактов
tags: docker
title: How to do clean docker restsrt instance
---
Stop the container(s) using the following command:

`docker-compose down`
Delete all containers using the following command:

`docker rm -f $(docker ps -a -q)`
Delete all volumes using the following command:

`docker volume rm $(docker volume ls -q)`

Restart the containers using the following command:

`docker-compose up -d`

- [[docker]]
- [[docker-compose]]
- [[docker-solutions]] вопросы и решеиня по докеру


[docker]: ../lists/docker "Docker"
[docker-compose]: docker-compose "Docker compose"
[docker-solutions]: docker-solutions "docker solutions"
