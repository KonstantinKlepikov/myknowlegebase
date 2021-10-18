---
description: Docker swarm rock ненативная реализация swarm mode
tags: docker
---
# Docker swarm rocks

Используется для [[docker]] [swarm mode](https://docs.docker.com/engine/swarm/). 

[Основной материал](https://dockerswarm.rocks/). [Репозиторий](https://github.com/tiangolo/dockerswarm.rocks)

Фичи swarm mode:

- Cluster management integrated with Docker Engine
- Decentralized design
- Declarative service model
- Scaling
- Desired state reconciliation
- Multi-host networking
- Service discovery
- Load balancing:
- Secure by default
- Rolling updates

Для запуска [[docker-swarm]] mode нужно установить [[docker]] и [[docker-compose]]. Интеграция автоматическая. Можно запусчтить в кластере или как один сервер, что делает его удобным для запуска на единственном дроплете в [[digital-ocean]]

[Docker swarm rock](https://dockerswarm.rocks/) - не ассоциирован напрмую с [[docker]]. В проект включено несколько собственных идей.

[Установка описана там-же](https://dockerswarm.rocks/)

## [[traefik]] Proxy

[Traefik Proxy with HTTPS](https://dockerswarm.rocks/traefik/)

Зачем [[traefik]]?

- Handle connections.
- Expose specific services and applications based on their domain names.
- Handle multiple domains (if you need to). Similar to "virtual hosts".
- Handle HTTPS.
- Acquire (generate) HTTPS certificates automatically (including renewals) with Let's Encrypt.
- Add HTTP Basic Auth for any service that you need to protect and doesn't have its own security, etc.
- Get all its configurations automatically from Docker labels set in your stacks (you don't need to update configuration files).

Идея состоит в том, чтобы иметь основной балансировщик нагрузки/прокси, который охватывает весь кластер Docker Swarm и обрабатывает сертификаты и запросы HTTPS для каждого домена.

Но делая это таким образом, чтобы вы могли иметь другие службы Traefik внутри каждого стека, не мешая друг другу, для перенаправления на основе пути в том же стеке (например, один контейнер обрабатывает /api для веб-интерфейса, а другой обрабатывает /api для API в том же домене) или для выборочного перенаправления с HTTP на HTTPS.

Подробнее [тут](https://dockerswarm.rocks/traefik/)

### Подготовка

- Connect via SSH to a manager node in your cluster (you might have only one node) that will have the Traefik service.
- Create a network that will be shared with Traefik and the containers that should be accessible from the outside

```bash
docker network create --driver=overlay traefik-public
```

- Get the Swarm node ID of this node and store it in an environment variable

export NODE_ID=$(docker info -f '\{\{.Swarm.NodeID\}\}')

- Create a tag in this node, so that Traefik is always deployed to the same node and uses the same volume

```bash
docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID
```

- Create an environment variable with your email, to be used for the generation of Let's Encrypt certificates

```bash
export EMAIL=admin@example.com
```

- Create an environment variable with the domain you want to use for the Traefik UI (user interface)

```bash
export DOMAIN=traefik.sys.example.com
```

- You will access the Traefik dashboard at this domain, e.g. traefik.sys.example.com. So, make sure that your DNS records point the domain to one of the IPs of the cluster. Better if it is the IP where the Traefik service runs (the manager node you are currently connected to).
- Create an environment variable with a username (you will use it for the HTTP Basic Auth for Traefik and Consul UIs)

```bash
export USERNAME=admin
```

- Create an environment variable with the password

```bash
export PASSWORD=changethis
```

- Use openssl to generate the "hashed" version of the password and store it in an environment variable:

```bash
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
```

(Optional): Alternatively, if you don't want to put the password in an environment variable, you could type it interactively

```bash
export HASHED_PASSWORD=$(openssl passwd -apr1)
Password: $ enter your password here
Verifying - Password: $ re enter your password here
```

- You can check the contents with

```bash
echo $HASHED_PASSWORD
```

### Next, create `docker-compose.yml` file

- Download the file `traefik.yml`

```bash
curl -L dockerswarm.rocks/traefik.yml -o traefik.yml
```

or create it by `nano`

```bash
nano traefik.yml
```

Content

```yaml
version: '3.3'

services:

  traefik:
    # Use the latest v2.2.x Traefik image available
    image: traefik:v2.2
    ports:
      # Listen on port 80, default for HTTP, necessary to redirect to HTTPS
      - 80:80
      # Listen on port 443, default for HTTPS
      - 443:443
    deploy:
      placement:
        constraints:
          # Make the traefik service run only on the node with this label
          # as the node with it has the volume for the certificates
          - node.labels.traefik-public.traefik-public-certificates == true
      labels:
        # Enable Traefik for this service, to make it available in the public network
        - traefik.enable=true
        # Use the traefik-public network (declared below)
        - traefik.docker.network=traefik-public
        # Use the custom label "traefik.constraint-label=traefik-public"
        # This public Traefik will only use services with this label
        # That way you can add other internal Traefik instances per stack if needed
        - traefik.constraint-label=traefik-public
        # admin-auth middleware with HTTP Basic auth
        # Using the environment variables USERNAME and HASHED_PASSWORD
        - traefik.http.middlewares.admin-auth.basicauth.users=${USERNAME?Variable not set}:${HASHED_PASSWORD?Variable not set}
        # https-redirect middleware to redirect HTTP to HTTPS
        # It can be re-used by other stacks in other Docker Compose files
        - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
        - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
        # traefik-http set up only to use the middleware to redirect to https
        # Uses the environment variable DOMAIN
        - traefik.http.routers.traefik-public-http.rule=Host(`${DOMAIN?Variable not set}`)
        - traefik.http.routers.traefik-public-http.entrypoints=http
        - traefik.http.routers.traefik-public-http.middlewares=https-redirect
        # traefik-https the actual router using HTTPS
        # Uses the environment variable DOMAIN
        - traefik.http.routers.traefik-public-https.rule=Host(`${DOMAIN?Variable not set}`)
        - traefik.http.routers.traefik-public-https.entrypoints=https
        - traefik.http.routers.traefik-public-https.tls=true
        # Use the special Traefik service api@internal with the web UI/Dashboard
        - traefik.http.routers.traefik-public-https.service=api@internal
        # Use the "le" (Let's Encrypt) resolver created below
        - traefik.http.routers.traefik-public-https.tls.certresolver=le
        # Enable HTTP Basic auth, using the middleware created above
        - traefik.http.routers.traefik-public-https.middlewares=admin-auth
        # Define the port inside of the Docker service to use
        - traefik.http.services.traefik-public.loadbalancer.server.port=8080
    volumes:
      # Add Docker as a mounted volume, so that Traefik can read the labels of other services
      - /var/run/docker.sock:/var/run/docker.sock:ro
      # Mount the volume to store the certificates
      - traefik-public-certificates:/certificates
    command:
      # Enable Docker in Traefik, so that it reads labels from Docker services
      - --providers.docker
      # Add a constraint to only use services with the label "traefik.constraint-label=traefik-public"
      - --providers.docker.constraints=Label(`traefik.constraint-label`, `traefik-public`)
      # Do not expose all Docker services, only the ones explicitly exposed
      - --providers.docker.exposedbydefault=false
      # Enable Docker Swarm mode
      - --providers.docker.swarmmode
      # Create an entrypoint "http" listening on port 80
      - --entrypoints.http.address=:80
      # Create an entrypoint "https" listening on port 443
      - --entrypoints.https.address=:443
      # Create the certificate resolver "le" for Let's Encrypt, uses the environment variable EMAIL
      - --certificatesresolvers.le.acme.email=${EMAIL?Variable not set}
      # Store the Let's Encrypt certificates in the mounted volume
      - --certificatesresolvers.le.acme.storage=/certificates/acme.json
      # Use the TLS Challenge for Let's Encrypt
      - --certificatesresolvers.le.acme.tlschallenge=true
      # Enable the access log, with HTTP requests
      - --accesslog
      # Enable the Traefik log, for configurations and errors
      - --log
      # Enable the Dashboard and API
      - --api
    networks:
      # Use the public network created to be shared between Traefik and
      # any other service that needs to be publicly available with HTTPS
      - traefik-public

volumes:
  # Create a volume to store the certificates, there is a constraint to make sure
  # Traefik is always deployed to the same Docker node with the same volume containing
  # the HTTPS certificates
  traefik-public-certificates:

networks:
  # Use the previously created public network "traefik-public", shared with other
  # services that need to be publicly available via this Traefik
  traefik-public:
    external: true
```

### Deploy

```bash
docker stack deploy -c traefik.yml traefik
```

### Check

```bash
docker stack ps traefik
```

### Getting the client IP

If you need to read the client IP in your applications/stacks using the `X-Forwarded-For` or `X-Real-IP` headers provided by [[traefik]], you need to make Traefik listen directly, not through Docker Swarm mode, even while being deployed with Docker Swarm mode.

For that, you need to publish the ports using "host" mode.

So, the Docker Compose lines

```yaml
ports:
    - 80:80
    - 443:443
```

need to be

```yaml
ports:
    - target: 80
    published: 80
    mode: host
    - target: 443
    published: 443
    mode: host
```

You can use all the same instructions above, downloading the host-mode file

```bash
curl -L dockerswarm.rocks/traefik-host.yml -o traefik-host.yml
```

Or alternatively, copying it directly

```yaml
version: '3.3'

services:

  traefik:
    # Use the latest Traefik image
    image: traefik:v2.2
    ports:
      # Listen on port 80, default for HTTP, necessary to redirect to HTTPS
      - target: 80
        published: 80
        mode: host
      # Listen on port 443, default for HTTPS
      - target: 443
        published: 443
        mode: host
...
```

and then deploy

```bash
docker stack deploy -c traefik-host.yml traefik
```

В [[fastapi-template-backend]] деплой traefik реализован из коробки.

**Другие возможности:**

- [Swarmpit web user interface for your Docker Swarm cluster](https://dockerswarm.rocks/swarmpit/) ([swarmpit](https://swarmpit.io/))
- [Swarmprom for real-time monitoring and alerts](https://dockerswarm.rocks/swarmprom/)
- [Portainer web user interface for your Docker Swarm cluster](https://dockerswarm.rocks/portainer/)
- [The Lounge - self-hosted web IRC client](https://dockerswarm.rocks/thelounge/)
- [GitLab CI runner for CI/CD](https://dockerswarm.rocks/gitlab-ci/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[docker]: ../lists/docker "Docker"
[docker-swarm]: docker-swarm "Docker swarm"
[docker]: ../lists/docker "Docker"
[docker-compose]: docker-compose "Docker compose"
[digital-ocean]: ../lists/digital-ocean "Digital ocean"
[docker]: ../lists/docker "Docker"
[traefik]: traefik "Traefik"
[traefik]: traefik "Traefik"
[traefik]: traefik "Traefik"
[fastapi-template-backend]: fastapi-template-backend "Fastapi template backend"
[//end]: # "Autogenerated link references"