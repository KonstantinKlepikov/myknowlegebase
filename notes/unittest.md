---
description: Тестирование с помозью unittest в python
tags: tests python
title: Unittest
---
Поддерживает все концепции тестирующего программного комплекса, описанного в [[тестирование]]

[Опции командной строки](https://docs.python.org/3/library/unittest.html#command-line-options)

`python -m unittest -v test_module` с детализацией в отчете

`--locals` показать локальные переменные в выводе теста

[Test discovery](https://docs.python.org/3/library/unittest.html#test-discovery) позволяет задать путь, с которого начинается поиск тестов. Кроме того, можно установить паттерн наименований тестов.

## Структура кода

```python
import unittest

class DefaultWidgetSizeTestCase(unittest.TestCase):
    def test_default_widget_size(self):
        widget = Widget('The widget')
        self.assertEqual(widget.size(), (50, 50))
```

Используется `TestCase` или `FunctionTestCase` (для легаси). Unittest распознает как фейлы только собственные ассерты, предоставленные классом `TestCase`. В наборе есть сравнение успешных и неуспещных случаев, приблизительное сравнение, а так-же специальные методы для сравнения контейнеров (к примеру списков). [Полный список тут](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertEqual). Все остальные ассерты идентифицируются как ошибки.

Для каждого теста мы можем задать как собственные сетапы/тирдауны так и для всех тестов сразу. Порядок запуска тестов определяется сортировкой по имени. Тирдаун и тирап запускаются вне зависимости от результатов теста.

```python
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
```

С помощью `TestSuite` класса можно [группировать тесты](https://docs.python.org/3/library/unittest.html#unittest.TestSuite) для запуска (unittest делает это и самостоятельно, обнаруживая тесты по именам)

```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_widget_size'))
    suite.addTest(WidgetTestCase('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
```

## [Re-using old test code](https://docs.python.org/3/library/unittest.html#re-using-old-test-code)

## [Skipping tests and expected failures](https://docs.python.org/3/library/unittest.html#skipping-tests-and-expected-failures)

Можно скипать тесты как безусловно так и при условии. Классы тоже могут быть заскипаны.

```python
class MyTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(mylib.__version__ < (1, 3),
                     "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass

    def test_maybe_skipped(self):
        if not external_resource_available():
            self.skipTest("external resource not available")
        # test code that depends on the external resource
        pass
```

## [Сабтесты](https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests)

Используется, к примеру, когда разница между тестами небольшая. Например когда тестируется определенный ренж значений для объекта тестирования. Это позволяет увидеть все фейлы (иначе тест фейлится на первом кейсе. Это полезно, когда надо тестировать одну и туже логику с различными данными - когда мы ожидаем одинакового результата, но часть тестов падает.

```python
import unittest


class SubTest(unittest.TestCase):

    def test_with_subtest(self):
        for pat in ['a', 'B', 'c', 'd']:
            with self.subTest(pattern=pat):
                self.assertRegex('abc', pat)
```

## API unittest

### [Test cases](https://docs.python.org/3/library/unittest.html#test-cases)

Методы в `TestCase`

- `setUp()` реализует предоставление разделяемого ресурса
- `tearDown()` освобождает разделяемый ресурс
- `setUpClass()` устанавливает разделяемые ресурсы для класса
- `tearDownClass()` освобождает ресурсы для класса
- `setUpModule()`
- `tearDownModule()`
- `run(result=None)`
- `skipTest(reason)`
- `subTest(msg=None, **params)`
- `debug()` тест запускается без агрегации результата

Подробнее смотри [Class and module fixtures](https://docs.python.org/3/library/unittest.html#class-and-module-fixtures)

Обычно сетапы и тирдауны выносятся в отельный класс, наследуемый от `TestCase`, от которого уже могут наследоваться конкретные тесты. Пример:

```python
class MyUnitTests(unittest.TestCase):
    """Unit tests basic
    """

    def setTestingEngine(self, engine):
        """Set temporal base
        """
        [...]

    def setTemporalBase(self):
        """Set temporal data to base for tests
        """
        [...]

    def setUp(self):
        """start test server
        """
        self.setTestingEngine(engine)
        self.setTemporalBase()
        self.proc = Process(target=uvicorn.run,
                            args=(app,),
                            kwargs={
                                'host': ALLOWED_HOSTS,
                                'port': PORT,
                                'debug': DEBUG,
                                'log_level': 'info'},
                            daemon=True)
        self.proc.start()

        with TestClient(app) as self.client:
            [...]

    def tearDown(self):
        """Stop test server
        """
        self.proc.kill()
```

Если в процессе очистки ресурсов упадет ошибка, не все ресурсы могут быть освобождены. Чтобы избежать этой проблемы можно добавить `addCleanup()`, которая будет вызываться после `tearDown()`. Если `setUp()` завершается ошибкой, что означает, что `tearDown()` не вызывается, то любые добавленные функции очистки все равно будут вызываться.

`doClenups()` вызывается безоговорочно после `tearDown()` или после `setUp()`, если `setUp()` вызывает исключение. Он отвечает за вызов всех функций очистки, добавленных функцией `addCleanup()`. Если вам нужно, чтобы функции очистки вызывались до `tearDown()`, вы можете сами вызвать `doCleanups()`. `doCleanups()` извлекает методы из стека функций очистки по одному, поэтому ее можно вызвать в любое время.

Есть функции, доступные на урвоне класса и модуля. Смотри [подробности тут](https://docs.python.org/3/library/unittest.html#unittest.TestCase.addCleanup)

### Тестирование неудачных случаев

```python
with self.assertRaises(SomeException):
    do_something()

with self.assertRaises(SomeException) as cm:
    do_something()

the_exception = cm.exception
self.assertEqual(the_exception.error_code, 3)
```

[Документация из юниттеста по райзес](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises)

### [Тестирование асинхронного кода](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase)

### [Группировка тестов](https://docs.python.org/3/library/unittest.html#grouping-tests)

- `addTest(test)`
- `addTests(test)`
- `run(result)`
- `run()`
- `debug()`
- `__iter__()`

используется для загрузки тестов из пакетов и модулей.

### [Тестлоадеры и запуск тестов](https://docs.python.org/3/library/unittest.html#loading-and-running-tests)

### [load test protocol](https://docs.python.org/3/library/unittest.html#load-tests-protocol)

## [Signal Handling](https://docs.python.org/3/library/unittest.html#signal-handling)

-----

- [[pytest]]
- [[doctest]]
- [[тестирование]]
- [[2021-04-02-daily-note]]
- [[mock]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
[pytest]: pytest "Pytest"
[doctest]: doctest "Doctest"
[2021-04-02-daily-note]: ../posts/2021-04-02-daily-note "Про работу behave и unittest и немного про datetime"
[mock]: mock "Mock-тесты"
[//end]: # "Autogenerated link references"