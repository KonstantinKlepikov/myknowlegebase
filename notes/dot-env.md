# dot-env

Тулза #python для управления переменными окружения. [Ссылка на доку](https://saurabh-kumar.com/python-dotenv/)

```python
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
```

[[honcho]]
[[heroku-variables-config]]
