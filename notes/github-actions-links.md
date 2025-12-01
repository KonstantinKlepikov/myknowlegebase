---
description: Как в github action получить ссылку на определенный вариант экшена в workflow
tags: cicd github
title: Ссылка на версию экшена
---
Не обязательно юзать экшен из магазина для [[github-action]]. Можно написать свой, форкнуть чей-то, внести изменеения и т.д. [Вот статья об этом](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstepsuses)

Вот такие ссылки можно использовать:

```yml
steps:
  # Reference a specific commit
  - uses: actions/checkout@a81bbbf8298c0fa03ea29cdc473d45769f953675
  # Reference the major version of a release
  - uses: actions/checkout@v2
  # Reference a specific version
  - uses: actions/checkout@v2.2.0
  # Reference a branch
  - uses: actions/checkout@main
  ```


[github-action]: github-action "Githunb action"
