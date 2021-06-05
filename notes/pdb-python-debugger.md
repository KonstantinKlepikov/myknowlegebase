# pdb-python-debugger

Дебагер #python из стандартной сбиблиотеки.

[Документация](https://docs.python.org/3/library/pdb.html)

```python
>>> import pdb
>>> import mymodule
>>> pdb.run('mymodule.test()')
> <string>(0)?()
(Pdb) continue
> <string>(1)?()
(Pdb) continue
NameError: 'spam'
> <string>(1)?()
(Pdb)
```

Можно запускать из терминала. [Подробнее как работать через терминал](https://docs.python.org/3/library/pdb.html#debugger-commands)

`python3 -m pdb myscript.py`

[[pytest]]