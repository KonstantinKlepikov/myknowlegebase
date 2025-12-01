---
description: Использование нескольких процессоров во фреймворке DEAP
tags: machine-learning genetic python evol
title: Multiproces for deap
---
```python
import multiprocessing

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

# Continue on with the evolutionary algorithm
```

Не забудь [закрыть процесс](https://stackoverflow.com/a/61963089/15966204)

```python
pool.close()
```

[Ссылка на статью документации](https://deap.readthedocs.io/en/master/tutorials/basic/part4.html)

[Пример](https://github.com/DEAP/deap/blob/master/examples/ga/onemax_mp.py)

- [[deap]]
- [[deap-docs]]
- [[evolution-methods]]


[deap]: deap "Deap - генетические алгоритмы на python"
[deap-docs]: deap-docs "Deap документация"
[evolution-methods]: ../lists/evolution-methods "Evolution methods"
