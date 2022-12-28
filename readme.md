# Моя база знаний

```vscode
Foam: Show Graph
```

```vscode
Foam: Create New Note from Template
```

`alt+d` создает ежедневную заметку

`alt+с` пометить флажок как прочитанный или снять флаг

`ctrl+b` сделать болдом

`ctrl+i` италик

`ctrl+alt+v` вставка картинок из буфера

`alt+d` создает заметку с текущей датой в папке journal.

## Создание ссылок

1. copy the following text: [https://google.com](https://google.com)
2. select me and paste
3. [select me and paste](https://google.com)

## Tables

`alt+shift+f` formats a table. Place the cursor in the table below and format the table.

| column 1 | column 2|
|-|-|
| one element | another element|
| second row| last cell|

---

## Search

Search in your repo with `cmd+shift+f`: type "search" (go back to the file explorer with `cmd+shift+e`)

## Templates

`Foam: Create New Note From Template`

- `list`
- `note`

## Installation

required `ruby => 2.6.0` (install `rvm`, `openssl` with `rvm pkg install openssl` and install required ruby with `rvm install ruby-<version> --with-openssl-dir=/usr/share/rvm/usr`, `gem update --system` and `bundle install`)

[install jekill](https://jekyllrb.com/docs/installation/)

## Use

`rvm use 2.6.0`

`make serve`

`make build`
