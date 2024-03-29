---
description: Github action - управление и ci/cd на github
tags: cicd github
title: Githunb action
---
- [[2021-04-06-daily-note]] ссылки на разные ресурсы
- [[github-action-триггеры-и-переменные]]
- [[2021-08-27-daily-note]] про оркестрацию с docker и github
- Проблемы трансфера данных между github и [[digital-ocean-container-registry]] в этой заметке: [[2021-09-07-daily-note]]
- Про организацию workflow вот тут: [[workflow-types]]
- про [проблему доступа к данным](https://stackoverflow.com/questions/57830375/github-actions-workflow-error-permission-denied) в workflow,. Permission denied. [Еще ссылка](https://github.community/t/action-showing-permission-denied/134957)
- [[github-actions-links]] - как получить ссылку на экшен в workflow
- [[github-action-resources]]
- [[github-action-how-start-workflow-action-after-another-action]]
- [как получить специфический аутпут из steps](https://stackoverflow.com/a/59201610/15966204)

Полезные экшены:

- [Repository attributes](https://github.com/marketplace/actions/repository-attributes) - собирает атрибуты от предыдущего релиза до текущего
- [Action cache](https://github.com/actions/cache) - кэширование зависимостей, чтобы не тормозить по времени регулярный экшен. [Вот статья в доке](https://docs.github.com/en/actions/guides/caching-dependencies-to-speed-up-workflows)
- [Checkout](https://github.com/actions/checkout) - переключение в экшене между репами, ветками и т.д.
- [Building and testing Python](https://docs.github.com/en/actions/guides/building-and-testing-python) дока как билдить и тестить python app. [Тут](https://github.com/actions/starter-workflows/blob/dda42cb8f2514b6ee4e8cc0a860512821ffaa9f7/ci/python-app.yml) пример с [[flake8]]. [Экшен-1](https://github.com/py-actions/flake8), [экшен-2](https://github.com/reviewdog/action-flake8) (пока не использовал).
- [create envfile](https://github.com/KonstantinKlepikov/create-envfile)
- [action-gh-release](https://github.com/softprops/action-gh-release) - создаем релиз
- [release-action](https://github.com/ncipollo/release-action) - создаем релизы и аплоадим артефакты
- [action-gh-release](https://github.com/softprops/action-gh-release) - GitHub Action for creating GitHub Releases
- [SCP for GitHub Actions](https://github.com/appleboy/scp-action) - реализует [[linux-scp]] обмен файлами по ssh
- [Upload-Artifact v2](https://github.com/actions/upload-artifact) - шаринг данных между jobs и workflows
- [Public IP](https://github.com/haythem/public-ip) - This action allows you to whitelist the runner's address and remove it once the pipeline finishes
- [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) Some out-of-the-box hooks for pre-commit - некоторое кол-во хуков для [pre-commit](https://pre-commit.com/)
- [gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) GitHub Action, for publishing distribution files to PyPI
- [heroku-deploy](https://github.com/AkhileshNS/heroku-deploy) A simple github action that dynamically deploys an app to heroku
- [action-github-changelog-generator](https://github.com/heinrichreimer/action-github-changelog-generator) Automatically generate change log from your tags, issues, labels and pull requests on GitHub.
- [actions-gh-pages](https://github.com/peaceiris/actions-gh-pages). GitHub Actions for GitHub Pages

[actions-ecosystem/repositories](https://github.com/orgs/actions-ecosystem/repositories?type=all)

[[cl]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[2021-04-06-daily-note]: ../posts/2021-04-06-daily-note "Github actions - ссылки на различныек ресурсы"
[github-action-триггеры-и-переменные]: github-action-%D1%82%D1%80%D0%B8%D0%B3%D0%B3%D0%B5%D1%80%D1%8B-%D0%B8-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5 "Github action триггеры и переменные - документация и полезные ссылки"
[2021-08-27-daily-note]: ../posts/2021-08-27-daily-note "Как добавить контейнеры на Digital Ocean registry с помощью docker-compose"
[digital-ocean-container-registry]: digital-ocean-container-registry "Digital ocean container registry"
[2021-09-07-daily-note]: ../posts/2021-09-07-daily-note "Как устроен github packages, подводные камни интеграции с digital ocean и другими сервисами"
[workflow-types]: workflow-types "Про варианты git workflow"
[github-actions-links]: github-actions-links "Ссылка на версию экшена"
[github-action-resources]: github-action-resources "Github actions resources"
[github-action-how-start-workflow-action-after-another-action]: github-action-how-start-workflow-action-after-another-action "How start second github action after success first"
[flake8]: flake8 "Flake8"
[linux-scp]: linux-scp "Linux-scp"
[cl]: cl "ci/cd - непрервыная интеграция"
[//end]: # "Autogenerated link references"