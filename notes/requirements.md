---
description: Управление зависимостями в requirements.txt на python
title: Requirements.txt
tags: cli python
---
Управлят ьнесколькими рекуйрментами можно [так](https://stackoverflow.com/questions/17803829/how-to-customize-a-requirements-txt-for-multiple-environments/20720019#20720019):

```bash
`-- django_project_root
|-- requirements
|   |-- common.txt
|   |-- dev.txt
|   `-- prod.txt
`-- requirements.txt
```

`common.txt`

```shell
# Contains requirements common to all environments
req1==1.0
req2==1.0
req3==1.0
...
```

`dev.txt`

```shell
# Specifies only dev-specific requirements
# But imports the common ones too
-r common.txt
dev_req==1.0
...
```

`prod.txt`

```shell
# Same for prod...
-r common.txt
prod_req==1.0
...
```

За пределами [[[heroku]]] или другного деплоя

`pip install -r requirements/dev.txt` или `pip install -r requirements/prod.txt`

При деплое мы будем видеть только `requirements.txt`, а в нем:

```shell
# Mirrors prod
-r requirements/prod.txt
```

Более крупный аналог - [[poetry]]


[poetry]: poetry "Poetry"
