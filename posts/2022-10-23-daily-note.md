---
title: Screenshoots with pytests amd dataclass fields dynamicaly and literal choices
description: How to get screenshot with selenium and pytest, dataclass literal and dataclass dynamic fields
category: post
tags: tests python crawlers python-standart-library
---
## [Take screenshot of full page with Selenium Python with chromedriver](https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver)

## [How to capture screenshot on test case failure with PyTest](https://stackoverflow.com/questions/60205391/how-to-capture-screenshot-on-test-case-failure-with-pytest)

## [Dataclass argument choices with a default option](https://stackoverflow.com/questions/61756716/dataclass-argument-choices-with-a-default-option)

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class Person:
    name: Literal['Eric', 'John', 'Graham', 'Terry'] = 'Eric'
```

## [Dynamically add fields to dataclass objects](https://stackoverflow.com/questions/52534427/dynamically-add-fields-to-dataclass-objects)

```python
@dataclass
class X:
    i: int

x = X(i=42)
x.__class__ = make_dataclass('Y', fields=[('s', str)], bases=(X,))
x.s = 'text'

asdict(x)
# {'i': 42, 's': 'text'}
```

Смотри еще:

- [[pytest]]
- [[scrapy]]
- [[python-dataclasses]]


[pytest]: ../notes/pytest "Pytest"
[scrapy]: ../notes/scrapy "Scrapy"
[python-dataclasses]: ../notes/python-dataclasses "Python dataclasses"
