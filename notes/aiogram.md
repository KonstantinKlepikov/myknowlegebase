---
description: Aiogram - библиотека для создания ботовв для telegram на python
tags: python bots asynco
title: Telegram python bots with aiogram
---
## [aiogram](https://github.com/aiogram/aiogram)

Is a pretty simple and fully asynchronous framework for Telegram Bot API written in Python 3.7 with [[asyncio]] and [[aiohttp]].

[Документация](https://docs.aiogram.dev/en/latest/)

`pip install -U aiogram`

```python
"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

# Then you have to initialize bot and dispatcher instances.
# Bot token you can get from @BotFather
API_TOKEN = 'BOT TOKEN HERE'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# interaction with bots starts with one command.
# Register your first command handler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

# If you want to handle all text messages in
# the chat simply add handler without filters
@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

[Больше примеров](https://docs.aiogram.dev/en/latest/examples/index.html)

АПИ реализуется с помощью классов `Bot`и `Dispatcher`. Bot реализует [[aiohttp]] сервер и связку с api telegram. Dispatcher обрабатывает входящие обновления: сообщения, отредактированные сообщения, сообщения канала, отредактированные сообщения канала, встроенные запросы, выбранные встроенные результаты, запросы колбеков, запросы на доставку, запросы пречекаута. `execitor` это [хелпер](https://docs.aiogram.dev/en/latest/utils/executor.html) для запуска бота в разных режимах, к примеру ниже в long-polling mode.

```python
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

Подробнее:

- [Bot object](https://docs.aiogram.dev/en/latest/telegram/bot.html)
- [Dispatcher](https://docs.aiogram.dev/en/latest/dispatcher/index.html)
- [Executor](https://docs.aiogram.dev/en/latest/utils/executor.html)

### [Bot](https://docs.aiogram.dev/en/latest/telegram/bot.html#telegram-bot) class

Методы:

- `download_file_by_id` Скачать файл по file_id в целевой файл или каталог
- `get_updates` получать входящие обновления с помощью long polling
- `set_webhook` Используйте этот метод, чтобы указать URL-адрес и получать входящие обновления через исходящий вебхук. Всякий раз, когда для бота появляется обновление, мы отправляем HTTPS-запрос POST на указанный URL-адрес, содержащий сериализованное обновление JSON. В случае неудачного запроса мы откажемся после разумного количества попыток. Возвращает `True` в случае успеха.
- `delete_webhook` удалить интеграцию с вебхуком
- `get_webhook_info`
- `get_me` simple method for testing your bot’s auth token
- `log_out` Используйте этот метод для логаута от сервера API перед локальным запуском бота. Вы должны выйти, прежде чем запускать локально, иначе нет гарантии, что бот будет получать обновления. После успешного звонка вы не сможете снова войти в систему с тем же токеном в течение 10 минут. Возвращает `True` в случае успеха.
- `close_bot` Используйте этот метод, чтобы закрыть экземпляр бота перед его перемещением с одного локального сервера на другой. Вам необходимо удалить вебхук перед вызовом этого метода, чтобы гарантировать, что бот не запустится снова после перезапуска сервера. Метод вернет ошибку 429 в первые 10 минут после запуска бота. Возвращает True в случае успеха
- `send_message` для текстовых сообщений
- `forward_message`
- `copy_message`
- `send_photo`
- `send_audio`
- `send_document`
- `send_video`
- `send_animation`
- `send_voice`
- `send_video_note`
- `send_media_group`
- `send_location`
- many send methods and chat_methods

### [Dispatcher](https://docs.aiogram.dev/en/latest/dispatcher/index.html#dispatcher-class) class

Методы:

- `skip_updates` Вы можете пропустить старые входящие обновления из очереди. Этот метод не рекомендуется использовать на проде
- `process_updates` Обработать список обновлений
- `process_update`
- `reset_webhook`
- `start_polling` старт long-polling
- `stop_polling`
- `wait_closed` дождаться завершения long pooling
- `is_polling`
- `message_handler` декоратор для обработки сообщений

```python
# Simple commands handler
@dp.message_handler(commands=['start', 'welcome', 'about'])
async def cmd_handler(message: types.Message):
    ...

# Filter messages by regular expression
@dp.message_handler(regexp='^[a-z]+-[0-9]+')
async def msg_handler(message: types.Message):
    ...

# Filter messages by command regular expression
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['item_([0-9]*)']))
async def send_welcome(message: types.Message):
    ...

# Filter by content type
@dp.message_handler(content_types=ContentType.PHOTO | ContentType.DOCUMENT)
async def audio_handler(message: types.Message):
    ...

# Filter by custom function
@dp.message_handler(lambda message: message.text and 'hello' in message.text.lower())
async def text_handler(message: types.Message):
    ...

# Use multiple filters
@dp.message_handler(commands=['command'], content_types=ContentType.TEXT)
async def text_handler(message: types.Message):
    ...

# Register multiple filters set for one handler
@dp.message_handler(commands=['command'])
@dp.message_handler(lambda message: demojize(message.text) == ':new_moon_with_face:')
async def text_handler(message: types.Message):
    ...
```

- `register_edited_message_handler` зарегистрировать обработчик для редактируемого сообщения
- `edited_message_handler` декоратор
- and ome register and decorator method for many types of messages
- `current_state` Получить текущее состояние пользователя в чате в качестве контекста
- `throttle`
- `check_key` Получить информацию о ключе в бакете
- `release_key` выпустить залоченный ключ
- `async_task` декоратор, который выполняет хендлер как асинхронный таск. Это надо использовать для медленных хендлеров с таймоутом.
- `throttled`
- `bind_filter`, `unbind_filter`
- `setup_middleware`

## Aiogram 3.x

Начиная с 3.x интерфейс aiogram полностью поменялся.

- [подробный гайд по новому интерфейсу](https://mastergroosha.github.io/aiogram-3-guide/)
- [docs](https://docs.aiogram.dev/en/dev-3.x/index.html)
- [aiogram_dialog](https://github.com/Tishka17/aiogram_dialog) is a framework for developing interactive messages and menus in your telegram bot like a normal GUI application. [docs](https://aiogram-dialog.readthedocs.io/en/latest/)
- [magic-filter](https://github.com/aiogram/magic-filter/)fro aiogram provides magic filter based on dynamic attribute getter
- [конечные автоматы](https://tproger.ru/translations/finite-state-machines-theory-and-implementation/)

Смотри еще:

- [примеры с aiogram](https://docs.aiogram.dev/en/latest/examples/index.html)
- [Пишем Telegram-ботов с aiogram 3.x](https://mastergroosha.github.io/aiogram-3-guide/) неплохое и подробное руководство
- [[aiogram-dialog]]
- [[telegram-bots]]
- [[aiohttp]]
- [[asyncio]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[asyncio]: asyncio "Asyncio"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[telegram-bots]: telegram-bots "Telegram python bots"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[asyncio]: asyncio "Asyncio"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[telegram-bots]: telegram-bots "Telegram python bots"
[aiohttp]: aiohttp "Aiohttp асинхронный клиент-свервер на python."
[asyncio]: asyncio "Asyncio"
[//end]: # "Autogenerated link references"