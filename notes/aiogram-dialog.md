---
description: Aiogram-dialog - библиотека для создания клавиатур и диалогов в telegram для aiogram
tags: python bots asynco
title: Aiogram extention aiogram-dialog
---
Aiogram-dialog — это фреймворк графического интерфейса для телеграмм-бота. Он вдохновлен идеями Android SDK и React.js.

## Versions

На момент написания статьи последней дев-версией был 2.0b17. Как мигрировать [тут](https://github.com/Tishka17/aiogram_dialog/blob/develop/docs/migration.rst).

Пример кода смотри [тут](https://github.com/Tishka17/aiogram_dialog/tree/develop/example).

Version status

- v1.x stable release, supports aiogram v2.x, bugfix only
- v2.x beta, future release, supports aiogram v3.x

## Основные идеи

- Раздельное извлечение данных и рендеринг сообщений
- Объединененные отрисовки кнопок и обработки кликов
- Улучшенная маршрутизация состояний
- Виджеты

Основным строительным блоком интерфейса является `Window`. Каждое окно представляет собой сообщение, отправляемое пользователю, и обработку реакции пользователя на это сообщение.

Каждое окно состоит из виджетов и функций обратного вызова. Виджеты могут отображать текст сообщения и клавиатуру. Обратные вызовы используются для получения необходимых данных или обработки пользовательского ввода.

Окна объединены в `Dialog`. Это позволяет переключаться между окнами, создавая различные сценарии общения с пользователем.

В более сложных случаях можно создать более одного диалога. Можно запускать новые диалоги, не закрывая предыдущий, и автоматически возвращаться обратно, когда новый диалог закрывается. Можно передавать данные между диалогами, одновременно сохраняя их состояние изолированным.

## Quicl start

`pip install aiogram_dialog`

Создайте [[aiogram]] группу состояний для вашего диалога:

```python
from aiogram.dispatcher.filters.state import StatesGroup, State

class MySG(StatesGroup):
    main = State()
```

Создайте хотя бы одно окно с кнопками или текстом:

```python
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


class MySG(StatesGroup):
    main = State()


main_window = Window(
    Const("Hello, unknown person"),  # just a constant text
    Button(Const("Useless button"), id="nothing"),  # button with text and id
    state=MySG.main,  # state is used to identify window between dialogs
)
```

Создайте диалог с вашими окнами:

```python
from aiogram_dialog import Dialog

dialog = Dialog(main_window)
```

Предположим, что вы создали своего бота с диспетчером и хранилищем состояний, как обычно. Важно, чтобы у вас было хранилище, потому что aiogram_dialog использует FSMContext aiogram для хранения своего состояния

```python
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='BOT TOKEN HERE')
dp = Dispatcher(bot, storage=storage)
```

Чтобы начать использовать ваш диалог, вам необходимо его зарегистрировать. Также библиотека нуждается в некоторых дополнительных регистрациях для своих внутренних процессов. Для этого мы создадим DialogRegistry и используем его для регистрации нашего диалога.

```python
from aiogram_dialog import DialogRegistry

registry = DialogRegistry(dp)  # this is required to use `aiogram_dialog`
registry.register(dialog)  # register a dialog
```

На данный момент мы все настроили. Но диалог не запускается сам. Мы создадим простой обработчик команд, чтобы справиться с этим. Для запуска диалога нам нужен `DialogManager`, который автоматически внедряется библиотекой. Также обратите внимание на `reset_stack` аргумент. Библиотека может запускать несколько диалогов, расположенных друг над другом. В настоящее время нам не нужна эта функция, поэтому мы будем сбрасывать стек при каждом запуске:

```python
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    # Important: always set `mode=StartMode.RESET_STACK` you don't want to stack dialogs
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)
```

Последний шаг, вам нужно запустить бота как обычно:

```python
from aiogram import executor

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

Полный пример (совместим с [[aiogram]] 2.0):

```python
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message

from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

storage = MemoryStorage()
bot = Bot(token='BOT TOKEN HERE')
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


class MySG(StatesGroup):
    main = State()


main_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MySG.main,
)
dialog = Dialog(main_window)
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

## [Виджеты и рендеринг](https://aiogram-dialog.readthedocs.io/en/latest/widgets.html)

### Как передаются данные

Некоторые виджеты содержат фиксированный текст, другие могут отображать динамическое содержимое. Для загрузки данных в окнах и диалогах есть `getter` атрибут. `detter` может быть как функцией, возвращающей данные, так и статическим словарем или списком таких объектов.

```python
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format


class MySG(StatesGroup):
    main = State()


async def get_data(**kwargs):
    return {
        "name": "Tishka17",
    }


dialog = Dialog(
    Window(
        Format("Hello, {name}!"),
        Button(Const("Useless button"), id="nothing"),
        state=MySG.main,
        getter=get_data,  # here we set our data getter
    )
)
```

Часть объектов доступно без геттера, а через атрибут хендлера:

- `dialog_data` - содержимое соответствующего поля из текущего контекста. Обычно он используется для хранения данных между несколькими вызовами и окнами в одном диалоговом окне.
- `start_data` - данные, передаваемые при запуске текущего диалога. Также доступны с помощью `current_context`
- `middleware_data` - данные передаются от промежуточного программного обеспечения к обработчику. Еще можно так `dialog_manager.data`
- `event` - текущее событие обработки, вызвавшее обновление окна. Будьте осторожны, используя его, потому что разные типы событий могут привести к обновлению одного и того же окна.

### Типы виджетов

В настоящее время существует 3 вида виджетов: тексты, клавиатуры и медиа

- Texts, используются для отображения текста в любом месте диалога. Это может быть текст сообщения, заголовок кнопки и так далее.
- Keyboards представляют собой части `InlineKeyboard` [[aiogram]]
- Media представляет мультимедийный аттачмент к сообщению

Также есть 2 основных типа:

- `Whenable` могут быть скрыты или показаны в зависимости от данных или некоторых условий. В настоящее время все виджеты доступны.
- `Actionable` любой виджет с действием (в настоящее время только любой тип клавиатуры). Он имеет id и может быть найден по этому идентификатору. Рекомендуется, чтобы все виджеты с состоянием (например, флаги) имели уникальный идентификатор в диалоговом окне. Кнопки с разным поведением также должны иметь разные идентификаторы.

#### Тексты

- `Const` - возвращает текст без промежуточных значений
- `Format` - форматирует текст с помощью `format`. При использовании в окне данные извлекаются через getter.
- `Multi` - несколько текстов, соединенных разделителем
- `Case` - показывает один из текстов по условию
- `Progress` - показывает индикатор выполнения
- `Jinja` — представляет собой HTML, отображаемый с использованием шаблона jinja2.

#### Клавиатуры

Каждая клавиатура имеет одну или несколько встроенных кнопок. Текст на кнопке отображается с помощью текстового виджета

- `Button` — одна встроенная кнопка. Предоставленный пользователем on_click метод вызывается при нажатии.
- `Url` — одна встроенная кнопка с URL
- `Group` - любая группа клавиатур друг над другом или микс из кнопок
- `ScrollingGroup` — то же, что и `Group`, но с возможностью прокрутки страниц кнопками.
- `ListGroup` - группа виджетов применяемая многократно для каждого элемента в списке
- `Row` - упрощенный вариант группы. Все кнопки расположены в один ряд.
- `Column` — еще одна упрощенная версия группы. Все кнопки размещены в одном столбце по одной в строке.
- `Checkbox` — кнопка с двумя состояниями
- `Select` - динамическая группа кнопок, предназначенная для использования при выборе.
- `Radio` - переключение между несколькими элементами. Подобно select, но сохраняет выбранный элемент и отображает его по-другому.
- `Multiselect` - выбор нескольких элементов. Подобно select/radio, но сохраняет все выбранные элементы и отображает их по-разному.
- `Calendar` — имитирует календарь в виде клавиатуры.
- `SwitchTo`- переключает окно в диалоге, используя предоставленное состояние
- `Next/Back` - переключает состояние вперед или назад
- `Start` - запускает новый диалог без параметров
- `Cancel` - закрывает текущий диалог без результата. Отображается базовый диалог

## [Transitions](https://aiogram-dialog.readthedocs.io/en/latest/transitions.html)

Разговаривая с пользователем, вам нужно будет переключаться между различными состояниями чата. Это можно сделать с помощью четырех типов переходов:

- Переключение состояния внутри диалога. При этом вы просто покажете другое окно.
- Запук диалога в том же стеке. В этом случае диалог будет добавлен в стек задач с пустым контекстом диалога, а соответствующее окно будет показано вместо ранее видимого.
- Начать диалог в новом стеке. В этом случае диалог будет отображаться в новом сообщении и вести себя независимо от текущего.
- Закрыть диалог. Диалог будет удален из стека, его данные стерты. Основной диалог будет снова показан.

### Стек задач

Для работы с несколькими открытыми диалогами в aiogram_dialog есть стек диалогов. Это позволяет открывать диалоги друг над другом («складывать»), поэтому виден только один из них.

Каждый раз, когда вы запускаете диалог, новая задача добавляется поверх стека и создается новый контекст диалога.

Каждый раз, когда вы закрываете диалог, задача и контекст диалога удаляются.

Вы можете запустить один и тот же диалог несколько раз, и несколько контекстов (обозначенных intent_id) будут добавлены в стек с сохранением порядка. Поэтому вы должны быть осторожны, перезапуская диалоги: не забудьте очистить стек, иначе он съест всю вашу память.

Начиная с версии 1.0 вы можете создавать новые стеки, но всегда существует один по умолчанию.

Самое простое, что вы можете сделать, чтобы изменить макет пользовательского интерфейса, — это переключить состояние диалога. Это не влияет на стек задач и просто рисует другое окно. Контекст диалога остается прежним, поэтому все ваши данные по-прежнему доступны.

Есть несколько способов сделать это:

- `dialog.switch_to` метод. Передайте другое состояние, и окно будет переключено
- `dialog.next` метод. Он переключится на следующее окно в том же порядке, в котором они были переданы при создании диалога. Невозможно вызвать, когда последнее окно активно
- `dialog.back` метод. Переключиться на противоположное направление (на предыдущее). Невозможно вызвать, когда активно первое окно

Пример

```python
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const


class DialogSG(StatesGroup):
    first = State()
    second = State()
    third = State()


async def to_second(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.second)


async def go_back(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().back()


async def go_next(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().next()


dialog = Dialog(
    Window(
        Const("First"),
        Button(Const("To second"), id="sec", on_click=to_second),
        state=DialogSG.first,
    ),
    Window(
        Const("Second"),
        Row(
            Button(Const("Back"), id="back2", on_click=go_back),
            Button(Const("Next"), id="next2", on_click=go_next),
        ),
        state=DialogSG.second,
    ),
    Window(
        Const("Third"),
        Button(Const("Back"), id="back3", on_click=go_back),
        state=DialogSG.third,
    )
)
```

Для упрощения у нас есть специальные типы кнопок. Каждый из них может содержать пользовательский текст, если это необходимо:

- `SwitchTo` - switch_to при нажатии. Состояние предоставляется через атрибут конструктора
- `Next` - next при клике
- `Back` - back при клике

[Пример тут](https://aiogram-dialog.readthedocs.io/en/latest/transitions.html)

[Несколько полезных инстурментов контроля реализации диалгов](https://aiogram-dialog.readthedocs.io/en/latest/tools.html)

Смотри еще:

- [документация](https://aiogram-dialog.readthedocs.io/en/latest/overview.html)
- [github](https://github.com/tishka17/aiogram_dialog)
- [[aiogram]]
- [[telegram-bots]]
- [[aiohttp]]
- [[asyncio]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[aiogram]: aiogram "Telegram python bots with aiogram"
[telegram-bots]: telegram-bots "Telegram python bots"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[aiogram]: aiogram "Telegram python bots with aiogram"
[aiogram]: aiogram "Telegram python bots with aiogram"
[aiogram]: aiogram "Telegram python bots with aiogram"
[aiogram]: aiogram "Telegram python bots with aiogram"
[telegram-bots]: telegram-bots "Telegram python bots"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"