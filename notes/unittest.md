# unittest

## Тестирование неудачных случаев

```python
with self.assertRaises(SomeException):
    do_something()

with self.assertRaises(SomeException) as cm:
    do_something()

the_exception = cm.exception
self.assertEqual(the_exception.error_code, 3)
```

[Документация из юниттеста по райзес](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises)

Аналог в [[pytest]]

[Список всех ассертов](https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug)

[[тестирование]]
[[daily-note-2021-04-02]]
