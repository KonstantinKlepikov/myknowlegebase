# Daily note,  2021-04-02, Friday

## Интеграция [[behave]] и [[unittest]]

[Статья](https://stackoverflow.com/questions/35286430/integrating-behave-or-lettuce-with-python-unittest)

> [[nose]] includes a package that takes all the class-based asserts that unittest provides and turns them into plain functions, the module's documentation states:
> The nose.tools module provides [...] all of the same assertX methods found in unittest.TestCase (only spelled in PEP 8#function-names fashion, so assert_equal rather than assertEqual).
> For instance:

```python
from nose.tools import assert_equal

@given("foo is 'blah'")
def step_impl(context):
    assert_equal(context.foo, "blah")
```

## Пример работы с таблицами в [[behave]]

[ссылка](https://jenisys.github.io/behave.example/tutorials/tutorial10.html)

```behave
  Scenario Outline: Calculator
    Given I have a calculator
    When I add "<x>" and "<y>"
    Then the calculator returns "<sum>"

    Examples:
        |  x  |  y | sum |
        |  1  |  1 |  2  |
        |  1  |  2 |  3  |
        |  2  |  1 |  3  |
        |  2  |  7 |  9  |
...

  Scenario Outline: Calculator -- @1.1  
    Given I have a calculator            
    When I add "1" and "1"               
    Then the calculator returns "2"     

  Scenario Outline: Calculator -- @1.2   
    Given I have a calculator            
    When I add "1" and "2"               
    Then the calculator returns "3"      

  Scenario Outline: Calculator -- @1.3   
    Given I have a calculator           
    When I add "2" and "1"               
    Then the calculator returns "3" 

  Scenario Outline: Calculator -- @1.4
    Given I have a calculator        
    When I add "2" and "7"              
    Then the calculator returns "9"  
```

Еще: как лучше организовать тестирование респонза с [[behave]]

[ссылка](https://stackoverflow.com/questions/50627578/specify-behave-table-row-data-type)

```behave
Given I have a valid client auth token
And I request a user with an unknown "valid" uuid
Then I should get user not found response
```

вместо

```behave
Given I have a valid client auth token
And I request a user with an unknown "valid" uuid
And I get the response json
Then the expected fields should contain expected content
| field      | content               |
| statusCode | 404                   |
| error      | Not Found             |
| message    | User record not found |
```

- a simple scenario
- no table processing for your scenario
- a method you can reuse in other scenarios where a user is not found
- much lower cost of change if for example you want to ad another field to the response.

## [[datatime]] без микросекунд

[ссылка](https://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component)

```python
>>> datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
'2011-11-03 18:21:26'
```

## сдежу.щий понедельник в [[datatime]] 

[ссылка](https://overcoder.net/q/17889/%D0%BD%D0%B0%D0%B9%D1%82%D0%B8-%D0%B4%D0%B0%D1%82%D1%83-%D0%BF%D0%BE%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D0%BA%D0%B0-%D1%81-python)

```python
м>>> import datetime
>>> today = datetime.date.today()
>>> today + datetime.timedelta(days=-today.weekday(), weeks=1)
datetime.date(2009, 10, 26)
```