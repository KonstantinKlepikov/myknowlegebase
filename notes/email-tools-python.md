---
description: Инструменты для работы с почтой в стандартной библиотеке python
tags: python-standart-library python
title: Email tools in python
---
[smtplib](https://docs.python.org/3/library/smtplib.html) - это клиент smtp-протокола, взаимодействующий с почтовым сервером. Он реализует соединение, отправку/получение сообщений, аутентификацию и шифрование.

[imaplib](https://docs.python.org/3/library/imaplib.html) реализует клиент протокла imap4,  [poplib](https://docs.python.org/3/library/poplib.html) клиент протокола pop3

[smtpb](https://docs.python.org/3/library/smtpd.html) реализует smtp-сервер, используемый в smtplib. В настоящий момент устарел (т.к. построена на базе модуля `asyncore`, который депрекейтед начиная с python3.6). Вместо него рекомендуется использовать асинхронный smtp-сервер [aiosmtp](https://aiosmtpd.readthedocs.io/en/latest/), построенный на базе [[asyncio]]

[mailbox](https://docs.python.org/3/library/mailbox.html) определяет АПИ для доступа к сообщениям электронной почты. Поддерживаемые форматы хранения Maildir, mbox, MH, Babyl и MMDF (чаще всего встречаются первые два). Формат mbox хранит содержимое почтового ящика в виде отдельного текстового файла, что упрощает работу с ним как с простым фалом. Недостаток такого подхода - потоконебезопасность из-за чего доступ к ящику приходится блокировать для других потребителей на время операций. Maildir хзранит почтовый ящик в виде папок и подпапок, что частично снимает проблему блокировки.

mailbox обеспечивает:

- создание почтовых ящиков
- чтение сообщений
- удаление сообщений
- создание подпапок (если это допустимо форматом)
- пометка сообщений флагами

[email](https://docs.python.org/3/library/email.html) реализует обработку электронной почты и ее содержимого. Модуль реализует обработку и представление email-сообщений, а так-же парсинг. Так-эже полезно знать про:

- `mimetypes` преобразует имя файла или URL-адрес в тип MIME, связанный с расширением файла. Обеспечиваются преобразования из имени файла в тип MIME и из типа MIME в расширение
- [base64](https://docs.python.org/3/library/base64.html)

Смотри еще:

- [[python-standart-library]]
- [[asyncio]]
- [[python-filesystem]]
- [[nets-with-python]]
- [[2022-01-04-daily-note]] как запустить локальный smtp для отладки

- [red-mail приложение для формирования и отправки писем](https://github.com/Miksus/red-mail)
- [mailu почтовый сервер](https://github.com/Mailu/Mailu/tree/1.9)
- [Envelope Insert](https://github.com/CZ-NIC/envelope) a message and attachments and send e-mail / sign / encrypt contents by a single line.
- [Sending Emails With Python](https://realpython.com/python-send-email/)
- [flanker](https://github.com/mailgun/flanker) Python email address and Mime parsing library
- [yagmail](https://github.com/kootenpv/yagmail) Send email in Python conveniently for gmail using yagmail



[asyncio]: asyncio "Asyncio"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[python-filesystem]: python-filesystem "Работа с файлами в python"
[nets-with-python]: nets-with-python "Nets and internet with python"
[2022-01-04-daily-note]: ../posts/2022-01-04-daily-note "Proxy в selenium, запуск локального smtp и несколько вопросов про pandas"
