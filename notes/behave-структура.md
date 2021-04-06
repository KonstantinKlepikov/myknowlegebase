# [[behave]] структура

[Основыная статья в документации](https://behave.readthedocs.io/en/stable/tutorial.html)

Структура проекта

- app
  - features
    - steps
      - step.py
    - environment.py
    - step.feature
  - [...]

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

## Steps

**Given** помещаем систему в заранее заданное состояние прежде чем пользователь начнет что-то делать самостоятельно

**When** пользователь что-то делает - это приводит к определенным изменеениям

**Then** что-то происходит после действий пользователя, что мы должны так-же проверить

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

## Scenario Outlines

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
