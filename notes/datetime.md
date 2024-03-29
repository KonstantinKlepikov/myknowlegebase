---
description: Datetime. Модуль стандартной библиотеки python для работы со значениями даты и времни
tags: python-standart-library python
title: Datetime
---
Библиотечка на python для синтаксического анализа значений даты и времени

Для представления значений времени используется класс `time`, доступ к данным времени можно получить по атрибутам. Экземпляр класса хранит только время и его разрещшающая способность ограничена микросекундами.

```python
>>> import datetime

>>> t = datetime.time(1, 2, 3)
>>> print(t)
01:02:03
>>> print(t.hour)
1
>>> print(t.minute)
2
>>> print(t.second)
3
>>> print(t.microsecond)
0
>>> print(t.tzinfo)
None
```

Даты можно извлекать через класс `date` используя похожий апи. Метод `today()` создает экземпляр текущей даты. Разрешающая способность - сутки.

```python
>>> import datetime

>>> today = datetime.date.today()
>>> tt = today.timetuple()
>>> print(tt.tm_year)
>>> print(tt.tm_mon)
>>> print(tt.tm_mday)
>>> print(tt.tm_hour)
>>> print(tt.tm_min)
>>> print(tt.tm_sec)
>>> print(tt.tm_wday)
>>> print(tt.tm_yday)
>>> print(tt.tm_isdst)
```

Кроме того, экземпляр даты можно получить из существующей даты с помощью метода `replace()`

`timedelta()` позволяет получить нужный промежуток времени, с которым можно осуществлять базовый арифметические операции и сравнение. У timedelta свой апи доступа к значениям. полную длительность в секундах можно получить из объекта timedelta с помощью ёещефд_ыусщтвы()ё

```python
>>> import datetime

>>> print(datetime.timedelta(microseconds=1))
>>> print(datetime.timedelta(milliseconds=1))
>>> print(datetime.timedelta(seconds=1))
>>> print(datetime.timedelta(minutes=1))
>>> print(datetime.timedelta(hours=1))
>>> print(datetime.timedelta(days=1))
>>> print(datetime.timedelta(weeks=1))
```

Класс datetime предоставляет методы `fromordinal()` и `fromtimestamp()`, позволяющие конвертировать представление даты и времени. `combine()` позволяет скомбинировать экземлпяр datetime из экземпляров date и time

```python
>>> import datetime

>>> t = datetime.time(1, 2, 3)
>>> print('t :', t)
t : 01:02:03

>>> d = datetime.date.today()
>>> print('d :', d)
d : 2021-12-05

>>> dt = datetime.datetime.combine(d, t)
>>> print('dt:', dt)
dt: 2021-12-05 01:02:03
```

Форматирование так-же доступно через функции `strftime()` и `strptime()`. Все доступные форматы [тут](https://docs.python.org/3/library/datetime.html?highlight=datetime#strftime-and-strptime-format-codes)

Частовые пояа представлены абстрактным классом `tzinfo` - необходимо определить сабкласс и предоставить ему реализации методов. В datetime представляена тривиальная реализация в виде сабкласса `timezone` с использованием фиксированного смещения относительно UTC

```python
>>> import datetime

>>> min6 = datetime.timezone(datetime.timedelta(hours=-6))
>>> plus6 = datetime.timezone(datetime.timedelta(hours=6))
>>> d = datetime.datetime.now(min6)
```

`astimezone()` обеспечивает преобразование одного часового пояса в другой.

```python
>>> z = d.astimezone(plus6)
```

## Как получимть текущее время

```python
>>> import datetime
>>> datetime.datetime.now()
datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)

>>> print(datetime.datetime.now())
2009-01-06 15:08:24.789150
```

или просто время

```python
>>> datetime.datetime.now().time()
datetime.time(15, 8, 24, 78915)

>>> print(datetime.datetime.now().time())
15:08:24.789150
```

Мне показался полезным этот вариант:

```python
>>> from time import gmtime, strftime
>>> strftime("%Y-%m-%d %H:%M:%S", gmtime())
'2009-01-05 22:14:39'
```

Или так

```python
>>> from datetime import datetime
>>> datetime.now().strftime('%Y-%m-%d %H:%M:%S')
```

[Ссылка](https://stackoverflow.com/a/415525/15966204)

Если надо представить разницу во времени в человекочитаемом виде, то можно [так](https://stackoverflow.com/a/3427051/15966204):

```python
>>> import datetime
>>> a = datetime.datetime.now()
>>> # ...wait a while...
>>> b = datetime.datetime.now()
>>> print(b-a)
0:03:43.984000
```

или, если не нужны микросекунды

```python
>>> a = datetime.datetime.now().replace(microsecond=0)
>>> b = datetime.datetime.now().replace(microsecond=0)
>>> print(b-a)
0:03:43
```

[Документация](https://docs.python.org/3/library/datetime.html?highlight=datetime#module-datetime)

[[date-and-time-in-python]]

Еще материалы:

- [[2021-04-02-daily-note]] - внизу заметки про то, как посчитать определенный день недели
- [[декоратор-wait-для-behave]]
- [[time]]
- [[calendar]]
- [[dateutil]]
- [[pytz]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[date-and-time-in-python]: date-and-time-in-python "Date and time in python"
[2021-04-02-daily-note]: ../posts/2021-04-02-daily-note "Про работу behave и unittest и немного про datetime"
[декоратор-wait-для-behave]: %D0%B4%D0%B5%D0%BA%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80-wait-%D0%B4%D0%BB%D1%8F-behave "Декоратор wait для behave"
[time]: time "Time"
[calendar]: calendar "Calendar"
[dateutil]: dateutil "Dateutil"
[pytz]: pytz "Pytz"
[//end]: # "Autogenerated link references"