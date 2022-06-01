---
description: Compose file version 3 reference
tags: docker
title: Docker compose file reference
---
[Compose file version 3 reference](https://docs.docker.com/compose/compose-file/compose-file-v3/#long-syntax-3)

example

```yaml
version: "3.9"
services:

  redis:
    image: redis:alpine
    ports:
      - "6379"
    networks:
      - frontend
    deploy:
      replicas: 2
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure

  db:
    image: postgres:9.4
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    deploy:
      placement:
        max_replicas_per_node: 1
        constraints:
          - "node.role==manager"

  vote:
    image: dockersamples/examplevotingapp_vote:before
    ports:
      - "5000:80"
    networks:
      - frontend
    depends_on:
      - redis
    deploy:
      replicas: 2
      update_config:
        parallelism: 2
      restart_policy:
        condition: on-failure

  result:
    image: dockersamples/examplevotingapp_result:before
    ports:
      - "5001:80"
    networks:
      - backend
    depends_on:
      - db
    deploy:
      replicas: 1
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure

  worker:
    image: dockersamples/examplevotingapp_worker
    networks:
      - frontend
      - backend
    deploy:
      mode: replicated
      replicas: 1
      labels: [APP=VOTING]
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 3
        window: 120s
      placement:
        constraints:
          - "node.role==manager"

  visualizer:
    image: dockersamples/visualizer:stable
    ports:
      - "8080:8080"
    stop_grace_period: 1m30s
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      placement:
        constraints:
          - "node.role==manager"

networks:
  frontend:
  backend:

volumes:
  db-data:
```

## Структура

Часть параметров можно записывать с полным синтаксисом, часть - в виде сокращенного.

- [build](https://docs.docker.com/compose/compose-file/compose-file-v3/#build) Параметры конфигурации, которые применяются во время сборки.
  - `context` - либо путь к каталогу, содержащему Dockerfile, либо URL-адрес репозитория git
  - `dockerfile` - альтернативный докерфайл
  - `args` - аргументы сборки, которые являются переменными среды, доступными только во время процесса сборки
  - `cache_from` - список имеджей, которые движок использует для разрешения кеша
  - labels - метадата в виде [docker labels](https://docs.docker.com/config/labels-custom-metadata/)
  - `network` - сетевые контейнеры, к которым подключаются инструкции RUN во время сборки
  - `shm_size` - размер раздела /dev/shm для контейнеров этой сборки
  - `target` - создает этап для [многоэтапной сборки](https://docs.docker.com/develop/develop-images/multistage-build/)
- `cap_add`, `cap_drop` - опции контейнера (игнорируется в [[docker-swarm]] моде)
- `cgroup_parent` контрольная группа контейнеров (игнорируется в сварм-моде)
- [command](https://docs.docker.com/compose/compose-file/compose-file-v3/#command) можно переопределить команду по умолчанию

    ```yaml
    command: bundle exec thin -p 3000
    ```

- [configs](https://docs.docker.com/compose/compose-file/compose-file-v3/#configs). Доступ к конфигурациям для каждой службы с помощью конфигурации для каждой службы. Оба варианта синтаксиса

    configs configuration reference

- [container_name](https://docs.docker.com/compose/compose-file/compose-file-v3/#container_name). Можно задать уникальное имя контейнера вместо автосгенеренного. игнорируется в сворме.
- [credential_spec](https://docs.docker.com/compose/compose-file/compose-file-v3/#credential_spec). Спецификация учетных данных для управляемой учетной записи службы. Этот параметр используется только для служб, использующих контейнеры Windows
- [depends_on](https://docs.docker.com/compose/compose-file/compose-file-v3/#depends_on) - зависимость от другого контейнера. Контейнеры поднимутся в порядке установленных зависимостей.

    > - `docker-compose up` starts services in dependency order.
    > - `docker-compose up SERVICE` automatically includes SERVICE’s dependencies.
    > - `docker-compose stop` stops services in dependency order.

    Установление зависимостей не ожидает готовности чего либо внутри контейнера. Опция игнорируется в сорм-моде.

- [deploy](https://docs.docker.com/compose/compose-file/compose-file-v3/#deploy) - конфигурация, связанная с развертыванием и запуском служб. Подпараметры вступают в силу только при развертывании в swarm через [docker stack deploy](https://docs.docker.com/engine/reference/commandline/stack_deploy/) и игнорируются при запуске `docker-compose up` и `docker-compose`, за исключением `resources`
  - `endpoint_mode` метод обнаружения службы для внешних клиентов, подключающихся к swarm
  - `labels` эти метки устанавливаются только для службы, а не для каких-либо контейнеров службы
  - `mode` тип контейнера в сворме
  - `placement` размещение ограничений и предпочтений
  - `max_replicas_per_node`
  - `replicas` количество контейнеров, которые должны быть запущены в любой момент времени
  - `resources` - квоты ресрусов (ЦПУ, память)
  - `restart_policy` как перезапускать контейнеры при выходе. Заменяет `restsrt`
  - `rollback_config` как следует выполнить откат службы в случае неудачного обновления
  - `update_config` как сервис должен быть обновлен. Полезно для настройки последовательных обновлений

    > Не поддерживается:
    >
    > - build
    > - cgroup_parent
    > - container_name
    > - devices
    > - tmpfs
    > - external_links
    > - links
    > - network_mode
    > - restart
    > - security_opt
    > - userns_mode

- [devices](https://docs.docker.com/compose/compose-file/compose-file-v3/#devices). Список сопоставлений устройств. Использует тот же формат, что и параметр создания клиента `docker --device`.
- [dns](https://docs.docker.com/compose/compose-file/compose-file-v3/#dns). Пользовательские DNS-серверы
- [dns_search](https://docs.docker.com/compose/compose-file/compose-file-v3/#dns_search). Пользовательские домены DNS
- [entrypoint](https://docs.docker.com/compose/compose-file/compose-file-v3/#entrypoint). Переопределяет точку входа по умолчанию (если в Dockerfile есть инструкция CMD, она тоже игнорируется).

    ```yaml
    entrypoint: /code/entrypoint.sh
    ```

- [env_file](https://docs.docker.com/compose/compose-file/compose-file-v3/#env_file). Переменные окружения из файла. Переменные среды, объявленные в `environment`, переопределяют эти значения — это остается истинным, даже если эти значения пусты или не определены. Порядок задания списка файлов имеет значение - файлы в списке обрабатываются сверху вниз

    ```yaml
    env_file:
      - ./common.env
      - ./apps/web.env
      - /opt/runtime_opts.env
    ```

    Если в службе указан `build`, переменные, определенные в `.env`, автоматически не отображаются во время сборки. Используйте подпараметр `args` в `build`, чтобы определить переменные среды времени сборки.

- [environment](https://docs.docker.com/compose/compose-file/compose-file-v3/#environment). Переменные среды. Вы можете использовать либо массив, либо словарь. Любые логические значения (true, false, yes, no) должны быть заключены в кавычки

    так:

    ```yaml
    environment:
        RACK_ENV: development
        SHOW: 'true'
        SESSION_SECRET:
    ```

    или так:

    ```yaml
    environment:
      - RACK_ENV=development
      - SHOW=true
      - SESSION_SECRET
    ```

    Аналогично - эти переменные не видны автоматически в `build` - нужно задать `args`

- [expose](https://docs.docker.com/compose/compose-file/compose-file-v3/#expose). Указание портов, не публикуя их на хост-машине — они будут доступны только связанным службам. Можно указать только внутренний порт

    ```yaml
    expose:
      - "3000"
      - "8000"
    ```

- [external_links](https://docs.docker.com/compose/compose-file/compose-file-v3/#external_links). Ссылка на контейнеры, запущенные за пределами этого docker-compose.yml или даже за пределами Compose, особенно для контейнеров, которые предоставляют общие службы. Контейнеры, созданные извне, должны быть подключены по крайней мере к одной из тех же сетей, что и служба, которая на них ссылается. Игнорируется в сворме.
- [extra_hosts](https://docs.docker.com/compose/compose-file/compose-file-v3/#extra_hosts). Сопоставления имен хостов. Используйте те же значения, что и в параметре клиента `docker --add-host`
- [healthcheck](https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck). Настройка проверки, которая запускается, чтобы определить, являются ли контейнеры для этой службы «работоспособными»

    ```yaml
    healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost"]
        interval: 1m30s
        timeout: 10s
        retries: 3
        start_period: 40s
    ```

- [image](https://docs.docker.com/compose/compose-file/compose-file-v3/#image). Jбраз, с которого будет запускаться контейнер. Может быть либо репозиторием/тегом, либо ID образа
- [init](https://docs.docker.com/compose/compose-file/compose-file-v3/#init). Запускает init внутри контейнера для передачи сигналов и запуска процессов.
- [isolation](https://docs.docker.com/compose/compose-file/compose-file-v3/#isolation). Технология изоляции контейнера. В Linux поддерживается только значение по умолчанию. В Windows допустимыми значениями являются значения default, process и hyperv
- [labels](https://docs.docker.com/compose/compose-file/compose-file-v3/#labels-2)
- [links](https://docs.docker.com/compose/compose-file/compose-file-v3/#links). Ссылка на контейнеры в другом сервисе. Легаси. Использовать `external_links`. Игнорируется в сворм-моде.
- [logging](https://docs.docker.com/compose/compose-file/compose-file-v3/#logging). Конфигурации логгирования внутри контейнера
- [network_mode](https://docs.docker.com/compose/compose-file/compose-file-v3/#network_mode). Сетевой режим. Используйте те же значения, что и параметр `docker client --network`, а также специальную форму `service:[service name]`. Игнорируется свормом.
- [networks](https://docs.docker.com/compose/compose-file/compose-file-v3/#networks). Сети, к которым нужно присоединиться, ссылаясь на [записи под ключом сети верхнего уровня](https://docs.docker.com/compose/compose-file/compose-file-v3/#network-configuration-reference).

    ```yaml
    services:
        some-service:
            networks:
            - some-network
            - other-network
    ```

    [Конфигурация для network](https://docs.docker.com/compose/compose-file/compose-file-v3/#network-configuration-reference)

    [Руководство по сетиям в compose](https://docs.docker.com/compose/networking/)

  - `aliases`. Псевдонимы (альтернативные имена хостов) для этой службы в сети. Другие контейнеры в той же сети могут использовать либо имя службы, либо этот псевдоним для подключения к одному из контейнеров службы.
  - `ipv4_address`, `ipv6_address` Статический IP-адрес для контейнеров для этой службы при подключении к сети
- [pid](https://docs.docker.com/compose/compose-file/compose-file-v3/#pid). Устанавливает режим PID в режим PID хоста. Это включает совместное использование контейнером и операционной системой хоста адресного пространства PID.
- [ports](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports). Открывает порты. Поддерживает короткий и длинный синтаксис. Можно задавать диапазоны.

    Короткий:

  - Укажите оба порта (`HOST:CONTAINER`)
  - Укажите только порт контейнера (в качестве порта хоста выбирается эфемерный порт хоста).
  - Укажите IP-адрес узла для привязки к обоим портам (по умолчанию `0.0.0.0`, что означает все интерфейсы): (`IPADDR:HOSTPORT:CONTAINERPORT`). Если `HOSTPORT` пуст (например, `127.0.0.1::80`), для привязки на хосте выбирается эфемерный порт.

    ```yaml
    ports:
      - "3000"
      - "3000-3005"
      - "8000:8000"
      - "9090-9091:8080-8081"
      - "49100:22"
      - "127.0.0.1:8001:8001"
      - "127.0.0.1:5000-5010:5000-5010"
      - "127.0.0.1::5000"
      - "6060:6060/udp"
      - "12400-12500:1240"
    ```

    Длинный:

  - `target`: порт внутри контейнера
  - `published`: общедоступный порт
  - `protocol`: протокол порта (tcp или udp)
  - `mode`: хост для публикации порта хоста на каждом узле или вход для порта в режиме сворма для балансировки нагрузки.

    ```yaml
    ports:
      - target: 80
        published: 8080
        protocol: tcp
        mode: host
    ```

- [profiles](https://docs.docker.com/compose/compose-file/compose-file-v3/#profiles). определяет список именованных профилей для включения службы. Если не установлено, служба всегда включена. [Подробнее](https://docs.docker.com/compose/profiles/)

    ```yaml
    profiles: ["frontend", "debug"]
    profiles:
    - frontend
    - debug
    ```

- [restart](https://docs.docker.com/compose/compose-file/compose-file-v3/#restart). Политика перезапуска. `no` — это политика перезапуска по умолчанию, и она не перезапускает контейнер ни при каких обстоятельствах. Если указано `always`, контейнер всегда перезапускается. Политика `on-failure` перезапускает контейнер, если код выхода указывает на ошибку при отказе. `unless-stopped` всегда перезапускает контейнер, за исключением случаев, когда контейнер остановлен (вручную или иным образом). Игнорируется в сворме.
- [secrets](https://docs.docker.com/compose/compose-file/compose-file-v3/#secrets). Доступ к шифрованным переменным для каждой службы с помощью конфигурации секретов для каждой службы. Поддерживаются оба синтаксиса. [Подробнее](https://docs.docker.com/engine/swarm/secrets/)

    С точки зрения сервисов Docker Swarm секрет — это блок данных, например пароль, закрытый ключ SSH, сертификат SSL или другой фрагмент данных, который не следует передавать по сети или хранить в незашифрованном виде в dockerfile или в папке вашего приложения. Вы можете использовать секреты Docker для централизованного управления этими данными и безопасной передачи их только тем контейнерам, которым необходим доступ к ним. Секреты шифруются во время передачи и далее в докерсварм. Данный секрет доступен только тем службам, которым был предоставлен явный доступ к нему, и только во время выполнения этих служебных задач.

    Короткий. Указывается только секретное имя. Это предоставляет контейнеру доступ к секрету и монтирует его в /run/secrets/<secret_name> внутри контейнера. И исходное имя, и целевая точка монтирования установлены на секретное имя.

    ```yaml
    version: "3.9"
    services:
        redis:
            image: redis:latest
            deploy:
            replicas: 1
            secrets:
            - my_secret
            - my_other_secret
        secrets:
        my_secret:
            file: ./my_secret.txt
        my_other_secret:
            external: true
    ```

    Полный синтаксис.

  - `source`: идентификатор секрета, как он определен в этой конфигурации.
  - `target`: имя файла, который будет смонтирован в /run/secrets/ в контейнерах задач службы. По умолчанию используется источник, если он не указан.
  - `uid` и `gid`: числовой UID или GID, которому принадлежит файл в /run/secrets/ в контейнерах задач службы. Оба значения по умолчанию равны 0, если не указано иное.
  - `mode` разрешения для файла, который будет смонтирован в /run/secrets/ в контейнерах задач службы, в восьмеричном представлении.

    ```yaml
    version: "3.9"
    services:
        redis:
            image: redis:latest
            deploy:
            replicas: 1
            secrets:
            - source: my_secret
                target: redis_secret
                uid: '103'
                gid: '103'
                mode: 0440
        secrets:
        my_secret:
            file: ./my_secret.txt
        my_other_secret:
            external: true
    ```

    Еще пример

    ```yaml
    version: '3'

    secrets:
    db_user:
        external: true
    db_password:
        external: true

    services:
    postgres_db:
    image: postgres
    secrets:
        - db_user
        - db_password
    environment:
        - POSTGRES_USER_FILE=/run/secrets/db_user
        - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    ```

    [Конфигурация secrets](https://docs.docker.com/compose/compose-file/compose-file-v3/#secrets-configuration-reference)

- [security_opt](https://docs.docker.com/compose/compose-file/compose-file-v3/#security_opt). Схема маркировки по умолчанию для каждого контейнера. Игнорируется в сворме.
- [stop_grace_period](https://docs.docker.com/compose/compose-file/compose-file-v3/#stop_grace_period). Как долго ждать при попытке остановить контейнер, если он не обрабатывает SIGTERM (или любой другой сигнал остановки, указанный с помощью stop_signal), перед отправкой SIGKILL.
- [stop_signal](https://docs.docker.com/compose/compose-file/compose-file-v3/#stop_signal). Устанавливает пользовательский сигнал для остановки контейнера.
- [sysctls](https://docs.docker.com/compose/compose-file/compose-file-v3/#sysctls). Параметры ядра для установки в контейнере
- [tmpfs](https://docs.docker.com/compose/compose-file/compose-file-v3/#tmpfs). Расположение монитруемых внутри контейнера временных файловых систем.
- [ulimits](https://docs.docker.com/compose/compose-file/compose-file-v3/#ulimits)
- [userns_mode](https://docs.docker.com/compose/compose-file/compose-file-v3/#userns_mode). Отключает пространство имен пользователей для этой службы, если демон Docker настроен с пространствами имен пользователей. Игнорируется в сворме.
- [volumes](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes). Пути хоста или именованные тома, заданные как подопции к службеДоступно оба синтаксиса.

    Тома можно смонтировать на уровне службы. Это полезно так-же чтобы использовать том в нескольких службах.

    ```yaml
    version: "3.9"
    services:
        web:
            image: nginx:alpine
            volumes:
            - type: volume
                source: mydata
                target: /data
                volume:
                nocopy: true
            - type: bind
                source: ./static
                target: /opt/app/static

        db:
            image: postgres:latest
            volumes:
            - "/var/run/postgres/postgres.sock:/var/run/postgres/postgres.sock"
            - "dbdata:/var/lib/postgresql/data"

    volumes:
        mydata:
        dbdata:
    ```

    В этом примере показан именованный том (`mydata`), используемый веб-службой, и монтирование привязки, определенное для одной службы (первый путь в томах службы БД). Служба db также использует именованный том с именем `dbdata` (второй путь в томах службы db), но определяет его, используя старый строковый формат для монтирования именованного тома. **Именованные тома должны быть перечислены под ключом томов верхнего уровня.**

    [Подробнее о томах](https://docs.docker.com/storage/volumes/) и в [docker plugins](https://docs.docker.com/engine/extend/plugins_volume/)

    Короткий синтаксис. Используется общий формат `[SOURCE:]TARGET[:MODE]`, где `SOURCE` может быть либо путем к хосту, либо именем тома. `TARGET` — это путь к контейнеру, в котором смонтирован том. Стандартные режимы: `ro` только для чтения и `rw` для чтения и записи (по умолчанию). Вы можете смонтировать относительный путь на хосте, который расширяется относительно каталога используемого файла конфигурации. Относительные пути всегда должны начинаться с `.` или же `..`

    ```yaml
    volumes:
        # Just specify a path and let the Engine create a volume
        - /var/lib/mysql

        # Specify an absolute path mapping
        - /opt/data:/var/lib/mysql

        # Path on the host, relative to the Compose file
        - ./cache:/tmp/cache

        # User-relative path
        - ~/configs:/etc/configs/:ro

        # Named volume
        - datavolume:/var/lib/mysql
    ```

    Длинный синтаксис.

  - `type`: тип монтирования `bind`, `tmpfs` или  `npipe`
  - `source`: источник монтирования, путь на хосте для монтирования. Или имя тома, определенное в ключе томов верхнего уровня. Неприменимо для монтирования `tmpfs`.
  - `target`: путь в контейнере, куда смонтирован том
  - `read_only`: флаг, чтобы сделать том доступным только для чтения
  - `bind`: настроить дополнительные параметры связывания
    - `propagation`: режим распространения, используемый для привязки
  - `volume`: настроить дополнительные параметры тома
    - `nocopy`: флаг для отключения копирования данных из контейнера при создании тома
  - `tmpfs`: настроить дополнительные параметры tmpfs
    - `size`: размер монтирования tmpfs в байтах

    ```yaml
    version: "3.9"
    services:
        web:
            image: nginx:alpine
            ports:
            - "80:80"
            volumes:
            - type: volume
                source: mydata
                target: /data
                volume:
                nocopy: true
            - type: bind
                source: ./static
                target: /opt/app/static

    networks:
        webnet:

    volumes:
        mydata:
    ```

    При создании привязанных монтирований использование длинного синтаксиса требует, чтобы папка, на которую делается ссылка, была создана заранее. Использование короткого синтаксиса создает папку на лету, если она не существует.

    При работе с сервисами, докер-свормом и файлами docker-stack.yml помните, что контейнеры, поддерживающие сервис, могут быть развернуты на любом узле, и каждый раз при обновлении сервиса это может быть другой узел.

    При отсутствии именованных томов с указанными источниками Docker создает анонимный том для каждой задачи, поддерживающей службу. Анонимные тома не сохраняются после удаления связанных контейнеров.

    Если вы хотите, чтобы ваши данные сохранялись, используйте именованный том и драйвер тома, поддерживающий работу с несколькими хостами, чтобы данные были доступны с любого узла. Или установите ограничения для службы, чтобы ее задачи развертывались на узле, на котором присутствует том.

    Например, файл docker-stack.yml для примера приложения определяет службу с именем db, которая запускает базу данных postgres. Он настроен как именованный том для сохранения данных сворме и ограничен запуском только на узлах менеджера.

    ```yaml
    version: "3.9"
    services:
        db:
            image: postgres:9.4
            volumes:
            - db-data:/var/lib/postgresql/data
            networks:
            - backend
            deploy:
            placement:
                constraints: [node.role == manager]
    ```

    [Подробнгее о конфигурации томов](https://docs.docker.com/compose/compose-file/compose-file-v3/#volume-configuration-reference) для создания томо, используемых в нескольких службах. Базовый пример

    ```yaml
    version: "3.9"

    services:
        db:
            image: db
            volumes:
            - data-volume:/var/lib/db
        backup:
            image: backup-service
            volumes:
            - data-volume:/var/lib/backup/data

    volumes:
        data-volume:
    ```

    Параметры:

    - `driver`. Укажите, какой драйвер тома следует использовать для этого тома. По умолчанию используется любой драйвер, который был настроен для использования Docker Engine, который в большинстве случаев является локальным
    - `driver_opts`. Список параметров драйвера.
    - `external`. Если установлено значение true, указывает, что этот том был создан вне Compose. `docker-compose up` не пытается его создать и выдает ошибку, если он не существует.

        В приведенном ниже примере вместо попытки создать том с именем [projectname]_data Compose ищет существующий том с простым названием data и монтирует его в контейнеры службы БД.

        ```yaml
        version: "3.9"

        services:
            db:
                image: postgres
                volumes:
                - data:/var/lib/postgresql/data

        volumes:
            data:
                external: true
        ```

    - `labels`
    - `name`. Задайте собственное имя для этого тома. Поле имени можно использовать для ссылки на тома, содержащие специальные символы. Имя используется как есть и не будет ограничиваться именем стека.

- [domainname, hostname, ipc, mac_address, privileged, read_only, shm_size, stdin_open, tty, user, working_dir](https://docs.docker.com/compose/compose-file/compose-file-v3/#domainname-hostname-ipc-mac_address-privileged-read_only-shm_size-stdin_open-tty-user-working_dir). Каждое из них представляет собой одно значение, аналогичное его аналогу вщслук кгт. Обратите внимание, что mac_address является устаревшей опцией.

    ```yaml
    user: postgresql
    working_dir: /code

    domainname: foo.com
    hostname: foo
    ipc: host
    mac_address: 02:42:ac:11:65:43

    privileged: true


    read_only: true
    shm_size: 64M
    stdin_open: true
    tty: true
    ```

## [Переменные в compose](https://docs.docker.com/compose/compose-file/compose-file-v3/#variable-substitution)

Поддерживается синтаксис `$VARIABLE` и `${VARIABLE}`. Кроме того, при использовании формата файла 2.1 можно указать встроенные значения по умолчанию, используя типичный синтаксис оболочки:

- `${VARIABLE:-default}` принимает значение по умолчанию, если `VARIABLE` не установлена или пуст в среде
- `${VARIABLE-default}` оценивается как значение по умолчанию, только если `VARIABLE` не установлен в среде

Точно так же следующий синтаксис позволяет указывать обязательные переменные:

- `${VARIABLE:?err}` завершается с сообщением об ошибке, содержащим `err`, если `VARIABLE` не установлена или пуста в среде
- `${VARIABLE?err}` завершается с сообщением об ошибке, содержащим ошибку, если `VARIABLE` не установлена в среде.

Другие расширенные функции оболочки, такие как `${VARIABLE/foo/bar}`, не поддерживаются.

Для использования знака `$` или экранирования переменных используйте `$$`

## [Дополнительные поля](https://docs.docker.com/compose/compose-file/compose-file-v3/#extension-fields)

Возможно повторное использование фрагментов конфигурации с помощью полей расширения. Эти специальные поля могут иметь любой формат, если они расположены в корне вашего файла Compose и их имена начинаются с последовательности символов x. Содержимое этих полей игнорируется Compose, но их можно вставить в определения ваших ресурсов с помощью привязок YAML. Привязки можно переопределять частично.

```yaml
version: "3.9"
x-volumes:
  &default-volume
  driver: foobar-storage

services:
  web:
    image: myapp/web:latest
    volumes: ["vol1", "vol2", "vol3"]
volumes:
  vol1: *default-volume
  vol2:
    << : *default-volume
    name: volume02
  vol3:
    << : *default-volume
    driver: default
    name: volume-local
```

Смотри еще:

- [[docker]]
- [[docker-compose]]
- [[docker-swarm]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[docker-swarm]: docker-swarm "Docker swarm"
[docker]: ../lists/docker "Docker"
[docker-compose]: docker-compose "Docker compose"
[docker-swarm]: docker-swarm "Docker swarm"
[//end]: # "Autogenerated link references"