---
description: Описание python фреймворка DEAP для эволюционной оптимизации
tags: ml
---
# Deap документация

Смотри вводную в [[deap]]

## [Creating Types](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html)

### Fitness

[Fitness](https://deap.readthedocs.io/en/master/api/base.html#deap.base.Fitness) is an abstract class that needs a weights attribute in order to be functional.

Можно использовать ready-tobuild [creator](https://deap.readthedocs.io/en/master/api/creator.html#module-deap.creator) матефабрику

```python
create("Foo", list, bar=dict, spam=1)
```

что эквивалентно:

```python
class Foo(list):
    spam = 1

    def __init__(self):
        self.bar = dict()
```

Пример создания

```python
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
```

```python
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
```

Во втором примере минимизируется первая функция и максимизируется вторая. Порядок определен слева направо. Знак определяет минимизацию или максимизацию, а значение числа - важность.

### Individual

[Individual](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#individual) - необходимо создать специальный класс, который определяет индивида. Пример

```python
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

IND_SIZE=10

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=IND_SIZE)
```

Варианты с наследованием типов естественно не ограничены списком

```python
creator.create("Individual", array.array, typecode="d", fitness=creator.FitnessMax)
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)
```

В примерах выше инициализация выполняется с пмощью методов [Initialization](https://deap.readthedocs.io/en/master/api/tools.html#initialization):

- `initRepeat`
- `initIterate`
- `initCycle`
- `genFull`
- `genGrow`
- `genHalfAndHalf`

Пример

```python
>>> import random
>>> random.seed(42)
>>> initRepeat(list, random.random, 2) # doctest: +ELLIPSIS,
...                                    # doctest: +NORMALIZE_WHITESPACE
[0.6394..., 0.0250...]
```

[Permutation](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#permutation) - пример инициализацйии индивидума с перестановкой. пример простейщего случая (список) - в данном случае создается кастомная функция для заполения, которой и инициализируется индивидуум с помощью`tools.initIterate`

```python
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

IND_SIZE=10

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)
```

[Arithmetic Expression](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#permutation) - использование математических выражений для инициализации

```python
import operator

from deap import base
from deap import creator
from deap import gp
from deap import tools

pset = gp.PrimitiveSet("MAIN", arity=1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin,
               pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.expr)
```

[Evolution Strategy](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#evolution-strategy) - индивидуальные стратегии эволюции содержат два списка: один для конкретного индивидума, а другой - для его параметров мутации.

```python
import array
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode="d",
               fitness=creator.FitnessMin, strategy=None)
creator.create("Strategy", array.array, typecode="d")

def initES(icls, scls, size, imin, imax, smin, smax):
    ind = icls(random.uniform(imin, imax) for _ in range(size))
    ind.strategy = scls(random.uniform(smin, smax) for _ in range(size))
    return ind

IND_SIZE = 10
MIN_VALUE, MAX_VALUE = -5., 5.
MIN_STRAT, MAX_STRAT = -1., 1. 

toolbox = base.Toolbox()
toolbox.register("individual", initES, creator.Individual,
                 creator.Str
```

[Particle](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#particle) - имеет ряд дополнительных параметров, позволяющих задавать скорость и запоминать лучший результат

```python
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Particle", list, fitness=creator.FitnessMax, speed=None,
               smin=None, smax=None, best=None)

def initParticle(pcls, size, pmin, pmax, smin, smax):
    part = pcls(random.uniform(pmin, pmax) for _ in xrange(size))
    part.speed = [random.uniform(smin, smax) for _ in xrange(size)]
    part.smin = smin
    part.smax = smax
    return part

toolbox = base.Toolbox()
toolbox.register("particle", initParticle, creator.Particle, size=2,
                 pmin=-6, pmax=6, smin=-3, smax=3)
```

[A Funky One](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#a-funky-one) - можно создавать любые собственные конструкции классов

```python
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

INT_MIN, INT_MAX = 5, 10
FLT_MIN, FLT_MAX = -0.2, 0.8
N_CYCLES = 4

toolbox.register("attr_int", random.randint, INT_MIN, INT_MAX)
toolbox.register("attr_flt", random.uniform, FLT_MIN, FLT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_int, toolbox.attr_flt), n=N_CYCLES)
```

### Population

[Варианты создания популяций](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#population)

#### Bag

Индивидумы создаются в виде списка

```python
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.population(n=100)
```

#### Grid

Сеточная популяция - это особый случай структурированной популяции, в которой соседние индивидумы оказывают прямое влияние друг на друга. Индивидумы распределены в матрице, где каждая ячейка содержит одного индивидума.

#### Swarm

Частично использована оптимизация роя

##### Demes

Позволяет создать сабпопуляцию в популяции

**[Seeding a Population](https://deap.readthedocs.io/en/master/tutorials/basic/part1.html#seeding-a-population)** - тут описывается способ создания воспроизводимой популяции

```python
import json

from deap import base
from deap import creator

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

def initIndividual(icls, content):
    return icls(content)

def initPopulation(pcls, ind_init, filename):
    with open(filename, "r") as pop_file:
        contents = json.load(pop_file)
    return pcls(ind_init(c) for c in contents)

toolbox = base.Toolbox()

toolbox.register("individual_guess", initIndividual, creator.Individual)
toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess, "my_guess.json")

population = toolbox.population_guess()
```

## [Evolutionary Tools](https://deap.readthedocs.io/en/master/api/tools.html#module-deap.tools)

Включает готовые тулзы:

- Initialization
- Crossover
- Mutation
- Selection
- Migration
- Initialization
- Crossover
- Mutation
- Bloat control

## [Alghoritms](https://deap.readthedocs.io/en/master/api/algo.html#module-deap.algorithms)

Включает несколько готовых алгоритмов эволюционной оптимизации.

**Complete Algorithms**:

- eaSimple - simplest evolutionary algorithm
- eaMuPlusLambda. This is the (μ+λ) evolutionary algorithm
- eaMuCommaLambda. This is the (μ , λ) evolutionary algorithm
- eaGenerateUpdate. Ask-tell model proposed in Colette2010 (Collette, Y., N. Hansen, G. Pujol, D. Salazar Aponte and R. Le Riche (2010). On Object-Oriented Programming of Optimizers - Examples in Scilab. In P. Breitkopf and R. F. Coelho, eds.: Multidisciplinary Design Optimization in Computational Mechanics, Wiley, pp. 527-565;), where ask is called generate and tell is called update

**Variations**:

- varAnd. Part of an evolutionary algorithm applying only the variation part (crossover and mutation). The modified individuals have their fitness invalidated. The individuals are cloned so returned population is independent of the input population.
- varOr. Part of an evolutionary algorithm applying only the variation part (crossover, mutation or reproduction). The modified individuals have their fitness invalidated. The individuals are cloned so returned population is independent of the input population.

**Covariance Matrix Adaptation Evolution Strategy**:

- Strategy. A strategy that will keep track of the basic parameters of the CMA-ES algorithm
- StrategyOnePlusLambda. A CMA-ES strategy that uses the 1+λ paradigm
- StrategyMultiObjective. Multiobjective CMA-ES strategy based on the paper Voss2010 (). It is used similarly as the standard CMA-ES strategy with a generate-update scheme.

## [Computing Statistics](https://deap.readthedocs.io/en/master/tutorials/basic/part3.html#computing-statistics)

## [Logging Data](https://deap.readthedocs.io/en/master/tutorials/basic/part3.html#logging-data)

## [Using Multiple Processors](https://deap.readthedocs.io/en/master/tutorials/basic/part4.html#using-multiple-processors)

Еще по теме:

- [One Max Problem: Using Numpy](https://deap.readthedocs.io/en/master/examples/ga_onemax_numpy.html)
- [DEEP examples in notebooks](https://github.com/DEAP/notebooks)

[//begin]: # "Autogenerated link references for markdown compatibility"
[deap]: deap "Deap - генетические алгоритмы на python"
[//end]: # "Autogenerated link references"