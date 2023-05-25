---
description: xlsxwriter - xlsx files on python
title: Пакет для создания xlsx файлов на python. xlswxriter
tags: templating
---
XlsxWriter — это модуль Python, который можно использовать для записи текста, чисел, формул и гиперссылок на несколько листов в файле Excel 2007+ XLSX. Он поддерживает такие функции, как форматирование и многие другие, в том числе:

- 100% совместимые файлы Excel XLSX.
- Полное форматирование.
- Объединенные ячеек.
- Имена.
- Графики.
- Автофильтры.
- Проверка данных и выпадающие списки.
- Условное форматирование.
- Изображения PNG/JPEG/GIF/BMP/WMF/EMF.
- Мультиформатные строки.
- Комментарии к ячейкам.
- Текстовые поля.
- Интеграция с Pandas и Polars.
- Режим оптимизации памяти для записи больших файлов.

`pip install XlsxWriter`

## Работа с пакетом

- [простой пример создания xlsx файла](https://xlsxwriter.readthedocs.io/tutorial01.html)
- [пример добавления форматирования](https://xlsxwriter.readthedocs.io/tutorial02.html)
- [пример записи разных типов данных](https://xlsxwriter.readthedocs.io/tutorial03.html)

[Создание документа](https://xlsxwriter.readthedocs.io/tutorial01.html).

```python
import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    worksheet.write(row, col, item)
    worksheet.write(row, col + 1, cost)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()
```

[Форматирование документа](https://xlsxwriter.readthedocs.io/tutorial02.html). Объекты формата представляют все свойства форматирования, которые можно применить к ячейке в Excel, такие как шрифты, форматирование чисел, цвета и границы, передава в качестве аргумента в `worksheet.write()`

```python
import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses02.xlsx')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Add a number format for cells with money.
money = workbook.add_format({'num_format': '$#,##0'})

# Write some data headers.
worksheet.write('A1', 'Item', bold)
worksheet.write('B1', 'Cost', bold)

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# Start from the first cell below the headers.
row = 1
col = 0

# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    worksheet.write(row, col, item)
    worksheet.write(row, col + 1, cost, money)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total', bold)
worksheet.write(row, 1, '=SUM(B2:B5)', money)

workbook.close()
```

[Запись разных типов данных](https://xlsxwriter.readthedocs.io/tutorial03.html)

```python
from datetime import datetime
import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses03.xlsx')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': 1})

# Add a number format for cells with money.
money_format = workbook.add_format({'num_format': '$#,##0'})

# Add an Excel date format.
date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

# Adjust the column width.
worksheet.set_column(1, 1, 15)

# Write some data headers.
worksheet.write('A1', 'Item', bold)
worksheet.write('B1', 'Date', bold)
worksheet.write('C1', 'Cost', bold)

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', '2013-01-13', 1000],
    ['Gas',  '2013-01-14',  100],
    ['Food', '2013-01-16',  300],
    ['Gym',  '2013-01-20',   50],
)

# Start from the first cell below the headers.
row = 1
col = 0

for item, date_str, cost in (expenses):
    # Convert the date string into a datetime object.
    date = datetime.strptime(date_str, "%Y-%m-%d")

    worksheet.write_string(row, col, item)
    worksheet.write_datetime(row, col + 1, date, date_format)
    worksheet.write_number(row, col + 2, cost, money_format)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total', bold)
worksheet.write(row, 2, '=SUM(C2:C5)', money_format)

workbook.close()
```

### [Workbook](https://xlsxwriter.readthedocs.io/workbook.html#Workbook)

Класс реализует конструктор новго excel документа. Он предоставляет апи управления используемой памятью и реализует протокол контекстного менеджера.

```python
from io import BytesIO
import xlsxwriter

output = BytesIO()

with xlsxwriter.Workbook('hello_world.xlsx') as workbook:
    worksheet = workbook.add_worksheet(output)
    worksheet.write('A1', 'Hello world')

xlsx_data = output.getvalue()
```

- `workbook.add_worksheet()` реализует добавление страницы в документ
- `workbook.add_format()` реализует добавление свойств из Format или позже
- `workbook.add_chart()` создает объект диаграмы
- `workbook.add_chartsheet()` добавляет лист диаграмы
- `workbook.close()`
- `workbook.set_size()` размер окна рабочей области книги
- `workbook.tab_ratio()` добавляет полосы прокрутки
- `workbook.set_properties()` добавляет стандартные свойства, такие как тайтл, автор и т.п.
- `workbook.set_custom_property()`
- `workbook.define_name()` добавляет имя, которое можно использовать как переменную в xlsx
- `workbook.add_vba_project()`
- `workbook.set_vba_name()`
- `workbook.worksheets()` список вккладок
- `workbook.get_default_url_format()`
- `workbook.set_calc_mode()`
- `workbook.use_zip64()`
- `workbook.read_only_recommended()`

### [The Format Class](https://xlsxwriter.readthedocs.io/format.html#format)

```python
cell_format1 = workbook.add_format()  # Set properties later.
cell_format2 = workbook.add_format(props)  # Set properties at creation.
```

```python
cell_format = workbook.add_format()
cell_format.set_bold()
cell_format.set_font_color('red')
```

```python
cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
```

После создания объекта Format и установки его свойств его можно передать в качестве аргумента методам `write()`, `set_row()`, `set_column()` рабочего листа

```python
worksheet.write(0, 0, 'Foo', cell_format)
worksheet.write_string(1, 0, 'Bar', cell_format)
worksheet.write_number(2, 0, 3, cell_format)
worksheet.write_blank (3, 0, '', cell_format)

worksheet.set_row(0, 18, cell_format)
worksheet.set_column('A:D', 20, cell_format)
```

В отсутствии утсановленного офрмата используется дефолтный Excel 2007+ cell format Calibri 11. При желании уже установленное форматирование можно переопределить позже в коде. Поддерживаются различные числовые форматы. [Смотри подробнее про методы форматирования и свойства Format](https://xlsxwriter.readthedocs.io/format.html#format)

### Worksheet class

Основной метод `worksheet.write()` Для записи разных типов доступно несколько дополнительных методов:

- `write_string()`
- `write_number()`
- `write_blank()`
- `write_formula()`
- `write_datetime()`
- `write_boolean()`
- `write_url()`
- `write_rich_string()`

`worksheet.add_write_handler()` добавляет функцию обратного вызова в метод `write()` для обработки определяемых пользователем типов. Можно добавлять множественные колбеки, но только один будет валиден для одного типа. Один и тот же колбек можно применять к разным типам.

```python
def write_uuid(worksheet, row, col, uuid, format=None):
    string_uuid = str(uuid)
    return worksheet.write_string(row, col, string_uuid, format)

worksheet.add_write_handler(uuid.UUID, write_uuid)

my_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')

# now use
my_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
worksheet.write('A1', my_uuid)
```

Кроме того, можно писать строки и колонки

- `write_row()` Напишите строку данных, начиная с (row, col).
- `write_column()` Напишите столбец данных, начиная с (row, col)
- `set_row()` Установите свойства для ряда ячеек.
- `set_row_pixels()` Задайте свойства строки ячеек с высотой строки в пикселях.
- `set_column()`
- `set_column_pixels()`

Дополнительно:

- `autofit()` Имитирует автоподгонку по ширине столбцов.
- `insert_image()`
- `insert_chart()`
- `insert_textbox()`
- `insert_button()`
- `data_validation()`
- `conditional_format()`
- `add_table()`
- `write_comment()`
- `show_comments()`
- `set_comments_author()`
- `get_name()`
- `activate()` Сделайте рабочий лист активным, то есть видимым рабочим листом.
- `select()` Установите вкладку рабочего листа как выбранную.
- `hide()`
- `set_first_sheet()`
- `merge_range()` Объединить диапазон ячеек.
- `autofilter()` Установите область автофильтра на листе.
- `filter_column()`
- `filter_column_list()`
- `set_selection()` Установите выбранную ячейку или ячейки на листе.
- `set_top_left_cell()` Установите первую видимую ячейку в левом верхнем углу рабочего листа.
- `freeze_panes()`
- `split_panes()`
- `set_zoom()`
- `right_to_left()`
- `hide_zero()`
- `set_background()`
- `set_tab_color()`
- `protect()` Защитить элементы рабочего листа от модификации (усьанавливается пароль)
- `unprotect_range()`
- `set_default_row()` Установите свойства строки по умолчанию.
- `outline_settings()`
- `set_vba_name()`
- `ignore_errors()`

Дополнительно [можно задать параметры страницы](https://xlsxwriter.readthedocs.io/page_setup.html) (к примеру формат печатного листа и etc)

### [The Chart Class](https://xlsxwriter.readthedocs.io/chart.html)

### [The Chartsheet Class](https://xlsxwriter.readthedocs.io/chartsheet.html)

### [The Exceptions Class](https://xlsxwriter.readthedocs.io/exceptions.html)

Смотир еще:

- [примеры обрадотки различных типов данных иприемы работы с докуменами](https://xlsxwriter.readthedocs.io/contents.html) (много)
- [[шаблонизаторы]]
- [[toml]]
- [[yaml]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[шаблонизаторы]: ../lists/шаблонизаторы "Шаблонизаторы"
[toml]: toml "Toml"
[yaml]: yaml "Yaml"
[//end]: # "Autogenerated link references"