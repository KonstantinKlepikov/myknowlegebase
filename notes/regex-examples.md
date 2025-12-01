---
description: Regex в стандартной библиотекой python
tags: python-standart-library python templating
title: Примеры использования модуля re в python
---
## Python regular Expression to get text between two strings

```python
import re

text="""<h3 class="heading">General Purpose</h3>"""
pattern="(<.*?>)(.*)(<.*?>)"

g=re.search(pattern,text)
g.group(2)
```

[сорс](https://stackoverflow.com/questions/40602714/python-regular-expression-to-get-text-between-two-strings)

```python
import re

re.search(r"(?<=AAA).*?(?=ZZZ)", your_text).group(0)
```

[сорс](https://stackoverflow.com/questions/4666973/how-to-extract-the-substring-between-two-markers)

Смотир еще:

- [[regex-basics]]
- [[python-standart-library]]
- [[2022-04-26-daily-note]] как заменить запятые на точки в сложных строках, содержащих смешанные цифры и другие знаки
- [[шаблонизаторы]]


[regex-basics]: regex-basics "Основы регулярных выражений"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[2022-04-26-daily-note]: ../posts/2022-04-26-daily-note "git remote stop tracking and replace comma to dot by re"
[шаблонизаторы]: ../lists/%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80%D1%8B "Шаблонизаторы"
