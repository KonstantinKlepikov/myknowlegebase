---
type: feature
keywords: pytest, python
---
# pytest

Библиотечка для [[модульные-тесты]]

## Тестирование неудачных случаев

```python
import pytest
with pytest.raises(ZeroDivisionError):
    1/0
```

[Документация raises](https://docs.pytest.org/en/stable/reference.html#pytest.raises)
[[unittest]] - аналог

[Документация пайтеста](https://docs.pytest.org/en/stable/contents.html#toc)
