---
description: Встроенные функции для работы с последовательностями в python
tags: python-standart-library
---
# Itertools

Модуль включает функции для обработки последовательностей. Задача - повысить эффективность использования памяти и скорость выполнения операций.

Идея заключается в том, чтобы использовать итераторы, которые возвращают данные только по вызову, что не требует расчета всей последовательности целиком переда началом операций над нею.

## [chain()](https://docs.python.org/3/library/itertools.html#itertools.chain)

Данная функция получает несколько последовательность и создает итератор, который проходит последоватлеьно по всем компонентам цепи. Такой подход не требует предварительного конструирования объединенного списка (или другой последовательности). Кроме того `chain()` не интересует какая именно последоваетльность передана функции - важно только, чтобы она поддерживала протокл итерации.

```python
import itertools

for i in itertools.chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
>>> 1 2 3 a b c
```

Когда мы не знаем объединяемые объекты заранее или их вычисление нужно отложить, можно использовать `chain.from_iterable()` для получения итератора из итераторов. Это [дополнительный конструктор](https://docs.python.org/3/library/itertools.html#itertools.chain.from_iterable), который принимает в качестве аргумента единственный итерируемый объект.

```python
def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']

for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
```

## [zip_longest()](https://docs.python.org/3/library/itertools.html#itertools.zip_longest)

`zip()` - создает итератор, который возвращает кортежи, состящие из элементов переданных `zip()` итераторов. Функция прекратит работу, когда одна из последовательностей завершится. Чтобы реализовать [другое поведение](https://docs.python.org/3/library/itertools.html#itertools.zip_longest), в itertools есть функция `zip_longest()`, которая заполнит `None` недостающие значения или проствит `fillvalue`

```python
r1 = range(3)
r2 = range(2)
print(list(zip_longest(r1, r2)))
>>> [(0, 0), (1, 1), (2, None)]
```

## [islice()](https://docs.python.org/3/library/itertools.html#itertools.islice)

Возвращает итератор, выдающий входные элементы в соответствии с заданным индексом. Протокол полностью идентичен start, step, stop за исключением того, что не поддерживаются отрицательные значения.

## [tee()](https://docs.python.org/3/library/itertools.html#itertools.tee)

Создает из одного итератора несколько идентичных, что можно использовать дял передачи данных одного источника нескольким потребителям. Деволтное значение n=2. После разделения оригинальный итератор использовать не рекомендуется, так как созданные им итераторы разделяют данные с исходным.

Функция не является потоко-безопасной.

```python
from itertools import islice, tee

r = islice(count(), 5)
i1, i2 = tee(r)
print(list(i1))
>>> [0, 1, 2, 3, 4]
print('i2:', list(i2))
>>> [0, 1, 2, 3, 4]
```

## [starmap()](https://docs.python.org/3/library/itertools.html#itertools.starmap)

Встроенная функция `map()` применяет выбранную функцию к последовательности. исбользую элементы последовательности как атрибуты. Так-же как и в `zip()` этот процесс прекращается при исчерпании одной из переданных последоватльностей. `starmap()` использует всего два аргумента - первый это функция для map, второй - э то последовательность кортеже, которые будут распаковываться в функцию при итерации.

```python
import itertools

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

for i in itertools.starmap(lambda x, y: (x, y, x * y), values):
    print('{} * {} = {}'.format(*i))
>>> 0 * 5 = 0
>>> 1 * 6 = 6
>>> 2 * 7 = 14
>>> 3 * 8 = 24
>>> 4 * 9 = 36
```

## [count()](https://docs.python.org/3/library/itertools.html#itertools.count)

Бесконечный счетчик. Считаться могут быть любые числа, для которых определна операция сложения. Можно указать начальное значение (дефолтное 0), считать можно в т.ч. и в обратную сторону.

```python
import itertools

for i in zip(itertools.count(0.1, 1.0), ['a', 'b', 'c']):
    print(i)
>>> (0.1, 'a')
>>> (1.1, 'b')
>>> (2.1, 'c')
```

## [cycle()](https://docs.python.org/3/library/itertools.html#itertools.cycle)

Повторяет содержимое переданного итератора бесконечное количество раз

```python
from itertools import cycle
for i in zip(range(7), cycle(['a', 'b', 'c'])):
    print(i)
>>> (0, 'a')
>>> (1, 'b')
>>> (2, 'c')
>>> (3, 'a')
>>> (4, 'b')
>>> (5, 'c')
>>> (6, 'a')
```

## [repeat()](https://docs.python.org/3/library/itertools.html#itertools.repeat)

Всегда возвращает одно и тоже значение. Число повторов можно ограничить через аргумент `times`

```python
from itertools import count, repeat

for i, s in zip(count(), repeat('repeat', 5)):
    print(i, s)
>>> 0 repeat
>>> 1 repeat
>>> 2 repeat
>>> 3 repeat
>>> 4 repeat

for i in map(lambda x, y: (x, y, x * y), repeat(2), range(5)):
    print('{:d} * {:d} = {:d}'.format(*i))
>>> 2 * 0 = 0
>>> 2 * 1 = 2
>>> 2 * 2 = 4
>>> 2 * 3 = 6
>>> 2 * 4 = 8
```

## [dropehile()](https://docs.python.org/3/library/itertools.html#itertools.dropwhile)

Возвращает значение переданного итератора с первой позиции, которая делает условие ложным

```python
from itertools import dropwhile

def to_drop(x):
    print('to_drop:', x)
    return x < 1

for i in dropwhile(should_drop, [0, 0, 3, 2, -2]):
    print('to_Yield:', i)
>>> to_drop: 0
>>> to_drop: 0
>>> to_drop 3
>>> to_Yield: 2
>>> to_Yield: -2
```

Обрати внимание, что проверка будет осуществляться ровно до выполнения условия, а дальше итератор возвращает значения не проверяя.

## [takewhile()](https://docs.python.org/3/library/itertools.html#itertools.takewhile)

Антипод `dropwhile()` - возвращает значения до тех пор, пока проверочное условие `True`. Данная функция работает немного экономнее - ей не нужно проходить последовательность предварительно, поэтому проверка условия и выдача результирующего значения происходит одновременно

## [filterfalse()](https://docs.python.org/3/library/itertools.html#itertools.filterfalse)

Встроенная функция `filter()` создает итератор, включающий только те элементы, для которых тестирующая функция возвращает `True`. `filterfalse()` проверяет условие на `False`

## [compress()](https://docs.python.org/3/library/itertools.html#itertools.compress)

Аналогичен `filter()`, с той лишь разницей, что фильтрация производится не с использованием придоставоленной функции, а основываясь на последовательности

```python
from itertools import cycle, compress

third = cycle([False, False, True])
data = range(1, 10)

for i in compress(data, third):
    print(i, end=' ')
>>> 3 6 9
```

## [groopby()](https://docs.python.org/3/library/itertools.html#itertools.groupby)

Производит группировку значений предоставленной последовательности в соответствии с общим признаком. Чтобы группировка работала, исходная последовательность должна быть отсортирована.

Возвращаемый итератор разделяет данные с самой функцией. Есть нюансы реализации - см.документацию.

## [accumulate()](https://docs.python.org/3/library/itertools.html#itertools.accumulate)

Обрабатывает переданную функции последовательност с накоплением. Грубо говоря, используется первый и последующий элемент последовательности (они передаются предоставленнйо функции), а наследующем шаге в качестве первого элемента используется результат вычислений.

```python
from itertools import accumulate

def f(a, b):
    return b + a + b

print(list(accumulate('abcde', f)))
>>> ['a', 'bab', 'cbabc', 'dcbabcd', 'edcbabcde']
```

Функцию можно не передавать - `accumulate()` просуммирует последовательност с накоплением. Ное если передается функция, то она должна принимать строго два аргумента. Если переда аргумент `initial`, то аккумулирование начнется с этого значения и выходна последовательность будет на один элемент больше входной.

В качестве функций можно передавать методы из модуля `operator`, к примеру `mul()`, `sum()`. `min()` и т.д.

## [product()](https://docs.python.org/3/library/itertools.html#itertools.product)

Возвращает декартово произведение элементов входящих последовательностей. Значения возвращаемой последовательности - кортежи с эелементами исходноых в том порядке ,в котором они передавались. `product(A, B)` верн6ет тоже самое что и `((x,y) for x in A for y in B)`. Функция затратная по вычислениям и работает только с последовательностями конечной длины. Атрибут `repeat` повзоляет задать число повторений (полезно, к примеру, для получения декартового произведения последовательности на себя)

## [permutations()](https://docs.python.org/3/library/itertools.html#itertools.permutations)

Возвращает все возможные комбинации из элементов входной последовательности. Длину выходных элементов можно задать

## [combinations()](https://docs.python.org/3/library/itertools.html#itertools.combinations)

Эта функция возвращает только уникальные возможные сочетания. Атрибут `r` задающий длину элементов выходной последовательности, в данном случае обязателен

## [combinations_with_replacement()](https://docs.python.org/3/library/itertools.html#itertools.combinations_with_replacement)

Допускает сочетание одинаковых элементов - при этом такое сочетание в итоговй последовательности будет уникальным.

## [pairwise()](https://docs.python.org/3/library/itertools.html#itertools.pairwise)

Возвращает последовательность, состоящую из кортежей, сождержащих пары пересекающихся значений переданной последовательности.

```python
from itertools import pairwise

d = pairwize('ABCD')
for i in d:
    print(i[0], [i[1]])
>>> AB
>>> BC
>>> CD
```

Эта функция доступна начиная с 3.10

[Документация по itertools](https://docs.python.org/3/library/itertools.html)

Смотри так-же [[more-itertools]]

[[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[more-itertools]: more-itertools "More-itertools"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python - список заметок"
[//end]: # "Autogenerated link references"