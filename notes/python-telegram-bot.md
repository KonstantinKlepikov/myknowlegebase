---
description: python-telegram-bot - библиотека для создания ботов для telegram на python
tags: python bots asyncio
title: Python telegram bot lib
---
`pip install python-telegram-bot --upgrade`

## Optional Dependencies

- `pip install "python-telegram-bot[passport]"` installs the cryptography>=39.0.1 library. Use this, if you want to use Telegram Passport related functionality.
- `pip install "python-telegram-bot[socks]"` installs httpx\[socks]. Use this, if you want to work behind a Socks5 server.
- `pip install "python-telegram-bot[http2]"` installs httpx\[http2]. Use this, if you want to use HTTP/2.
- `pip install "python-telegram-bot[rate-limiter]"` installs aiolimiter~=1.1.0. Use this, if you want to use `telegram.ext.AIORateLimiter`.
- `pip install "python-telegram-bot[webhooks]"` installs the tornado~=6.2 library. Use this, if you want to use `telegram.ext.Updater.start_webhook/telegram.ext.Application.run_webhook`.
- `pip install "python-telegram-bot[callback-data]"` installs the cachetools~=5.3.1 library. Use this, if you want to use arbitrary callback_data.
- `pip install "python-telegram-bot[job-queue]"` installs the APScheduler~=3.10.1 library and enforces pytz>=2018.6, where pytz is a dependency of `APScheduler`. Use this, if you want to use the `telegram.ext.JobQueue`.

To install multiple optional dependencies, separate them by commas, e.g. pip install `"python-telegram-bot[socks,webhooks]"`.

Additionally, two shortcuts are provided:

- `pip install "python-telegram-bot[all]"` installs all optional dependencies.
- `pip install "python-telegram-bot[ext]"` installs all optional dependencies that are related to `telegram.ext`, i.e. [rate-limiter, webhooks, callback-data, job-queue].

## [Примеры](https://docs.python-telegram-bot.org/en/stable/examples.html)

[Простейший эхобот](https://docs.python-telegram-bot.org/en/stable/examples.echobot.html)

```python
#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
```

Смотри еще:

- [[telegram-bots]]
- [документация](https://docs.python-telegram-bot.org/en/stable/#)
- [wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki)
- [API telegram](https://core.telegram.org/)
- [[aiogram]] библиотека
- [[aiogram-dialog]] библиотека


[telegram-bots]: telegram-bots "Telegram python bots"
[aiogram]: aiogram "Telegram python bots with aiogram"
[aiogram-dialog]: aiogram-dialog "Aiogram extention aiogram-dialog"
