---
description: Линтер для python
type: feature
keywords: python
---

# flake8

Линтер для python. [Ссылка на документацию](https://flake8.pycqa.org/en/latest/index.html)

## Using Flake8

```bash
flake8 path/to/code/to/check.py
# or
flake8 path/to/code/
```

If you only want to see the instances of a specific warning or error, you can select that error like so

```bash
flake8 --select E123,W503 path/to/code/
```

or ignore

```bash
flake8 --ignore E24,W504 path/to/code/
```

[Все опции](https://flake8.pycqa.org/en/latest/user/options.html)
