---
description: Тестирование с помощью функциональных тестов в pytest
tags: tests behave pip python
title: pytest-bdd
---
Pytest-bdd implements a subset of the [[gherkin]] language to enable automating project requirements testing and to facilitate behavioral driven development

## Пример проекта

`pip install pytest`
`pip install pytest-bdd`

Структура проекта

```bash
[project root directory]
|‐‐ [product code packages]
|-- [test directories]
|   |-- features
|   |   `-- *.feature
|   `-- step_defs
|       |-- __init__.py
|       |-- conftest.py
|       `-- test_*.py
`-- [pytest.ini|tox.ini|setup.cfg]
```

```gherkin
@web @duckduckgo
Feature: DuckDuckGo Web Browsing
  As a web surfer,
  I want to find information online,
  So I can learn new things and get tasks done.

  # The "@" annotations are tags
  # One feature can have multiple scenarios
  # The lines immediately after the feature title are just comments

  Scenario: Basic DuckDuckGo Search
    Given the DuckDuckGo home page is displayed
    When the user searches for "panda"
    Then results are shown for "panda"
```

Обратите внимание, что в файле feature допускается только одна feature.

```python
import pytest

from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Constants

DUCKDUCKGO_HOME = 'https://duckduckgo.com/'

# Scenarios

scenarios('../features/web.feature')

# Fixtures

@pytest.fixture
def browser():
    b = webdriver.Firefox()
    b.implicitly_wait(10)
    yield b
    b.quit()

# Given Steps

@given('the DuckDuckGo home page is displayed')
def ddg_home(browser):
    browser.get(DUCKDUCKGO_HOME)

# When Steps

@when(parsers.parse('the user searches for "{phrase}"'))
def search_phrase(browser, phrase):
    search_input = browser.find_element_by_id('search_form_input_homepage')
    search_input.send_keys(phrase + Keys.RETURN)

# Then Steps

@then(parsers.parse('results are shown for "{phrase}"'))
def search_results(browser, phrase):
    # Check search result list
    # (A more comprehensive test would check results for matching phrases)
    # (Check the list before the search phrase for correct implicit waiting)
    links_div = browser.find_element_by_id('links')
    assert len(links_div.find_elements_by_xpath('//div')) > 0
    # Check search phrase
    search_input = browser.find_element_by_id('search_form_input')
    assert search_input.get_attribute('value') == phrase
```

launch: `pytest tests/step_defs`

## [Более подробный пример](https://pytest-bdd.readthedocs.io/en/latest/#example)

Функции, декорированные как scenario, ведут себя как обычные тестовые функции и будут выполняться после всех шагов сценария. Рекомендуется по возможности помещать всю логику внутрь when, then и and.

Иногда приходится объявлять одни и те же установки или шаги разными именами для лучшей читабельности. Чтобы использовать одну и ту же пошаговую функцию с несколькими именами шагов, ее можно декорировать несколько раз. Указанные псевдонимы шагов являются независимыми и будут выполняться каждый раз при упоминании.

```python
@given("I have an article")
@given("there's an article")
def article(author, target_fixture="article"):
    return create_test_article(author=author)
```

Сами шаги можно использовать с разными параметрами повторно. При этом доступно несколько типов парсеров параметра шага:

- string (the default)
- parse (based on: pypi_parse) - предоставляет простой синтаксический анализатор, который заменяет регулярные выражения для параметров шага удобочитаемым синтаксисом, например `{param:Type}`. Синтаксис вдохновлен встроенной в Python функцией `string.format()`. Параметры шага должны использовать синтаксис именованных полей pypi_parse в определениях шага. Именованные поля извлекаются, дополнительно преобразуются типы, а затем используются в качестве аргументов функции шага. Поддерживает преобразования типов с помощью преобразователей типов, передаваемых через extra_types.
- cfparse (extends: pypi_parse, based on: pypi_parse_type) - предоставляет расширенный синтаксический анализатор с поддержкой «поля кардинальности» (CF)
- re

```python
# cparse example
from pytest_bdd import parsers

@given(
    parsers.cfparse("there are {start:Number} cucumbers", extra_types={"Number": int}),
    target_fixture="cucumbers",
)
def given_cucumbers(start):
    return {"start": start, "eat": 0}

# for re
@given(
    parsers.re(r"there are (?P<start>\d+) cucumbers"),
    converters={"start": int},
    target_fixture="cucumbers",
)
def given_cucumbers(start):
    return {"start": start, "eat": 0}
```

Кроме того,можно имплементировать собственные парсеры.

Иногда нужен такой заданный шаг, который обязательно менял бы фикстуру только для определенного теста (сценария), а для остальных тестов он оставался бы нетронутым. Для этого в given декораторе существует специальный параметр target_fixture. В этом примере существующая фикстура foo будет переопределена шагом только для сценария, в котором она используется.

```gherkin
Feature: Target fixture
    Scenario: Test given fixture injection
        Given I have injecting given
        Then foo should be "injected foo"
```

```python
from pytest_bdd import given

@pytest.fixture
def foo():
    return "foo"


@given("I have injecting given", target_fixture="foo")
def injecting_given():
    return "injected foo"


@then('foo should be "injected foo"')
def foo_is_foo(foo):
    assert foo == 'injected foo'
```

Как и Gherkin, pytest-bdd поддерживает многострочные шаги (также известные как строки документа). Но гораздо более чистым и мощным способом:

```gherkin
Feature: Multiline steps
    Scenario: Multiline step using sub indentation
        Given I have a step with:
            Some
            Extra
            Lines
        Then the text should be parsed with correct indentation
```

Шаг считается многострочным, если следующая(ые) строка(и) после первой строки имеет отступ относительно первой строки. Затем имя шага просто расширяется путем добавления дополнительных строк с символами новой строки. В приведенном выше примере имя заданного шага будет таким

`'I have a step with:\nSome\nExtra\nLines'`. Использоать это можно так:

```python
from pytest_bdd import given, then, scenario, parsers


scenarios("multiline.feature")


@given(parsers.parse("I have a step with:\n{content}"), target_fixture="text")
def given_text(content):
    return content


@then("the text should be parsed with correct indentation")
def text_should_be_correct(text):
    assert text == "Some\nExtra\nLines"
```

Если есть относительно большой набор файлов функций, вручную привязывать сценарии к тестам с помощью декоратора сценариев сложно. Конечно, при ручном подходе вы получаете все возможности, чтобы иметь возможность дополнительно параметризовать тест, дать тестовой функции красивое имя, задокументировать ее и т. д., но в большинстве случаев вам это не нужно. Вместо этого вы хотите рекурсивно автоматически связать все сценарии, найденные в папках функций, с помощью помощника сценариев. Вы можете передать несколько путей, и эти пути могут быть либо файлами функций, либо папками функций.

```python
from pytest_bdd import scenarios

# pass multiple paths/files
scenarios('features', 'other_features/some.feature', 'some_other_features')
```

Кроме того, сценарий можно привязать и декоратором

```python
from pytest_bdd import scenario, scenarios

@scenario('features/some.feature', 'Test something')
def test_something():
    pass

# assume 'features' subfolder is in this file's directory
scenarios('features')
```

Сценарии могут быть параметризованы для охвата нескольких случаев. В Gherkin они называются Scenario Outlines, а шаблоны переменных записываются с использованием угловых скобок (например, `<var_name>`).

```gherkin
# content of scenario_outlines.feature

Feature: Scenario outlines
    Scenario Outline: Outlined given, when, then
        Given there are <start> cucumbers
        When I eat <eat> cucumbers
        Then I should have <left> cucumbers

        Examples:
        | start | eat | left |
        |  12   |  5  |  7   |
```

```python
from pytest_bdd import scenarios, given, when, then, parsers


scenarios("scenario_outlines.feature")


@given(parsers.parse("there are {start:d} cucumbers"), target_fixture="cucumbers")
def given_cucumbers(start):
    return {"start": start, "eat": 0}


@when(parsers.parse("I eat {eat:d} cucumbers"))
def eat_cucumbers(cucumbers, eat):
    cucumbers["eat"] += eat


@then(parsers.parse("I should have {left:d} cucumbers"))
def should_have_left_cucumbers(cucumbers, left):
    assert cucumbers["start"] - cucumbers["eat"] == left
```

Организовать структуру тестов можно так:

```sh
features
│
├──frontend
│  │
│  └──auth
│     │
│     └──login.feature
└──backend
   │
   └──auth
      │
      └──login.feature

tests
│
└──functional
   │
   └──test_auth.py
      │
      └ """Authentication tests."""
        from pytest_bdd import scenario

        @scenario('frontend/auth/login.feature')
        def test_logging_in_frontend():
            pass

        @scenario('backend/auth/login.feature')
        def test_logging_in_backend():
            pass
```

Cucumber использует теги как способ классификации ваших функций и сценариев, которые поддерживает pytest-bdd.

```gherkin
@login @backend
Feature: Login

  @successful
  Scenario: Successful login
```

Теперь это можно запустить так: `pytest -m "backend and login and successful"`

Маркеры функций и сценариев не отличаются от стандартных маркеров pytest, а символ `@` автоматически удаляется, чтобы разрешить выражения селектора тестов. Если вы хотите, чтобы теги, связанные с bdd, отличались от других тестовых маркеров, используйте префикс, например `bdd`. Обратите внимание: если вы используете pytest с параметром `--strict`, все теги bdd, упомянутые в файлах функций, также должны быть в настройке маркеров конфигурации pytest.ini. Также для тегов используйте имена переменных, совместимые с python, т. е. начинайте не с числа, используйте только символы подчеркивания или буквенно-цифровые символы и т. д. Таким образом, вы можете безопасно использовать теги для фильтрации тестов. Вы можете настроить преобразование тегов в метки pytest, внедрив хук `pytest_bdd_apply_tag` и вернув из него True:

```python
def pytest_bdd_apply_tag(tag, function):
    if tag == 'todo':
        marker = pytest.mark.skip(reason="Not implemented yet")
        marker(function)
        return True
    else:
        # Fall back to the default behavior of pytest-bdd
        return None
```

Первоначальные установки теста осуществляется с помощью Given. Несмотря на то, что эти шаги выполняются в обязательном порядке для применения возможных побочных эффектов, pytest-bdd пытается извлечь выгоду из фикстур PyTest, которые основаны на внедрении зависимостей и делают настройку более декларативной.

```gherkin
Feature: The power of PyTest
    Scenario: Symbolic name across steps
        Given I have a beautiful article
        When I publish this article
        And my article is published
```

```python
@given("I have a beautiful article", target_fixture="article")
def article():
    return Article(is_beautiful=True)

@when("I publish this article")
def publish_article(article):
    article.publish()

@given("my article is published")
def published_article(article):
    article.publish()
    return article
```

pytest-bdd не зависит от глобального контекста и все установки теста можно определять в given.

Часто бывает так, что для охвата определенной функции вам потребуется несколько сценариев. И логично, что установка для этих сценариев будет иметь некоторые общие части. pytest-bdd реализует бекграунды для функций.

```python
Feature: Multiple site support

  Background:
    Given a global administrator named "Greg"
    And a blog named "Greg's anti-tax rants"
    And a customer named "Wilson"
    And a blog named "Expensive Therapy" owned by "Wilson"

  Scenario: Wilson posts to his own blog
    Given I am logged in as Wilson
    When I try to post to "Expensive Therapy"
    Then I should see "Your article was published."

  Scenario: Greg posts to a client's blog
    Given I am logged in as Greg
    When I try to post to "Expensive Therapy"
    Then I should see "Your article was published."
```

В разделе Background следует использовать только Given шаги. Шаги When и Then запрещены, потому что их цели связаны с действиями и потреблением результатов; что противоречит цели Background — подготовить систему к испытаниям или «привести систему в известное состояние», как это делает Given. Утверждение выше относится к строгому режиму Gherkin, который включен по умолчанию.

Steps и Given можно использовать повторно. Лучшее решение - определить реюзабельные фикстуры в `conftest`

```gherkin
# content of common_steps.feature

Scenario: All steps are declared in the conftest
    Given I have a bar
    Then bar should have value "bar"
```

```python
# content of conftest.py
from pytest_bdd import given, then


@given("I have a bar", target_fixture="bar")
def bar():
    return "bar"


@then('bar should have value "bar"')
def bar_is_bar(bar):
    assert bar == "bar"


# content of test_common.py
@scenario("common_steps.feature", "All steps are declared in the conftest")
def test_conftest():
    pass
```

Иногда у вас есть определения шагов, которые было бы гораздо проще автоматизировать, чем писать их вручную снова и снова. Это распространено, например, при использовании таких библиотек, как [pytest-factoryboy](https://pytest-factoryboy.readthedocs.io/en/stable/), которые автоматически создают фикстуры. Написание определений шагов для каждой модели может стать утомительной задачей. По этой причине pytest-bdd позволяет автоматически генерировать определения шагов. Хитрость заключается в том, чтобы передать параметр stacklevel в Given, When и т.д.. Это даст им указание внедрить фикстуры шага в соответствующий модуль, а не просто вставить их в кадр вызывающего объекта. [Пример тут](https://pytest-bdd.readthedocs.io/en/latest/#programmatic-step-generation)

Смотри еще:

- [документация](https://pytest-bdd.readthedocs.io/en/latest/)
- [репо](https://github.com/pytest-dev/pytest-bdd)
- [[gherkin]]
- [[behave]]
- [[pytest]]
- [[тестирование]]


[gherkin]: gherkin "Gherkin"
[behave]: behave "Behave"
[pytest]: pytest "Pytest"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
