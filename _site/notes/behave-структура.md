# behave структура

[Основыная статья в документации](https://behave.readthedocs.io/en/stable/tutorial.html)

Структура проекта [[behave]]

```bash
- app
  - features
    - steps
      - step.py
    - environment.py
    - step.feature
  - [...]
```

В `environment.py` мы утанавливаем страт/остановку сервера и другие регулярные штуки для каждого теста. в `.feature` файлах пишем тест на [[gherkin]]

## Features

1. Реализует бизнес-логику
2. Шаги соответствуют #python функциям, тестирующим сценарий

```gherkin
Feature: showing off behave

  Scenario: run a simple test
     Given we have behave installed
      When we implement a test
      Then behave will test it for us!
```

Пример организации

> features/
> features/signup.feature
> features/login.feature
> features/account_details.feature
> features/environment.py
> features/steps/
> features/steps/website.py
> features/steps/utils.py

## Scenarios

[Основная страница](https://behave.readthedocs.io/en/stable/gherkin.html)

### Background steps

```gherkin
@tags @tag
Feature: feature name
  description
  further description

  Background: some requirement of this test
    Given some setup condition
      And some other setup action

  Scenario: some scenario
      Given some condition
       When some action is taken
       Then some result is expected.

  Scenario: some other scenario
      Given some other condition
       When some action is taken
       Then some other result is expected.
```

В бекграунд обычно помещается что-то, что необходимо зааффектить перед стартом основных шагов сценария. Например логирование или развертку базы данных.

- не спользовать **background** для натсройки сложных стейтментов
- сделть этот раздел максимально коротким
- использовать яркие имена и близкие к юзеру термины, а не символические привязки типа user 1

### Scenario

Включает в себя несколько шагов

```gherkin
Scenario: we have some stock when we open the store
  Given that the store has just opened
   then we should have items for sale.
```

### Scenario Outlines

Используется для запуска нескольких тестирующих примеров. Тест будет запущен отдельно для каждой строки

```gherkin
Scenario Outline: Blenders
   Given I put <thing> in a blender,
    when I switch the blender on
    then it should transform into <other thing>

 Examples: Amphibians
   | thing         | other thing |
   | Red Tree Frog | mush        |

 Examples: Consumer Electronics
   | thing         | other thing |
   | iPhone        | toxic waste |
   | Galaxy Nexus  | toxic waste |
```

[[daily-note-2021-04-02]] пример работы с таблицами

[Дока по таблицам](https://behave.readthedocs.io/en/stable/api.html#behave.model.Table)

### Other steps

**Given** помещаем систему в заранее заданное состояние прежде чем пользователь начнет что-то делать самостоятельно

**When** пользователь что-то делает - это приводит к определенным изменениям

**Then** что-то происходит после измененеий, что можем увидеть мы, пользователь или другие пользователи в каких-то местах, напирмер в вимде сообщеинй или отображений на экране

**And** и **But** подразумевают теже шаги, под которыми использованы эти термины.

```gherkin
Feature: Fight or flight
  In order to increase the ninja survival rate,
  As a ninja commander
  I want my ninjas to decide whether to take on an
  opponent based on their skill levels

  Scenario: Weaker opponent
    Given the ninja has a third level black-belt
     When attacked by a samurai
     Then the ninja should engage the opponent

  Scenario: Stronger opponent
    Given the ninja has a third level black-belt
     When attacked by Chuck Norris
     Then the ninja should run for his life
```

```gherkin
Scenario: Stronger opponent
  Given the ninja has a third level black-belt
   When attacked by Chuck Norris
   Then the ninja should run for his life
    And fall off a cliff
```

## Step data

Следующие строки будут доступны в имплементации через `context.text`

```gherkin
Scenario: some scenario
  Given a sample text loaded into the frobulator
     """
     Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
     eiusmod tempor incididunt ut labore et dolore magna aliqua.
     """
 When we activate the frobulator
 Then we will find it similar to English
 ```

 Другой вариант - использовать таблицу внутри шага, если нужно протестировать несколько состояний. Таблица будет доступна в виде списка словарей через атрибут `context.table`

```gherkin
 Scenario: some scenario
  Given a set of specific users
     | name      | department  |
     | Barry     | Beer Cans   |
     | Pudey     | Silly Walks |
     | Two-Lumps | Silly Walks |

 When we count the number of people in each department
 Then we will find two people in "Silly Walks"
  But we will find one person in "Beer Cans"
```

```python
@given('a set of specific users')
def step_impl(context):
    for row in context.table:
        model.add_user(name=row['name'], department=row['department'])
```

## Python Step Implementations

Шаги идентифицируются по декоратору **given**, **when**, **then** и **step**. Декоратор должен содержать строку шага. Название функции может не буть уникальным, т.к. функция регистрируется и матчится перед ее вызовом.

```gherkin
Scenario: Search for an account
   Given I search for a valid account
    Then I will see the account details
```

```python
@given('I search for a valid account')
def step_impl(context):
    context.browser.get('http://localhost:8000/index')
    form = get_element(context.browser, tag='form')
    get_element(form, name="msisdn").send_keys('61415551234')
    form.submit()

@then('I will see the account details')
def step_impl(context):
    elements = find_elements(context.browser, id='no-account')
    eq_(elements, [], 'account not found')
    h = get_element(context.browser, id='account-head')
    ok_(h.text.startswith("Account 61415551234"),
        'Heading %r has wrong text' % h.text)
```

Внутри имплементации шага можно вызвать другие шаги за счет метода `execute_steps()`

```gherkin
@when('I do the same thing as before')
def step_impl(context):
    context.execute_steps('''
        when I press the big red button
         and I duck
    ''')
```

## Step Parameters

В описании

```gherkin
Scenario: look up a book
  Given I search for a valid book
   Then the result page will include "success"

Scenario: look up an invalid book
  Given I search for a invalid book
   Then the result page will include "failure"
```

в имплементации (при условии, что в **Given** мы определили `context.response`)

```python
@then('the result page will include "{text}"')
def step_impl(context, text):
    if text not in context.response:
        fail('%r not in %r' % (text, context.response))
```

Варианты имплеменаций

- `parse (the default, based on: parse)` - синтаксис `{param:Type}`
- `cfparse (extends: parse, requires: parse_type)` - extended parser with “Cardinality Field” (CF) support

> {values:Type+} (cardinality=1..N, many)
> {values:Type*} (cardinality=0..N, many0)
> {value:Type?} (cardinality=0..1, optional)

= `re` - регулярки типа `“(?P<name>…)”`, чтобы выбрать определенные данные из текста, которые мы дали на этапе задания шагов. Типы не поддерживает

[use_step_matcher()](https://behave.readthedocs.io/en/stable/api.html#behave.use_step_matcher) задает тип парсера (там же смотри про типы данных)

## Context

Собирает информацию от старта до окончания теста. Можно использовать как дефолтные атрибуты, так и собственные.

```python
@given('I request a new widget for an account via SOAP')
def step_impl(context):
    client = Client("http://127.0.0.1:8000/soap/")
    context.response = client.Allocate(customer_first='Firstname',
        customer_last='Lastname', colour='red')

@then('I should receive an OK SOAP response')
def step_impl(context):
    eq_(context.response['ok'], 1)
```

Дефолтные

- table
- text
- failed

## Environmental Controls

Поозволяет задать настройки до запуска и после теста.

- `before_step(context, step), after_step(context, step)` для каждого шага
- `before_scenario(context, scenario), after_scenario(context, scenario)` для каждого сценария
- `before_feature(context, feature), after_feature(context, feature)` для каждого feature файла
- `before_tag(context, tag), after_tag(context, tag)` для тегов
- `before_all(context), after_all(context)` для любых объектов

.feature сценарий и step объект имеют аттрибуты:

- `keyword` - “Feature”, “Scenario”, “Given”, etc.
- `name` - имя шага (текст после ключевого слова)
- `tags` - теги
- `filename` and `line` - имя файла теста и номер состояния

Пример использования:

```python
# -- FILE: features/environment.py
from behave import fixture, use_fixture
from behave4my_project.fixtures import wsgi_server
from selenium import webdriver

@fixture
def selenium_browser_chrome(context):
    # -- HINT: @behave.fixture is similar to @contextlib.contextmanager
    context.browser = webdriver.Chrome()
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()

def before_all(context):
    use_fixture(wsgi_server, context, port=8000)
    use_fixture(selenium_browser_chrome, context)
    # -- HINT: CLEANUP-FIXTURE is performed after after_all() hook is called.

def before_feature(context, feature):
    model.init(environment='test')
```

```python
# -- FILE: behave4my_project/fixtures.py
# ALTERNATIVE: Place fixture in "features/environment.py" (but reuse is harder)
from behave import fixture
import threading
from wsgiref import simple_server
from my_application import model
from my_application import web_app

@fixture
def wsgi_server(context, port=8000):
    context.server = simple_server.WSGIServer(('', port))
    context.server.set_app(web_app.main(environment='test'))
    context.thread = threading.Thread(target=context.server.serve_forever)
    context.thread.start()
    yield context.server
    # -- CLEANUP-FIXTURE PART:
    context.server.shutdown()
    context.thread.join()
```

## tags

```gherkin
Feature: Fight or flight
  In order to increase the ninja survival rate,
  As a ninja commander
  I want my ninjas to decide whether to take on an
  opponent based on their skill levels

  @slow
  Scenario: Weaker opponent
    Given the ninja has a third level black-belt
    When attacked by a samurai
    Then the ninja should engage the opponent

  @whip
  Scenario: Stronger opponent
    Given the ninja has a third level black-belt
    When attacked by Chuck Norris
    Then the ninja should run for his life
```

`behave --tags=slow1` запустит только сценарий с тегом `@slow`

Еще варианты:

- `--tags=wip,slow` оба тега
- `--tags=wip --tags=slow` при условии, что шаг тегирован обоими тегами

Теги доступны в качестве аттрибутов в окружении, что позволяет задавать запуск специфических скриптов для специфических случаев по тегу

```python
# -- FILE: features/environment.py
# HINT: Reusing some code parts from above.
...

def before_feature(context, feature):
    model.init(environment='test')
    if 'browser' in feature.tags:
        use_fixture(wsgi_server, context)
        use_fixture(selenium_browser_chrome, context)
```

## work in progress

Флаг -w отключает логирование и вывод теста в консоль. Запускаются только сценарии с тегом `@wip`. Тест останавливается на первой ошибке. Раболтают самописныек логи типа

```python
if not context.config.log_capture:
    logging.basicConfig(level=logging.DEBUG)
```

## Fixtures

[Подробная статья](https://behave.readthedocs.io/en/stable/fixtures.html)

Фикстуры содержат yield-состояния, которые очищаются, когда удаляется `context` (после сценария, запуска фичи и т.д., в зависимости от того, когда фикстуры применяются)

```python
# -- FILE: behave4my_project/fixtures.py (or: features/environment.py)
from behave import fixture
from somewhere.browser import FirefoxBrowser

@fixture(name="fixture.browser.firefox")
def browser_firefox(context, *args, **kwargs):
    # -- SETUP-FIXTURE PART:
    context.browser = FirefoxBrowser(*args, **kwargs)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.shutdown()

# -- FILE: features/environment.py
from behave import use_fixture
from behave4my_project.fixtures import browser_firefox

def before_tag(context, tag):
    if tag == "fixture.browser.firefox":
        use_fixture(browser_firefox, context, timeout=10)
```

Параметры фикстур:

- fixture_func
- context
- fixture_kwargs
- fxture_kwargs

## Debug-on-Error (in Case of Step Failures)

Чтобы не захламлять вывод в консоль мусором ошибок, можно логировать, проще всего через `after_step()`

Пример

```python
# -- FILE: features/environment.py
# USE: behave -D BEHAVE_DEBUG_ON_ERROR         (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=yes     (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=no      (to disable debug-on-error)

BEHAVE_DEBUG_ON_ERROR = False

def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")

def before_all(context):
    setup_debug_on_error(context.config.userdata)

def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
```

[//begin]: # "Autogenerated link references for markdown compatibility"
[behave]: behave "behave"
[gherkin]: gherkin "gherkin"
[daily-note-2021-04-02]: ../journal/daily-note-2021-04-02 "Daily note,  2021-04-02, Friday"
[//end]: # "Autogenerated link references"