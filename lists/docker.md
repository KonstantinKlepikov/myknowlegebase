# Docker

## Начало работы

`docker version`
`docker run debian echo 'hello world'`

В данном случае запускается образ debian (если его нет, он будет загружен с докерхаба) - упрощенный дестрибутив линукс. После загрузки и проверки образа он помещается в контейнер. Затем выполняется echo.

Запуск баша внутри контейнера: `docker run -i -t debian /bin/bash` (не заработал ui в vscode - видимо надо погуглить баг)

Зададим имя хоста: `docker run -h CONTAINER -i -t debian /bin/bash` а вот так заработал

Инфа по конкретному контейнеру: `docker inspect short_pseudonime`

Более короткий вывод через grep, например ip: `docker inspect short_pseudonime | grep IPAddress`

Или через `--format`: `docker inspect --format {{.NetworkSettings.IPAddress}} short_pseudonime`

Список файлов, которые были измсененеы в работающем контейнере: `docker diff short_pseudonime`

Список всех событий, произошедших внутри контейнера: `docker logs short_pseudonime`

Остановить контейнера: `exit`

Удаление всех остановленных контейнеров: `docker rm -v $(docker ps -aq -f status=exited)`

Удалить отдельный контейнер очень просто `docker rm short_pseudonime`

Проще всего вести раборту с докером через Dockerfile - это простой текстовый файл, в котором прописан скрипт, который будет выполнен при создании нового образа. Т.е. вначале мы создаем контейнер, а затем из него новый образ. Например такой докерфайл:

```Dockerfile
FROM debian
RUN apt-get update && apt-get install -y cowsay fortune
```

Инструкция FROM определяет базовый образ ОС - эта инструкция строго обязательна. RUN определяет команды, выполняемые в оболочке.

Теперь можно создавать образ с помощью `docker build` с помощью Dockerfile: `docker build -t test/cowsay-dockerfile`. Аналогично эту процедуру можно реализовать через run, команды в шеле внутри контейнера и docker commit.

Теперь можно запускать образ так-же, как и любой другой образ.

`docker run test/cowsay-dockerfile /usr/games/cowsay "Moo"`

![moo](../attachments/2021-06-07-23-15-44.png)

Все доп.команды, которые мы используем для запуска контейнера можно добавить в докерфайл - тогда они станут исполняться при запуске контейнера. При изменеении докерфайла требуется пересоздание образа.

```Dockerfile
FROM debian
RUN apt-get update && apt-get install -y cowsay fortune

ENTRYPOINT ["/usr/games/cowsay"]
```

`docker build -t test/cowsay-dockerfile`

Теперь входим так:

`docker run test/cowsay-dockerfile "Moo"`

Если создать рядом с докерфайлом entrypoint.sh, то можно получить некие исполняемые скрипты, в данном случае - доступ к потоку ввода/вывода. Теперь мы можем заменить и ентрипоинт (не забудь выдать права файлу entrypoint.sh. как исполняемому)

```Dockerfile
FROM debian
RUN apt-get update && apt-get install -y cowsay fortune
COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
```

```sh
#!/bin/bash
if [ $# -eq 0 ]; then
        /usr/games/fortune | /usr/games/cowsay
    else
        /usr/games/cowsay "$@"
fi
```

Инструкция COPY прост окопирует файл из файловой системы хоста в файловую систему образа. Первый аргумент - файл хоста, второй - путь в образе.

![moo](../attachments/2021-06-07-23-33-09.png)

Работа с репозиториями образов ведется с помощью build, pull, push

## Архитектура docker
