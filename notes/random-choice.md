---
description: Как выбирать случайные объекты в python
tags: numpy python
title: Random choice
---
## Weighted random choice

[A weighted version of random.choice](https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice)

[Как реализовать](https://stackoverflow.com/a/26196078/15966204) на [[numpy]]

Специальный метод `numpy.random.choice`, например с нечисловыми объектами

```python
aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])
array(['pooh', 'pooh', 'pooh', 'Christopher', 'piglet'], # random
      dtype='<U11')
```

Мы задаем array-like объект, число чейзов на выходе и вероятности выбора из последовательности. На выходе получаем numpy array. Способ может быть проблематичным, когда объекты не хешируются или имеют разные типы.

Другой способо - [использовать](https://docs.python.org/dev/library/random.html#random.choices) `random.choices`

```python
random.choices(population, weights=None, *, cum_weights=None, k=1)
```

Вот тут с примерами: [[2021-11-30-daily-note]]

[[mathematic-in-python]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[numpy]: numpy "Numpy"
[2021-11-30-daily-note]: ../posts/2021-11-30-daily-note "Diff массивов, случайный выбор, конвертация в булев массив и произвольные заполнители в numpy"
[mathematic-in-python]: mathematic-in-python "Mathematic in python"
[//end]: # "Autogenerated link references"