---
description: Cбор и анализ потребления процессорного времени в python
tags: python-standart-library python
title: Profile
---
- cProfile рекомендуется большинству пользователей; это расширение C
- profile, чистый модуль Python, интерфейс которого имитирует cProfile, но который значительно увеличивает нагрузку на профилируемые программы

Вывод отчетов организован с помощью pstats. Для маленьких объектов кода лучше использовать [[timeit]]

Запускается через `run()`. В данном примере мы получим вывод функции и отчет

```python
import cProfile


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n - 1))
    seq.append(fib(n))
    return seq


cProfile.run('print(fib_seq(20)); print()')
```

```shell
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]

         57358 function calls (68 primitive calls) in 0.009 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.009    0.009 <string>:1(<module>)
 57291/21    0.009    0.000    0.009    0.000 profile_fibonacci_raw.py:11(fib)
     21/1    0.000    0.000    0.009    0.009 profile_fibonacci_raw.py:22(fib_seq)
        1    0.000    0.000    0.009    0.009 {built-in method builtins.exec}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
       21    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
       20    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
```

В данном отчете указано сколько всего было вызовов (и сколько примитивов, что указывает на долю рекурсии) и затраченное время. Подробно расписано на что потрачено процессорное время. ncalls  - количество вызовов. tottime общее затраченное время. percall время затраченное на вызов (tottime/ncalls). cumtime кумулятивное время, затраченное на функцию и последнее - отноешине кумулятивного времени к количеству примитивных вызовов (cumtime/primitive calls).

Другой вариант запуска прпофилировщика - `runctx()`? который позволяет передать простое выражение  с параметрами через контекст. [Смотри тут](https://docs.python.org/3/library/profile.html#profile.runctx)

pstats позволяет создавать пользовательский отчет, сохраняя исходные данные профилирования, полученные с `run()` или `runctx()`. Обработку данных выполняет `pstats.Stats`. [Смотри тут](https://docs.python.org/3/library/profile.html#the-stats-class)

С помощью [gprof2dot](https://github.com/jrfonseca/gprof2dot) результат работы профилировщика можно визуализировать.

Смотри еще:

- [документация](https://docs.python.org/3/library/profile.html)
- [[timeit]]
- [[time]]
- [[python-standart-library]]


[timeit]: timeit "Timeit"
[time]: time "Time"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
