---
title: Про переменные инстанса класса и n-мерные массивы в numpy
description: Как получит ьвсе переменные инстанса класса и про n-мерные массивы в numpy
category: post
---
## Как получить переменные, созданные при инилицализации класса?

[How to get python class instance variables inside __init__](https://stackoverflow.com/questions/55629400/how-to-get-python-class-instance-variables-inside-init)

```python
class Identity:
    table = "tb_identity"
    def __init__(self, id="", app_name="", app_code="", state="", criticality=""):
        self.id = id
        self.app_name = 'trigram_name'
        self.app_code = 'trigram_irt'
        self.state = state
        self.criticality = criticality
        print(self.__dict__.keys())
i = Identity()

>>> dict_keys(['id', 'app_name', 'app_code', 'state', 'criticality'])
```

Соответственно, если нужен словарь: [Python dictionary from an object's fields](https://stackoverflow.com/a/62680/15966204)

## n-мерный массив в [[numpy]]

[Собстивенно все очень просто](https://stackoverflow.com/a/22982371/15966204)

[Про n-мерные массивы статья](https://numpy.org/doc/stable/reference/arrays.ndarray.html)

## 137 code в [[github-action]]

[Не хватило памяти](https://github.community/t/docker-container-running-tests-keep-on-exiting-on-github-acitons-with-exit-code-137/176417) вирутальной машине. Посмотреть [[github-action-resources]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[numpy]: ../notes/numpy "Numpy"
[github-action]: ../notes/github-action "Githunb action"
[github-action-resources]: ../notes/github-action-resources "Github actions resources"
[//end]: # "Autogenerated link references"