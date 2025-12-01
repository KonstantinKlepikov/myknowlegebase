---
title: Proxy в selenium, запуск локального smtp и несколько вопросов про pandas
description: Про proxy в selenium, smtp локально и ошибки в pandas
category: post
---
## Использование proxy вместе с [[selenium]]

[статья](https://medium.com/ml-book/multiple-proxy-servers-in-selenium-web-driver-python-4e856136199d)

Можно спарсить бесплатные прокси, но надо учитывать, что их доступность может быть крайне низкой. Пример

```python
>>> from selenium import webdriver
>>> from selenium.webdriver.chrome.options import DesiredCapabilities
>>> import random

>>> class WebDriver:
...     """Selenium webdriver context manager"""
...     def __init__(self, driver: webdriver.Firefox):
...         self.driver = driver

...     def __enter__(self):
...         return self.driver

...     def __exit__(self, exc_type, exc_val, exc_tb):
...         self.driver.quit()

>>> service = webdriver.firefox.service.Service('./geckodriver', port=8080)

>>> with WebDriver(webdriver.Firefox(service=service)) as driver:

...     driver.get("https://free-proxy-list.net/")
...     html = driver.page_source
...     soup = bs(html, 'html.parser')

...     proxies = soup.find('textarea', class_='form-control').string

>>> prox = [pr for pr in proxies.split('\n') if pr and pr[0].isnumeric()]
>>> random.shuffle(prox)
>>> print(prox)
['94.247.244.120:3128',
 '151.232.72.21:80',
 '103.228.118.78:8080',
 '103.87.164.76:8080',
...
```

[Еще статья](https://www.browserstack.com/guide/set-proxy-in-selenium). [Обсуждение на оверфло](https://stackoverflow.com/questions/17082425/running-selenium-webdriver-with-a-proxy-in-python)

## Использование smtplib на localhost

Необходимо вначале запустить сервер с выводом отладочной информации. Вот так:

```shell
python -m smtpd -n -c DebuggingServer localhost:1025
```

[Подробнее](https://stackoverflow.com/a/20352563/15966204)

Смотри еще [[email-tools-python]]

## Несколько вопросов про [[pandas]]

### Ошибка "ValueError: If using all scalar values, you must pass an index"

В сообщении об ошибке говорится, что если вы передаете скалярные значения, вы должны передать индекс. Решение - не использовать скаляры или передать индекс:

```python
>>> a = 2
>>> b = 3
>>> df = pd.DataFrame({'A': [a,], 'B': [b,]})
>>> df
   A  B
0  2  3
```

```python
>>> df = pd.DataFrame({'A': a, 'B': b}, index=[0])
>>> df
   A  B
0  2  3
```

[Источник](https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi)

### Convert a Pandas DataFrame into a single row DataFrame

```python
df = df[0].stack().swaplevel().to_frame().T
df.columns = df.columns.map('{0[0]}_{0[1]}'.format)
```

[Обсуждение и варианты тут](https://stackoverflow.com/questions/47736022/convert-a-pandas-dataframe-into-a-single-row-dataframe)

### Converting string that looks like a list into a real list - python

Иногда бывает полезно упаковать список в ячейку [[pandas]] в виде строки (т.к. архитектура модуля крайне не способствует хранению списков)

```python
>>> import ast
>>> ast.literal_eval("[(0, 1), (1, 3), (2, 1), (3, 1), (4, 1)]")
[(0, 1), (1, 3), (2, 1), (3, 1), (4, 1)]
>>> ast.literal_eval("[(0, 1, 6), (1, 3,7), (3, 1,4), (3, 1,3), (8, 1,2)]")
[(0, 1, 6), (1, 3, 7), (3, 1, 4), (3, 1, 3), (8, 1, 2)]
>>> ast.literal_eval("[1,2,3,5,3]")
[1, 2, 3, 5, 3]
```

[ссылка на оверфло](https://stackoverflow.com/a/20250415/15966204)


[selenium]: ../notes/selenium "Selenium"
[email-tools-python]: ../notes/email-tools-python "Email tools in python"
[pandas]: ../notes/pandas "Pandas"
