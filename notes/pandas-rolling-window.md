---
description: Pandas rolling window and ewm
title: Pandas rolling window - скользящие средние в pandas
tags: market-stocks python
---
Простые [[скользящие-средние]] в pandas реализованы в многочисленном семействе функций [window](https://pandas.pydata.org/docs/reference/window.html) функций. Кроме того, есть:

- алгоритм скользящего окна
- экспоненциальные взвешенные скользящее средние

Вычисление скользящих обеспечено функциями [pandas.Series.rolling](https://pandas.pydata.org/docs/reference/api/pandas.Series.rolling.html#pandas.Series.rolling), [pandas.DataFrame.rolling](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html#pandas.DataFrame.rolling), которые принимают объект [window](https://pandas.pydata.org/docs/reference/window.html) для определения типа трансформации над данными. К примеру вот о[бъект скользящего среднего](https://pandas.pydata.org/docs/reference/api/pandas.core.window.rolling.Rolling.mean.html#pandas.core.window.rolling.Rolling.mean) для расчета скользящего окна.

## [rolling window](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html)

```python
DataFrame.rolling(
     window,
     min_periods=None,
     center=False,
     win_type=None,
     on=None,
     axis=0,
     closed=None,
     method='single'
          )
```

**window int, offset, or BaseIndexer subclass** - размер скользящего окна. Это количество наблюдений из фрейма, используемых для расчета статистики. Каждое окно будет фиксированного размера.

Если это смещение, то это будет период времени каждого окна. Каждое окно будет иметь переменный размер на основе наблюдений, включенных в период времени.

Все это работает только для индексов типа datetime. Если передан подкласс BaseIndexer, границы окна вычисляются на основе определенного метода get_window_bounds. Дополнительные аргументы скользящего окна, а именно min_periods, center и closed будут переданы в get_window_bounds.

**min_periodsi nt, default None** - минимальное количество наблюдений в окне, необходимое для получения значения (в противном случае результат - NA). Для окна, заданного смещением, min_periods будет по умолчанию равным 1. В противном случае min_periods будет по умолчанию равным размеру окна.

**center bool, default False** - устанавливает метки в центр окна

**win_type str, default None** - устанавливает тип окна. Если `none` - все значения будут иметь одинаковый вес. Смотри ниже о типах окон.

**closed str, default None** - определяет где закрыть интерфвал `right`, `left`, `both` или `neither`. Дефолтный `right`

**method str {‘single’, ‘table’}, default ‘single’** - выполните операцию для отдельного столбца или строки `single` или для всего объекта `table`. Этот аргумент реализуется только при указании `engine = 'numba'` в вызове метода.

По умолчанию результат устанавливается у правого края окна (см. `closed`). [Большая статья про смещения в pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).

Если `win_type = None`, все значения имеют равный вес; в противном случае `win_type` может принимать любую оконную функцию из [scipy.signal window function](https://docs.scipy.org/doc/scipy/reference/signal.windows.html#module-scipy.signal.windows). Некоторые типы окон Scipy требуют передачи дополнительных параметров в функцию агрегирования. Дополнительные параметры должны соответствовать ключевым словам, указанным в сигнатуре метода типа окна [[scipy]].

Примеры

```python
>>> df = pd.DataFrame({'B': [0, 1, 2, np.nan, 4]})
>>> df
     B
0  0.0
1  1.0
2  2.0
3  NaN
4  4.0
```

Скользящая сумма с длиной окна 2, с использованием типа окна «треугольник»

```python
>>> df.rolling(2, win_type='triang').sum()
     B
0  NaN
1  0.5
2  1.5
3  NaN
4  NaN
```

Скользящая сумма с длиной окна 2, с использованием типа окна «гауссово» (обратите внимание, как нам нужно указать std)

```python
>>> df.rolling(2, win_type='gaussian').sum(std=3)
          B
0       NaN
1  0.986207
2  2.958621
3       NaN
4       NaN
```

Скользящая сумма с длиной окна 2, min_periods по умолчанию равняется длине окна.

```python
>>> df.rolling(2).sum()
     B
0  NaN
1  1.0
2  3.0
3  NaN
4  NaN
```

Тоже, с заданным периодом

```python
>>> df.rolling(2, min_periods=1).sum()
     B
0  0.0
1  1.0
2  3.0
3  2.0
4  4.0
```

Тоже самое, но смотрящее вперед окно

```python
indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=2)
df.rolling(window=indexer, min_periods=1).sum()
     B
0  1.0
1  3.0
2  2.0
3  4.0
4  4.0
```

Неравномерный (с нерегулярной частотй) индексированный по времени датафрейм

```python
>>> df = pd.DataFrame({'B': [0, 1, 2, np.nan, 4]},
                  index = [pd.Timestamp('20130101 09:00:00'),
                           pd.Timestamp('20130101 09:00:02'),
                           pd.Timestamp('20130101 09:00:03'),
                           pd.Timestamp('20130101 09:00:05'),
                           pd.Timestamp('20130101 09:00:06')])

>>> df
                       B
2013-01-01 09:00:00  0.0
2013-01-01 09:00:02  1.0
2013-01-01 09:00:03  2.0
2013-01-01 09:00:05  NaN
2013-01-01 09:00:06  4.0
```

В отличие от целочисленного скользящего окна, тут будет применяться окно переменной длины, соответствующее периоду времени. По умолчанию для min_periods установлено значение 1.

```python
>>> df.rolling('2s').sum()
                       B
2013-01-01 09:00:00  0.0
2013-01-01 09:00:02  1.0
2013-01-01 09:00:03  3.0
2013-01-01 09:00:05  NaN
2013-01-01 09:00:06  4.0
```

## [pandas.DataFrame.expanding](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.expanding.html)

Обеспечивает заполняющую трансформацию данных

```python
DataFrame.expanding(min_periods=1, center=None, axis=0, method='single')
```

**min_periods int, default 1** - минимальное кол-во наблюдений в окне, необходимых для получения значений (иначе NA)

**center bool, default False** - по умолчанию результат устанавливается у правого края окна. Это можно изменить в центр окна.

Все остальное аналогично скользящим окнам

```python
>>> df = pd.DataFrame({"B": [0, 1, 2, np.nan, 4]})
>>> df
     B
0  0.0
1  1.0
2  2.0
3  NaN
4  4.0

>>> df.expanding(2).sum()
     B
0  NaN
1  1.0
2  3.0
3  3.0
4  7.0
```

## [pandas.DataFrame.ewm](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)

Подробнее смотир в документации (формулы и etc.)

Пример кода:

```python
>>> df = pd.DataFrame({'B': [0, 1, 2, np.nan, 4]})
>>> df
     B
0  0.0
1  1.0
2  2.0
3  NaN
4  4.0

>>> df.ewm(com=0.5).mean()
          B
0  0.000000
1  0.750000
2  1.615385
3  1.615385
4  3.670213
```

Указание времени с "периодом полураспада" (специфичный к алгоритму термин) timedelta при вычислении среднего значения.

```python
>>> times = ['2020-01-01', '2020-01-03', '2020-01-10', '2020-01-15', '2020-01-17']
>>> df.ewm(halflife='4 days', times=pd.DatetimeIndex(times)).mean()
          B
0  0.000000
1  0.585786
2  1.523889
3  1.523889
4  3.233686
```

[//begin]: # "Autogenerated link references for markdown compatibility"
[скользящие-средние]: %D1%81%D0%BA%D0%BE%D0%BB%D1%8C%D0%B7%D1%8F%D1%89%D0%B8%D0%B5-%D1%81%D1%80%D0%B5%D0%B4%D0%BD%D0%B8%D0%B5 "Скользящие средние (moving average)"
[scipy]: scipy "Scipy"
[//end]: # "Autogenerated link references"