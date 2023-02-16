---
description: Тестирование с использованием pytest на python
tags: tests pip python
title: Pytest
---
Библиотечка для [[модульные-тесты]]

[Документация](https://docs.pytest.org/en/stable/contents.html#toc)

[API - все методы пайтеста](https://docs.pytest.org/en/6.2.x/reference.html)

## [Usage](https://docs.pytest.org/en/6.2.x/usage.html)

```shell
pytest --version   # shows where pytest was imported from
pytest --fixtures  # show available builtin function arguments
pytest -h | --help # show help on command line and config file options

pytest -x           # stop after first failure
pytest --maxfail=2  # stop after two failures

# run selecting tests

pytest test_mod.py
pytest testing/ # all in one directory
pytest -k "MyClass and not method" # by keyword. The example above will run TestMyClass.test_something but not TestMyClass.test_method_simple

pytest test_mod.py::test_func # by functions name
pytest test_mod.py::TestClass::test_method # by method name
pytest -m slow # by mark, such a @pytest.mark.slow
pytest --pyargs pkg.testing # This will import pkg.testing and use its filesystem location to find and run tests from

# Modifying Python traceback printing

pytest --showlocals # show local variables in tracebacks
pytest -l           # show local variables (shortcut)

pytest --tb=auto    # (default) 'long' tracebacks for the first and last
                     # entry, but 'short' style for the other entries
pytest --tb=long    # exhaustive, informative traceback formatting
pytest --tb=short   # shorter traceback format
pytest --tb=line    # only one line per failure
pytest --tb=native  # Python standard library formatting
pytest --tb=no      # no traceback at all
```

Вывод саммари с отметкой pass/fail/skip `pytest -v`

[Можно запускать через](https://docs.pytest.org/en/6.2.x/usage.html#detailed-summary-report) `pytest -r`

Опции для запуска:

- f - failed
- E - error
- s - skipped
- x - xfailed
- X - xpassed
- p - passed
- P - passed with output

Выбор групп:

- a - all except passes (pP)
- A - all
- N - none, this can be used to display nothing (since fE is the default)

Пример `pytest -ra` или `[ytest -rfs`]

[Запуск](https://docs.pytest.org/en/6.2.x/usage.html#dropping-to-pdb-python-debugger-on-failures) с [[pdb-python-debugger]] `pytest --pdb` или `pytest --trace` (для запуска дебаггера в начале каждого теста).

[Запуск из кода](https://docs.pytest.org/en/6.2.x/usage.html#calling-pytest-from-python-code)

## [Написание ассертов](https://docs.pytest.org/en/6.2.x/assert.html)

### Тестирование неудачных случаев

Используется `pytest.raises()` с контекстным менеджером.

```python
import pytest
with pytest.raises(ZeroDivisionError):
    1/0
```

Или анлогично встроенным функциям [[unittest]]

```python
def myfunc():
    raise ValueError("Exception 123 raised")


def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
```

### [Определение собственных описаний для проваленных тестов](https://docs.pytest.org/en/6.2.x/assert.html#defining-your-own-explanation-for-failed-assertions)

Используется хук `pytest_assertrepr_compare(config: Config, op: str, left: object, right: object) → Optional[List[str]]`

```python
# content of conftest.py
from test_foocompare import Foo


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing Foo instances:",
            "   vals: {} != {}".format(left.val, right.val),
        ]

# content of test_foocompare.py
class Foo:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val


def test_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    assert f1 == f2
```

## [Фикстуры](https://docs.pytest.org/en/6.2.x/fixture.html)

Применяются с помощью декораторв `@pytest.fixture`. Доступно несколько дефолтных фикстур.

Почитать что такое [[фикстуры]]

В pytest «фикстуры» - это определяемые вами функции, которые служат цели задания условий теста. Они также могут предоставить шаг действия, и это может быть мощным методом для разработки более сложных тестов. Пример:

```python
class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)
```

Фикстуры можно выстраивать в зависимости

```python
# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]
```

С этим механизмом фикстуры легко становятся reusable

```python
# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]


def test_int(order):
    # Act
    order.append(2)

    # Assert
    assert order == ["a", 2]
```

Можно так-же запрашивать более одной фикстуры за разделе

```python
# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def second_entry():
    return 2


# Arrange
@pytest.fixture
def order(first_entry, second_entry):
    return [first_entry, second_entry]


# Arrange
@pytest.fixture
def expected_list():
    return ["a", 2, 3.0]


def test_string(order, expected_list):
    # Act
    order.append(3.0)

    # Assert
    assert order == expected_list
```

Кроме того, фикстуры можно вызвать более одного раза за тест, значение кешируется.

```python
# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order():
    return []


# Act
@pytest.fixture
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]
```

Можно сделать автоюзабельные фикстуры (тогда они будут применяться для всех тестов)

```python
@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return []


@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(order, first_entry):
    assert order == [first_entry]


def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]
```

[Мы можем пошарить фикстуры на классы, модули, пакеты и сессии](https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session)

```python
import pytest
import smtplib


@pytest.fixture(scope="module")
def smtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
```

```python
def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert b"smtp.gmail.com" in msg
    assert 0  # for demo purposes


def test_noop(smtp_connection):
    response, msg = smtp_connection.noop()
    assert response == 250
    assert 0  # for demo purposes
```

```shell
$ pytest test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 2 items

test_module.py FF                                                    [100%]

================================= FAILURES =================================
________________________________ test_ehlo _________________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
>       assert 0  # for demo purposes
E       assert 0

test_module.py:7: AssertionError
________________________________ test_noop _________________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
E       assert 0

test_module.py:13: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_ehlo - assert 0
FAILED test_module.py::test_noop - assert 0
============================ 2 failed in 0.12s =============================
```

Для scopes оступно:

- `function`: the default scope, the fixture is destroyed at the end of the test.
- `class`: the fixture is destroyed during teardown of the last test in the class.
- `module`: the fixture is destroyed during teardown of the last test in the module.
- `package`: the fixture is destroyed during teardown of the last test in the package.
- `session`: the fixture is destroyed at the end of the test session.

Кроме того, можно динамически

```python
def determine_scope(fixture_name, config):
    if config.getoption("--keep-containers", None):
        return "session"
    return "function"


@pytest.fixture(scope=determine_scope)
def docker_container():
    yield spawn_container()
```

[Errors фикстур](https://docs.pytest.org/en/6.2.x/fixture.html#fixture-errors)

### [Teardown/Cleanup (AKA Fixture finalization)](https://docs.pytest.org/en/6.2.x/fixture.html#teardown-cleanup-aka-fixture-finalization)

#### yield fixtures (recommended)

1. return is swapped out for yield.
2. Any teardown code for that fixture is placed after the yield

```python
import pytest

from emaillib import Email, MailAdminClient


@pytest.fixture
def mail_admin():
    return MailAdminClient()


@pytest.fixture
def sending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    admin_client.delete_user(user)


@pytest.fixture
def receiving_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    admin_client.delete_user(user)


def test_email_received(receiving_user, email):
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(_email, receiving_user)
    assert email in receiving_user.inbox
```

Все что записано после `yield` будет запускаться после выпаолнения теста, но в обратном порядке. Поскольку `receiving_user` последний, то сначала будет удален узер для него, затем для `sending_user`

#### [Прямая реализация финализирующей части](https://docs.pytest.org/en/6.2.x/fixture.html#adding-finalizers-directly)

#### [Безопасный тирдаун](https://docs.pytest.org/en/6.2.x/fixture.html#safe-teardowns)

```python
import pytest

from emaillib import Email, MailAdminClient


@pytest.fixture
def setup():
    mail_admin = MailAdminClient()
    sending_user = mail_admin.create_user()
    receiving_user = mail_admin.create_user()
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_emai(email, receiving_user)
    yield receiving_user, email
    receiving_user.delete_email(email)
    admin_client.delete_user(sending_user)
    admin_client.delete_user(receiving_user)


def test_email_received(setup):
    receiving_user, email = setup
    assert email in receiving_user.inbox
```

### [Обеспечение доступности фикстур на разных уровнях видимости](https://docs.pytest.org/en/6.2.x/fixture.html#fixture-availabiility)

### [Fixture instantiation order](https://docs.pytest.org/en/6.2.x/fixture.html#fixture-instantiation-order)

### [Running multiple assert statements safely](https://docs.pytest.org/en/6.2.x/fixture.html#running-multiple-assert-statements-safely)

### [Using markers to pass data to fixtures](https://docs.pytest.org/en/6.2.x/fixture.html#using-markers-to-pass-data-to-fixtures)

```python
@pytest.fixture
def fixt(request):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        # Handle missing marker in some way...
        data = None
    else:
        data = marker.args[0]

    # Do something with the data
    return data


@pytest.mark.fixt_data(42)
def test_fixt(fixt):
    assert fixt == 42
```

### [Factories as fixtures](https://docs.pytest.org/en/6.2.x/fixture.html#factories-as-fixtures)

### [Parametrizing fixtures](https://docs.pytest.org/en/6.2.x/fixture.html#parametrizing-fixtures)

Позволяет запустить серию тестов.

```python
import pytest
import smtplib

@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print("finalizing {}".format(smtp_connection))
    smtp_connection.close()
```

### Далее еще несколько разделов про использование меток, группировку фикстур и автоматическое выполнение

## [Использование меток для обозначения режимов запуска тестов](https://docs.pytest.org/en/6.2.x/mark.html#marking-test-functions-with-attributes)

Запускается через `pytest --markers`. По дефолту доступно:

- `usefixtures` - use fixtures on a test function or class
- `filterwarnings` - filter certain warnings of a test function
- `skip` - always skip a test function
- `skipif` - skip a test function if a certain condition is met
- `xfail` - produce an “expected failure” outcome if a certain condition is met
- `parametrize` - perform multiple calls to the same test function.

Метку можно зарегистрирповать в `pytest.ini`

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    serial
```

или в `pyproject.toml`

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
```

или через хук пайтеста

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )
```

## [Monkeypatching/mocking modules and environments](https://docs.pytest.org/en/6.2.x/monkeypatch.html)

`monkeypatch` фикстура позволяет безопасно добавлять/убирать атрибуты и объекты, а так-же менять `sys.path`

```python
monkeypatch.setattr(obj, name, value, raising=True)
monkeypatch.delattr(obj, name, raising=True)
monkeypatch.setitem(mapping, name, value)
monkeypatch.delitem(obj, name, raising=True)
monkeypatch.setenv(name, value, prepend=False)
monkeypatch.delenv(name, raising=True)
monkeypatch.syspath_prepend(path)
monkeypatch.chdir(path)
```

Все очищается, как только запрашивающая тестирующая функция завершает свою работу. Простой пример

```python
# contents of test_module.py with source code and the test
from pathlib import Path


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")
```

`monkeypatch.setattr` может использоваться для конструирования классов, которые возвращают объект вместо значений

```python
import requests


def get_json(url):
    """Takes a URL, and returns the JSON."""
    r = requests.get(url)
    return r.json()
```

```python
# import requests for the purposes of monkeypatching
import requests

# our app.py that includes the get_json() function
# this is the previous code block example
import app

# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = app.get_json("https://fakeurl")
    assert result["mock_key"] == "mock_response"
```

### [Global patch example: preventing “requests” from remote operations](https://docs.pytest.org/en/6.2.x/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations)

### [Monkeypatching environment variables](https://docs.pytest.org/en/6.2.x/monkeypatch.html#monkeypatching-environment-variables)

### [Monkeypatching dictionaries](https://docs.pytest.org/en/6.2.x/monkeypatch.html#monkeypatching-dictionaries)

## [Temporary directories and files](https://docs.pytest.org/en/6.2.x/tmpdir.html)

`tmp_path` позволяет создавать временные директории для теста

```python
CONTENT = "content"


def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 0
```

### [The tmp_path_factory fixture](https://docs.pytest.org/en/6.2.x/tmpdir.html#the-tmp-path-factory-fixture)

## [Capturing of the stdout/stderr output](https://docs.pytest.org/en/6.2.x/capture.html)

Можно задать методы получения стандартного вывода

```shell
pytest -s                  # disable all capturing
pytest --capture=sys       # replace sys.stdout/stderr with in-mem files
pytest --capture=fd        # also point filedescriptors 1 and 2 to temp file
pytest --capture=tee-sys   # combines 'sys' and '-s', capturing sys.stdout/stderr
                           # and passing it along to the actual sys.stdout/stderr
```

Можно использовать print() для дебаг

```python
def setup_function(function):
    print("setting up", function)


def test_func1():
    assert True


def test_func2():
    assert False
```

### [Accessing captured output from a test function](https://docs.pytest.org/en/6.2.x/capture.html#accessing-captured-output-from-a-test-function)

## [Warnings Capture](https://docs.pytest.org/en/6.2.x/warnings.html)

## [Doctest integration for modules and test files](https://docs.pytest.org/en/6.2.x/doctest.html)

[[doctest]]

## [Skip and xfail: dealing with tests that cannot succeed](https://docs.pytest.org/en/6.2.x/skipping.html)

- `skip` тест будет проскипан за исключением ряда условий
- `xfail` тест будет провлен за исключением ряда условий

```python
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...

# альтернатива
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

Скипать можно и на уровне модуля

```python
import sys
import pytest

if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)
```

### skipif

```python
import sys


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_function():
    ...
```

Можно шарить скипы между разными модулями.

Крмое того, можно проискпать все тесты модуля или класса в модуле:

```python
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls:
    def test_function(self):
        "will not be setup or run under 'win32' platform"
```

Кроме того, можно скипать тесты, [если невозможно заимпортить зависимости](https://docs.pytest.org/en/6.2.x/skipping.html#skipping-on-a-missing-import-dependency).

### [XFail: mark test functions as expected to fail](https://docs.pytest.org/en/6.2.x/skipping.html#xfail-mark-test-functions-as-expected-to-fail)

```python
@pytest.mark.xfail
def test_function():
    ...

# альтернатива
def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")

# или
def test_function2():
    import slow_module

    if slow_module.slow_function():
        pytest.xfail("slow_module taking too long")
```

Мы так-же можем задать несколько параметров

```python
@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function():

@pytest.mark.xfail(reason="known parser issue")
def test_function():
    ...

# можно задать ошибку, которая будет поднята
@pytest.mark.xfail(raises=RuntimeError)
def test_function():
    ...

@pytest.mark.xfail(run=False)
def test_function():
    ...

@pytest.mark.xfail(strict=True)
def test_function():
    ...
```

Проигнорить `xfail` можно так `pytest --runxfail`

Аналогом является `zpass`

[Скип, фейл и пас могут быть параметризованы](https://docs.pytest.org/en/6.2.x/skipping.html#skip-xfail-with-parametrize) для запуска в серии тестов

## [Parametrizing fixtures and test functions](https://docs.pytest.org/en/6.2.x/parametrize.html)

Используется для запуска серии тестов

```python
# content of test_expectation.py
import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

## [Cache: working with cross-testrun state](https://docs.pytest.org/en/6.2.x/cache.html)

Позволяет кешировать и выводить только определеныне тесты

- --lf, --last-failed - to only re-run the failures.
- --ff, --failed-first - to run the failures first and then the rest of the tests.

Мы можем сконфигурирровать следующий запуск тестов

```shell
pytest --last-failed --last-failed-no-failures all    # run all tests (default behavior)
pytest --last-failed --last-failed-no-failures none   # run no tests and exit
```

Очистить кеш `pytest --cache-clear`

## [unittest.TestCase Support](https://docs.pytest.org/en/6.2.x/unittest.html)

pytest саппортит запуск [[unittest]]. Из коробки это можно сделать так: `pytest tests`

Крмое того, пайтест автоматически коллектит `unittest.TestCase` сабклассы и их методы в  `test_*.py` или `*_test.py`. Кроме того, саппортятся:

- `@unittest.skip` style decorators;
- `setUp/tearDown`;
- `setUpClass/tearDownClass`;
- `setUpModule/tearDownModule`;

не саппортится load test протокол и сабтесты

В юниттестовых сабклассах саппортятся:

- Marks: skip, skipif, xfail;
- Auto-use fixtures;

Не работаюти (и никогда не будут):

- Fixtures (except for autouse fixtures);
- Parametrization;
- Custom hooks;

pytest fixtures [можно миксить](https://docs.pytest.org/en/6.2.x/unittest.html#mixing-pytest-fixtures-into-unittest-testcase-subclasses-using-marks) в `unittest.TestCase` сабклассы

```python
# we define a fixture function below and it will be "used" by
# referencing its name from tests

import pytest


@pytest.fixture(scope="class")
def db_class(request):
    class DummyDB:
        pass

    # set a class attribute on the invoking test context
    request.cls.db = DummyDB()
```

Теперь, если мы используем db_class, он будет вызван однажды для каждого теста и установит на уровне атрибута класса инстанс сласса DummyDB(). Он станет доступен в тесте юниттеста благодаря `cls`

```python
import unittest
import pytest


@pytest.mark.usefixtures("db_class")
class MyTest(unittest.TestCase):
    def test_method1(self):
        assert hasattr(self, "db")
        assert 0, self.db  # fail for demo purposes

    def test_method2(self):
        assert 0, self.db  # fail for demo purposes
```

`@pytest.mark.usefixtures("db_class")` проверяет, что db_class вызван только один раз для теста.

```shell
$ pytest test_unittest_db.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 2 items

test_unittest_db.py FF                                               [100%]

================================= FAILURES =================================
___________________________ MyTest.test_method1 ____________________________

self = <test_unittest_db.MyTest testMethod=test_method1>

    def test_method1(self):
        assert hasattr(self, "db")
>       assert 0, self.db  # fail for demo purposes
E       AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef>
E       assert 0

test_unittest_db.py:10: AssertionError
___________________________ MyTest.test_method2 ____________________________

self = <test_unittest_db.MyTest testMethod=test_method2>

    def test_method2(self):
>       assert 0, self.db  # fail for demo purposes
E       AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef>
E       assert 0

test_unittest_db.py:13: AssertionError
========================= short test summary info ==========================
FAILED test_unittest_db.py::MyTest::test_method1 - AssertionError: <conft...
FAILED test_unittest_db.py::MyTest::test_method2 - AssertionError: <conft...
============================ 2 failed in 0.12s =============================
```

### [Using autouse fixtures and accessing other fixtures](https://docs.pytest.org/en/6.2.x/unittest.html#using-autouse-fixtures-and-accessing-other-fixtures)

Иногда это полезно, когда мы хотим использовать фикстуру автоматически в данном контексте. Например мы можем так получить доступ к фикстурам временного пути и временных директорий

```python
import pytest
import unittest


class MyTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        tmpdir.chdir()  # change to pytest-provided temporary directory
        tmpdir.join("samplefile.ini").write("# testdata")

    def test_method(self):
        with open("samplefile.ini") as f:
            s = f.read()
        assert "testdata" in s
```

## [Running tests written for nose](https://docs.pytest.org/en/6.2.x/nose.html)

## [classic xunit-style setup](https://docs.pytest.org/en/6.2.x/xunit_setup.html)

## [Installing and Using plugins](https://docs.pytest.org/en/6.2.x/plugins.html)

```shell
pip install pytest-NAME
pip uninstall pytest-NAME
```

- `pytest-django`: write tests for django apps, using pytest integration.
- `pytest-twisted`: write tests for twisted apps, starting a reactor and processing deferreds from test functions.
- `pytest-cov`: coverage reporting, compatible with distributed testing
- `pytest-xdist`: to distribute tests to CPUs and remote hosts, to run in boxed mode which allows to survive segmentation faults, to run in looponfailing mode, automatically re-running failing tests on file changes.
- `pytest-instafail`: to report failures while the test run is happening.
- `pytest-bdd`: to write tests using behaviour-driven testing.
- `pytest-timeout`: to timeout tests based on function marks or global definitions.
- `pytest-pep8`: a --pep8 option to enable PEP8 compliance checking.
- `pytest-flakes`: check source code with pyflakes.
- `oejskit`: a plugin to run javascript unittests in live browsers.

[pytest-selenium](https://pytest-selenium.readthedocs.io/en/latest/index.html) - плугин для использования [[selenium]] в тестаХ

Узнать какие плагины установлены можно так: `pytest --trace-config`

## [Writing plugins](https://docs.pytest.org/en/6.2.x/writing_plugins.html)

## [Writing hook functions](https://docs.pytest.org/en/6.2.x/writing_plugins.html#writing-hook-functions)

## [Logging¶](https://docs.pytest.org/en/6.2.x/logging.html)

## [Пример хорошей интеграции в проект](https://docs.pytest.org/en/6.2.x/goodpractices.html)

## [[Flaky-tests]] [статья](https://docs.pytest.org/en/6.2.x/flaky.html)

## [pytest import mechanisms and sys.path/PYTHONPATH](https://docs.pytest.org/en/6.2.x/pythonpath.html)

## [Конфигурирование](https://docs.pytest.org/en/6.2.x/customize.html)

## [Примеры](https://docs.pytest.org/en/6.2.x/example/index.html)

Смотри [[pytest-parametrizing]]

Смотри еще:

- [[pytest-bdd]]
- [[pytest-asyncio]]
- [[unittest]]
- [[doctest]]
- [[env-for-test]]
- [[mock]]
- [[testfixtures]]
- [[pytest-parametrizing]]
- [pytest-bdd](https://github.com/pytest-dev/pytest-bdd) functional testing for pytest
- [[testinfra]]
- [[2022-07-04-daily-note]] how to get the current test's name from the setup method
- [[pydantic-factories]]
- [pytest tricks](https://hackebrot.github.io/pytest-tricks/)
- [[behave]]
- [pytest-factoryboy](https://pytest-factoryboy.readthedocs.io/en/stable/#) makes it easy to combine factory approach to the test setup with the dependency injection, heart of the pytest fixtures

Моки:

- [[faker]]
- [pytest-mock](https://github.com/pytest-dev/pytest-mock/)
- [aioresponses](https://github.com/pnuckowski/aioresponses). Aioresponses is a helper for mock/fake web requests in python [[aiohttp]] package
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio). Pytest support for [[asyncio]].

[//begin]: # "Autogenerated link references for markdown compatibility"
[модульные-тесты]: модульные-тесты "Модульные тесты"
[pdb-python-debugger]: pdb-python-debugger "Pdb python debugger"
[unittest]: unittest "Unittest"
[фикстуры]: фикстуры "Фикстуры"
[doctest]: doctest "Doctest"
[unittest]: unittest "Unittest"
[selenium]: selenium "Selenium"
[Flaky-tests]: flaky-tests "Flaky tests"
[pytest-parametrizing]: pytest-parametrizing "Pytest parametrizing tests python"
[pytest-bdd]: pytest-bdd "pytest-bdd"
[unittest]: unittest "Unittest"
[doctest]: doctest "Doctest"
[env-for-test]: env-for-test "Env variables for tests"
[mock]: mock "Mock-тесты"
[testfixtures]: testfixtures "Testfixtures"
[pytest-parametrizing]: pytest-parametrizing "Pytest parametrizing tests python"
[testinfra]: testinfra "Testinfra"
[2022-07-04-daily-note]: ../posts/2022-07-04-daily-note "Postgres Initialization scripts and unzip with init"
[pydantic-factories]: pydantic-factories "Pydantic-factories"
[behave]: behave "Behave"
[faker]: faker "Faker - пакет для создания фейковых данных для тестов"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[модульные-тесты]: модульные-тесты "Модульные тесты"
[pdb-python-debugger]: pdb-python-debugger "Pdb python debugger"
[unittest]: unittest "Unittest"
[фикстуры]: фикстуры "Фикстуры"
[doctest]: doctest "Doctest"
[unittest]: unittest "Unittest"
[selenium]: selenium "Selenium"
[Flaky-tests]: flaky-tests "Flaky tests"
[pytest-parametrizing]: pytest-parametrizing "Pytest parametrizing tests python"
[pytest-bdd]: pytest-bdd "pytest-bdd"
[pytest-asyncio]: pytest-asyncio "Pytest-asyncio"
[unittest]: unittest "Unittest"
[doctest]: doctest "Doctest"
[env-for-test]: env-for-test "Env variables for tests"
[mock]: mock "Mock-тесты"
[testfixtures]: testfixtures "Testfixtures"
[pytest-parametrizing]: pytest-parametrizing "Pytest parametrizing tests python"
[testinfra]: testinfra "Testinfra"
[2022-07-04-daily-note]: ../posts/2022-07-04-daily-note "Postgres Initialization scripts and unzip with init"
[pydantic-factories]: pydantic-factories "Pydantic-factories"
[behave]: behave "Behave"
[faker]: faker "Faker - пакет для создания фейковых данных для тестов"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"