# Pytest parametrizing tests

[Основная статья](https://docs.pytest.org/en/6.2.x/example/parametrize.html)

```python
# content of test_time.py

import pytest

from datetime import datetime, timedelta

testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]


@pytest.mark.parametrize("a,b,expected", testdata)
def test_timedistance_v0(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
def test_timedistance_v1(a, b, expected):
    diff = a - b
    assert diff == expected


def idfn(val):
    if isinstance(val, (datetime,)):
        # note this wouldn't show any hours/minutes/seconds
        return val.strftime("%Y%m%d")


@pytest.mark.parametrize("a,b,expected", testdata, ids=idfn)
def test_timedistance_v2(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        pytest.param(
            datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1), id="forward"
        ),
        pytest.param(
            datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1), id="backward"
        ),
    ],
)
def test_timedistance_v3(a, b, expected):
    diff = a - b
    assert diff == expected
```

С `--collect-only` покажет сгенерированные айдищники тестов. С помощью `-k` их можно вызвать.

Иногда есть смысл использовать [непрямую параметризацию](https://docs.pytest.org/en/6.2.x/example/parametrize.html#indirect-parametrization), например когда параметры должны быть вычислены на лету при вызове теста

```python
import pytest


@pytest.fixture
def fixt(request):
    return request.param * 3


@pytest.mark.parametrize("fixt", ["a", "b"], indirect=True)
def test_indirect(fixt):
    assert len(fixt) == 3
```

Параметризацмя решается в рамках [[pytest]]. Если нужно имплеметировать в [[unittest]] стиле, то есть [такое решение](https://pypi.org/project/testscenarios/). Использование параметризирования с другими декораторами может быть сложным: [тут пример](https://stackoverflow.com/a/67477929/15966204). Мне не удалось реализовать случай, когда тест является методом.