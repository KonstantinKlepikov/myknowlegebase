---
description: Управление переменными окружения в python с помощью dot-env
tags: python-standart-library pip python
title: Dot-env
---
Тулза python для управления переменными окружения. [Ссылка на доку](https://saurabh-kumar.com/python-dotenv/)

```python
import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
```

Смотри еще:

- [[how-to-set-nonstring-env-variables]]
- [[honcho]]
- [[heroku-variables-config]]
- [[env-for-test]]
- [How to pass a list as an environment variable?](https://stackoverflow.com/questions/31352317/how-to-pass-a-list-as-an-environment-variable)
- [How to define lists in python dot env file?](https://stackoverflow.com/questions/65969601/how-to-define-lists-in-python-dot-env-file)


[how-to-set-nonstring-env-variables]: how-to-set-nonstring-env-variables "How set nonstring env variables"
[honcho]: honcho "Honcho"
[heroku-variables-config]: heroku-variables-config "Heroku variables config"
[env-for-test]: env-for-test "Env variables for tests"
