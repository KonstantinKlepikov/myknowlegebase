---
title: Python dict concatenate and way to convert dict to namedtuple
description: Как конкатенировать словари? как преобразовать словарь в namedtuple и немного про property в python
category: post
---
## Python dict concatenate

```python
d1={1:2,3:4}
d2={5:6,7:9}
d3={10:8,13:22}
```

Самый быстрый

```python
d4 = dict(d1, **d2); d4.update(d3)
```

Еще

```python
d4 = {}
for d in (d1, d2, d3):
    d4.update(d)
```

```python
d4 = dict(d1)
for d in (d2, d3):
    d4.update(d)
```

[Ссылка на источник и обсуждение](https://stackoverflow.com/a/1784128/15966204)

## Dict to namedtuple

[Статья на оверфло](https://stackoverflow.com/a/43921348/15966204)

Создаем объект именованного кортежа из словаря

```python
MyTuple = namedtuple('MyTuple', d)
```

Затем распаковываем в инстанс этот же словарь

```python
my_tuple = MyTuple(**d)
```

## Property в классах - как использовать

Приватные атрибуты через сет/гет

```python
class SampleClass1:

    def __init__(self, a):
        ## calling the set_a() method to set the value 'a' by checking certain conditions
        self.set_a(a)

    ## getter method to get the properties using an object
    def get_a(self):
        return self.__a

    ## setter method to change the value 'a' using an object
    def set_a(self, a):

        ## condition to check whether 'a' is suitable or not
        if a > 0 and a % 2 == 0:
            self.__a = a
        else:
            self.__a = 2
```

Через проперти

```python
class Property:

    def __init__(self, var):
        ## initializing the attribute
        self.a = var

    @property
    def a(self):
        return self.__a

    ## the attribute name and the method name must be same which is used to set the value for the attribute
    @a.setter
    def a(self, var):
        if var > 0 and var % 2 == 0:
            self.__a = var
        else:
            self.__a = 2
```

Можно создават ьконструкции, в которых "морозить" данные ээкземпляров. [Подробнее](https://www.datacamp.com/community/tutorials/property-getters-setters?utm_source=adwords_ppc)
