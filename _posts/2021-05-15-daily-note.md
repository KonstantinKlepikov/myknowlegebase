# Daily note,  2021-05-15, Saturday

## Convert a String to Variable Name in Python

[Статья](https://www.delftstack.com/howto/python/python-string-to-variable-name/)

### Вариант №1 - globals()

Функция `globals()` в #python возвращает словарь текущей глобальной таблицы символов. В глобальной таблице символов хранится вся информация, относящаяся к глобальной области видимости программы, доступ к которой можно получить с помощью функции `globals()`.

```python
user_input = "apple"
globals()[user_input] = 50
print(apple)
print(type(apple))

>>> 50
>>> <class 'int'>
```

### Вариант №2 locals() аналогично

```python
user_input = "apple"
locals()[user_input] = 50
print(apple)
print(type(apple))
```

### №3 exec()

Функция `exec()` используется для динамического выполнения программы #python. Способ не является безопасным.

```python
name = 'Elon'
exec("%s = %d" % (name, 100))
print(Elon)

>>> 1000
```

Внутри функции `exec()` у нас есть %s и %d, используемые в качестве заполнителя для метки и значения переменной соответственно. Это означает, что мы присваиваем строке целочисленное значение с помощью оператора присваивания =, %s, и %d заключены в кавычки "".
