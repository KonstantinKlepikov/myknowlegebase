---
description: Генератор python проектов
title: Cookiecutter
tags: templating
---

[Документация](https://cookiecutter.readthedocs.io/en/stable/index.html#)

## Проекты - шаблонизаторы

### [CookieTemple](https://cookietemple.readthedocs.io/en/latest/)

- Dependency Management
  - [[poetry]]
- Documentation
  - Sphinx
  - Darglint to manage documentation linting
- Testing
  - [[pytest]]
  - Nox for cross platform testing
  - Codecoverage.yml for managing coverage
- [[github]]
  - Pull request
  - Feature request
  - Bug
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - updating docs
    - Dependabot dependency upgrades
    - syncs the project with their template updates as well
    - Has master branch protection enabled
    - Uses Pre-commit to fix everything before you push to GitHub
- [[makefile]]
  - Separate for Windows and Linux
- [[docker]] Dockerfile
  - Very basic, uses alpine Python distribution
- Type checking
  - [[mypy]]
- Security
  - Bandit for scanning vulnerabilities
- Other stuff
  - [[flake8]]
  - black
  - isort

### [CookieCutter Poetry](https://github.com/fpgmaas/cookiecutter-poetry)

- Dependency Management
  - [[poetry]]
- Documentation
  - MkDocs with Material Theme
  - ❌ No Darglint
- Testing
  - [[pytest]]
  - [[tox]] for cross platform testing
  - ❌ No Codecoverage
- [[github]]
  - Pull request
  - Feature request
  - Bug
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - updating docs
    - ❌ No Dependabot
    - ❌ No master branch protection enabled
    - ❌ Doesn't have Pre-Commit
- [[makefile]]
  - ❌ Not separate for Windows and Linux
- [[docker]] Dockerfile
  - ✅ Much better Dockerfile than cookietemple above, highly optimized
- Type checking
  - [[mypy]]
- Security
  - ❌ No sign of Bandit here
- Other stuff
  - [[flake8]]
  - black
  - isort

### [Wolt Python Package Cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter)

- Dependency Management
  - [[poetry]]
- Documentation
  - MkDocs Material (Both the above projects had a lot more into their documentation than this one)
  - ❌ No Darglint
  - ✅ This one has something both of the above ones dont. It is using python-kacl to automatically manage CHANGELOG
- Testing
  - [[pytest]]
  - ❌ No sign of [[tox]] or Nox
  - Codecoverage.yml for managing coverage
- [[github]]
  - Pull request
  - ❌ No Feature request Template
  - ❌ No Bug Template
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - updating docs
    - ❌ No Dependabot for dependency upgrades. Manages them manually which I think is not a good idea.
    - ❌ No master branch protection
    - Uses Pre-commit to fix everything before you push to GitHub
- ❌ No Makefile
- ❌ No Dockerfile
- Type checking
  - [[mypy]]
- Security
  - ❌ No Bandit
- Other stuff
  - [[flake8]]
  - black
  - isort
  - Uses cruft to keep templates automatically upto date

### [Python Project Template By Rucha Bruno](https://github.com/rochacbruno/python-project-template)

- Dependency Management
  - ✅ Uses setup tools by default but you can switch to [[puetry]] if you want
- Documentation
  - MkDocs
  - ❌ No sign of Darglint
  - ✅ This one also manages CHANGELOG automatically using gitchangelog
- Testing
  - [[pytest]]
  - No need for nox or [[tox]] in this one as they are manually testing it on each OS using the matrix strategy
  - Codecoverage.yml for managing coverage
- [[github]]
  - Pull request
  - Feature request
  - Bug
  - ✅ Adds a funding page too
  - [[github-action]]
    - lint
    - release
    - testing
    - publishing package on PyPi
    - ❌ Coudnt find where docs are getting updated
    - ❌ No sign of dependabot
    - ❌ No master branch protection
    - ❌ No sign of precommit
- [[makefile]]
  - ❌ Not separate for Windows and Linux
- Containerfile
  - Instead of a Dockerfile it uses the open standards Containerfile, very basic
- Type checking
  - [[mypy]]
- Security
  - ❌ No sign of Bandit
- Other stuff
  - [[flake8]]
  - black
  - isort

[source](https://www.reddit.com/r/Python/comments/vnh8od/here_are_5_python_project_starter_templates_after/)

Смотри еще:

- [[шаблонизаторы]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[poetry]: poetry "Poetry"
[pytest]: pytest "Pytest"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[makefile]: makefile "Makefile"
[docker]: ../lists/docker "Docker"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[poetry]: poetry "Poetry"
[pytest]: pytest "Pytest"
[tox]: tox "Tox"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[makefile]: makefile "Makefile"
[docker]: ../lists/docker "Docker"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[poetry]: poetry "Poetry"
[pytest]: pytest "Pytest"
[tox]: tox "Tox"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[pytest]: pytest "Pytest"
[tox]: tox "Tox"
[github]: ../tag/github "Tag: github"
[github-action]: github-action "Githunb action"
[makefile]: makefile "Makefile"
[mypy]: mypy "Mypy"
[flake8]: flake8 "Flake8"
[шаблонизаторы]: ../lists/шаблонизаторы "Шаблонизаторы"
[//end]: # "Autogenerated link references"