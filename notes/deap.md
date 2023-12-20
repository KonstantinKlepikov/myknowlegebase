---
description: Использование фреймворка DEAP для эволюционной оптимизации
tags: machine-learning genetic pip python evol
title: Deap - генетические алгоритмы на python
---
- [deap на гитхаб](https://github.com/DEAP/deap)
- [документация](https://deap.readthedocs.io/en/master/)
- [[deap-docs]]

## Основные термины

**Ген** - вектор значений индивидуума, обучаемый алгоритмом

**Популяция** - коллекция генов

**Функция приспособленности** - или целевая функция. Функция, которую мы оптимизируем. Индивидуумы, для которых ф-ия дает наилучшую оценку будут отобраны генетическим алгоритмом.

## Класс creator

Метафабрика. позволяющая расширять существующие классы. Используется обычно для создания классов `Fitness` и `Individual`

```python
from deap import creator, base, tools, algorithms

class Employee:
    pass

creator.create("Developer", Employee, position="Developer", programmingLanguages=set)

help(creator.Developer)
```

```shell
    Help on class Developer in module deap.creator:

    class Developer(__main__.Employee)
     |  Developer(*args, **kargs)
     |
     |  Method resolution order:
     |      Developer
     |      __main__.Employee
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__ = initType(self, *args, **kargs)
     |      Replace the __init__ function of the new type, in order to
     |      add attributes that were defined with **kargs to the instance.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  position = 'Developer'
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from __main__.Employee:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
```

## Fitness

В этом классе инкапсулированы значения приспособленности. Приспособленность в deap можно определять по нескольким компонентам (целями). у каждой из которых есть вес. Комбинация весов определяет поведение или стратегию приспособления в конкретной задаче

base.Fitness - абстрактный класс. содержащий кортеж `weights`. Чтобы определить стратегию, кортежу наджо присвоить значения.

```python
creator.create('FitnessMax', base.Fitness, weights=(1.0,))

help(creator.FitnessMax)
```

```shell
    Help on class FitnessMax in module deap.creator:

    class FitnessMax(deap.base.Fitness)
     |  FitnessMax(*args, **kargs)
     |
     |  The fitness is a measure of quality of a solution. If *values* are
     |  provided as a tuple, the fitness is initialized using those values,
     |  otherwise it is empty (or invalid).
     |
     |  :param values: The initial values of the fitness as a tuple, optional.
     |
     |  Fitnesses may be compared using the ``>``, ``<``, ``>=``, ``<=``, ``==``,
     |  ``!=``. The comparison of those operators is made lexicographically.
     |  Maximization and minimization are taken care off by a multiplication
     |  between the :attr:`weights` and the fitness :attr:`values`. The comparison
     |  can be made between fitnesses of different size, if the fitnesses are
     |  equal until the extra elements, the longer fitness will be superior to the
     |  shorter.
     |
     |  Different types of fitnesses are created in the :ref:`creating-types`
     |  tutorial.
     |
     |  .. note::
     |     When comparing fitness values that are **minimized**, ``a > b`` will
     |     return :data:`True` if *a* is **smaller** than *b*.
     |
     |  Method resolution order:
     |      FitnessMax
     |      deap.base.Fitness
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__ = initType(self, *args, **kargs)
     |      Replace the __init__ function of the new type, in order to
     |      add attributes that were defined with **kargs to the instance.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  weights = (1.0,)
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from deap.base.Fitness:
     |
     |  __deepcopy__(self, memo)
     |      Replace the basic deepcopy function with a faster one.
     |
     |      It assumes that the elements in the :attr:`values` tuple are
     |      immutable and the fitness does not contain any other object
     |      than :attr:`values` and :attr:`weights`.
     |
     |  __eq__(self, other)
     |      Return self==value.
     |
     |  __ge__(self, other)
     |      Return self>=value.
     |
     |  __gt__(self, other)
     |      Return self>value.
     |
     |  __hash__(self)
     |      Return hash(self).
     |
     |  __le__(self, other)
     |      Return self<=value.
     |
     |  __lt__(self, other)
     |      Return self<value.
     |
     |  __ne__(self, other)
     |      Return self!=value.
     |
     |  __repr__(self)
     |      Return the Python code to build a copy of the object.
     |
     |  __str__(self)
     |      Return the values of the Fitness object.
     |
     |  delValues(self)
     |
     |  dominates(self, other, obj=slice(None, None, None))
     |      Return true if each objective of *self* is not strictly worse than
     |      the corresponding objective of *other* and at least one objective is
     |      strictly better.
     |
     |      :param obj: Slice indicating on which objectives the domination is
     |                  tested. The default value is `slice(None)`, representing
     |                  every objectives.
     |
     |  getValues(self)
     |
     |  setValues(self, values)
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from deap.base.Fitness:
     |
     |  valid
     |      Assess if a fitness is valid or not.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from deap.base.Fitness:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  values
     |      Fitness values. Use directly ``individual.fitness.values = values`` in order to set the fitness and ``del individual.fitness.values`` in order to clear (invalidate) the fitness. The (unweighted) fitness can be directly accessed via ``individual.fitness.values``.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from deap.base.Fitness:
     |
     |  wvalues = ()
```

В данном случае стратегия `FitnessMax` - максимизировать приспособленность индивидумов с единственной целью. Минимизация будет выглядеть так:

```python
creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
```

Множество целей. Первые две компоненты максимизируются, третья минимизируется. Важность компонент следует слева направо

```python
creator.create('FitnessCompound', base.Fitness, weights=(1.0, 0.2, -0.5))
```

**Кортеж values** хранит сами значения приспособленности. Эти значения дает отдельно определяемая функция, которую обычно называют `evaluate()`. Кортеж содержит по одному значению для каждой функуции (цели).

**Третий кортеж wvalues** содержит взвешенные значени, полученные перемножением `values` и `weights`. Это используется для сравнения индивидуумов.

wvalues можно сравнивать лексикографически с помощью операторов ``>``, ``<``, ``>=``, ``<=``, ``==``, ``!=``

## Individual

С помощью этого класса определяются индивидуумы, образующие популяцию. В данном случае все гены индивидумов будут иметь тип лист, а класс каждого индивидума будет содержать экземляр `FitnessMax`

```python
creator.create('Individual', list, fitness=creator.FitnessMax)

help(creator.Individual)
```

```text
    Help on class Individual in module deap.creator:

    class Individual(builtins.list)
     |  Individual(*args, **kargs)
     |
     |  Built-in mutable sequence.
     |
     |  If no argument is given, the constructor creates a new empty list.
     |  The argument must be an iterable if specified.
     |
     |  Method resolution order:
     |      Individual
     |      builtins.list
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__ = initType(self, *args, **kargs)
     |      Replace the __init__ function of the new type, in order to
     |      add attributes that were defined with **kargs to the instance.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.list:
     |
     |  __add__(self, value, /)
     |      Return self+value.
     |
     |  __contains__(self, key, /)
     |      Return key in self.
     |
     |  __delitem__(self, key, /)
     |      Delete self[key].
     |
     |  __eq__(self, value, /)
     |      Return self==value.
     |
     |  __ge__(self, value, /)
     |      Return self>=value.
     |
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |
     |  __gt__(self, value, /)
     |      Return self>value.
     |
     |  __iadd__(self, value, /)
     |      Implement self+=value.
     |
     |  __imul__(self, value, /)
     |      Implement self*=value.
     |
     |  __iter__(self, /)
     |      Implement iter(self).
     |
     |  __le__(self, value, /)
     |      Return self<=value.
     |
     |  __len__(self, /)
     |      Return len(self).
     |
     |  __lt__(self, value, /)
     |      Return self<value.
     |
     |  __mul__(self, value, /)
     |      Return self*value.
     |
     |  __ne__(self, value, /)
     |      Return self!=value.
     |
     |  __repr__(self, /)
     |      Return repr(self).
     |
     |  __reversed__(self, /)
     |      Return a reverse iterator over the list.
     |
     |  __rmul__(self, value, /)
     |      Return value*self.
     |
     |  __setitem__(self, key, value, /)
     |      Set self[key] to value.
     |
     |  __sizeof__(self, /)
     |      Return the size of the list in memory, in bytes.
     |
     |  append(self, object, /)
     |      Append object to the end of the list.
     |
     |  clear(self, /)
     |      Remove all items from list.
     |
     |  copy(self, /)
     |      Return a shallow copy of the list.
     |
     |  count(self, value, /)
     |      Return number of occurrences of value.
     |
     |  extend(self, iterable, /)
     |      Extend list by appending elements from the iterable.
     |
     |  index(self, value, start=0, stop=9223372036854775807, /)
     |      Return first index of value.
     |
     |      Raises ValueError if the value is not present.
     |
     |  insert(self, index, object, /)
     |      Insert object before index.
     |
     |  pop(self, index=-1, /)
     |      Remove and return item at index (default last).
     |
     |      Raises IndexError if list is empty or index is out of range.
     |
     |  remove(self, value, /)
     |      Remove first occurrence of value.
     |
     |      Raises ValueError if the value is not present.
     |
     |  reverse(self, /)
     |      Reverse *IN PLACE*.
     |
     |  sort(self, /, *, key=None, reverse=False)
     |      Sort the list in ascending order and return None.
     |
     |      The sort is in-place (i.e. the list itself is modified) and stable (i.e. the
     |      order of two equal elements is maintained).
     |
     |      If a key function is given, apply it once to each list item and sort them,
     |      ascending or descending, according to their function values.
     |
     |      The reverse flag can be set to sort in descending order.
     |
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.list:
     |
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from builtins.list:
     |
     |  __hash__ = None
```

## Toolbox

Это контейнер для функций и операторов и позволяет создавать новые операторы путем назначения псевдонимов

Первым аргументом реигстрируем имя ф-ии. Вторым передаем ей выполняемую функцию. Остальные рагументы - необязательны (аргументы выполняемой ф-ии)

```python
def sum_of_two(a, b):
    return a + b

toolbox = base.Toolbox()
toolbox.register('increment_by_five', sum_of_two, b=5)
toolbox.increment_by_five(10)

>>>15
```

## Создание генетических операторов

модуль `tools` содержит полезные функции для осуществления операций отбора, включая скрещивание и мутации, а так-же утилиты для инициализации. Поэтому `Toolbox` используется в основном для этого

В данном случае:

- создан оператор `tools.select` использующий турнирный отбор с аргументом 3 (размер тиурнира)
- создан оператор `mate` как псевдоним ф-ии `cxTwoPoint()`, выполняющей двухточечное скрещивание
- создан оператор `mutate` c операцией инвертирования бита и вероятностью 0.02

Функции отбора хранятся в `selection.py`. Функции скрещивания в `crossower.py`. Функции мутации в `mutation.py`

```python
toolbox.register('select', tools.selTournament, tournize=3)
toolbox.register('mate', tools.cxESTwoPoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=0.02)
```

## Создание популяции

`init.py` содержит несколько ф-ий полезных для создания и иницализации популяции.

Функцияя `initRepeat()` принимает три аргумента:

- тип контейнера результирующих объектов
- ф-ия. генерирующая объекты, которые помещаются в контейнер
- сколько объектов генерировать

```python
import random
toolbox.register('zero_or_one', random.randint, 0, 1)
rnd = tools.initRepeat(list, toolbox.zero_or_one, 30)
rnd

>>> [0, 1, 0, 1, 1, ..., 1, 1]
```

## Вычисление приспособленности

значение приспособленности обычно возвращаются отдельно определенной ф-ией, которая регистрируется в `toolbox` как `evaluate` (соглашение)

```python
def some_calc(nums):
    return nums

toolbox.register('evaluate', some_calc)
```

## Statistics

Класс `tools.Statistics` позволяет собират ьстатистику. задавая ф-ию, применяемую к данным, для которых вычисляется статистика. Например для случая, когда популяция является данными, функция извлекающая приспособленность каждого индивидуума и зарегистрированные методы

```python
import numpy as np
stats = tools.Statistics(lambda ind: inf.fitness.values)
stats.register("max", np.max)
stats.register("avg", np.mean)
```

## Встроенные алгоритмы

В DEAP несколько встроенных эволюционных алгоритмов, реализующих пайплайн обучения. Пример примененеия:

```python
population, logbook = algorithms.eaSimple(
    population,
    toolbox,
    cxpb=CONST1,
    mutpb=CONST2,
    ngen=CONST3,
    stats=stats,
    verbose=True,
)
```

## logbook

логбук - собранная статистика, которую возвращает алгоритм. Ее можно извлечь методом `select()` (в данном случае как раз и используются зарегистрирвоанные нами методы сбора статы)

```python
max_, mean_ = logbook.select('max', 'avg`)
```

## Зал славы

Класс HallOfFame модуля tools возвращает отранжированный список лучших индивидумов, даже если в процессе эволюции или отбора они были утрачены.

## Еще информация

- как использовать несколько процессоров тут: [[deap]]
- документация тут [[deap-docs]]
- [sklearn-deap](https://github.com/rsteca/sklearn-deap) - имплементит эволюционный алгоритм вместо гридсерча
- [How to write loss function with extra parameters](https://github.com/DEAP/deap/issues/331)
- [[deap-checkpoints]] чекпоинты в обучении
- [[deap-history]] истоиря обучения для построения генеалогического дерева индивидуумов
- [[evolution-methods]]

[[evolution-for-neural-networks]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[deap-docs]: deap-docs "Deap документация"
[deap]: deap "Deap - генетические алгоритмы на python"
[deap-checkpoints]: deap-checkpoints "Deap чекпоинты"
[deap-history]: deap-history "Deap history"
[evolution-methods]: ..%2Flists%2Fevolution-methods "Evolution methods"
[evolution-for-neural-networks]: evolution-for-neural-networks "Evolution for neural networks"
[//end]: # "Autogenerated link references"