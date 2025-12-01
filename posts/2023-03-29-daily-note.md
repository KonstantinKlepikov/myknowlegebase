---
title: Watchdogtricks, numpy arrais comparison
description: Авторестарт скрипта python после определенных событий в системе и сравнение массивов в Numpy
category: post
tags: python numpy
---
## [How do i watch python source code files and restart when i save?](https://stackoverflow.com/a/55196033/15966204)

Самый простой способ - использовать `wathcdog` как-нибудь так : `watchmedo auto-restart -p "*.py" -R -- python pplication.py`

## [Comparing two NumPy arrays for equality, element-wise](https://stackoverflow.com/questions/10580676/comparing-two-numpy-arrays-for-equality-element-wise)

```python
import numpy as np
(A==B).all()

np.array_equal(A,B)  # test if same shape, same elements values
np.array_equiv(A,B)  # test if broadcastable shape, same elements values
np.allclose(A,B,...) # test if same shape, elements have close enough values
```

Смотри еще [[numpy]]


[numpy]: ../notes/numpy "Numpy"
