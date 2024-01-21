---
description: Работа с сетями и интернет в стандартной библиотеке python
tags: python-standart-library servers python
title: Nets and internet with python
---
## Работа с сетями

### [ipaddress](https://docs.python.org/3/library/ipaddress.html)

Модуль реализует проверку, сравнение и другие операции с сетевыми адресами IPv4/IPv6. Позволяет работать с сетевыми адресами и диапазонами адресов. а так-же с сетевыми интерфейсами (сетевой адроес, предоставленный в виде адреса хоста и сетевого префикса или маски сети)

### [socket](https://docs.python.org/3/library/socket.html)

Низкоуровневый интерфейс к c-библиотеке socket, используется для взаимодействия с сетевыми службами с использованием сокетов BSD. Решает задачи преобразования именит сервера в адрес и формирование данных для передачи по сети.

Сокет - это конечная точка соединения, используемая для локального обмена или обмена по сети интернет. Процессом передачи управляют два свойства сокета - семейство адресов, задающее сетевой протокол модели OSI и тип сокета, соответствующий протоколу транспортного уровня.

Формат адреса, требуемый конкретным объектом сокета, выбирается автоматически на основе семейства адресов, указанного при создании объекта сокета. Адреса сокетов представлены следующим образом:

- адрес сокета AF_UNIX, привязанный к узлу файловой системы, представлен в виде строки с использованием кодировки файловой системы и обработчика ошибок. Сокеты домена Unix (UDS) позволяют передавать данные непосредственно из процесса в процесс без прохождения сетевого стека, но применеение UDS ограничено процессами, выполняемыми в одной системе.
- семейство адресов AF_INET спользуется для IPv4 адресации. Адреса IPv4 имеют длину 4 байта и представляются в виде последовательности 4-х чисел, разделенных точкой (например 10.2.2.15). Большинство адресов в интернет - IPv4. В socket используется пара (хост, порт), где host - это строка, представляющая либо имя хоста в нотации интернет-домена, например daring.cwi.nl, либо адрес IPv4, например, 100.50.200.5, а порт - целое число.
- для семейства адресов AF_INET6 используется четыре кортежа (хост, порт, flowinfo, scope_id). IPv6 обеспечивает поддержку 128-битновых адресов
- еще доступны AF_NETLINK, AF_TIPC, AF_CAN, SYSPROTO_CONTROL, AF_BLUETOOTH, AF_ALG, AF_VSOCK, AF_PACKET, AF_QIPCRTR, IPPROTO_UDPLITE. [Подробнее](https://docs.python.org/3/library/socket.html#socket-families)

Обычно реализуются два типа сокетов - SOCK_DGRAM (UDP), не обеспечивающие высокую надежность передачи данных, т.к. они не гарантируют доставку и SOCK_STREAM (TCP), гарантирующих доставку. Большинство протоколов прикладного уровня (к примеру [[http]]) реализовано поверх TCP. UDP в основном используется, когда порядок получения сообщений не существенен и для многоадресном вещании.

Модуль socket реализует:

- поиск хостов в сети и преобрназование имени хоста в сетевой адрес
- получение информации ор сетевых службах
- получение информации об адресе сервера
- реализацию программных конструкций сервер-клиент на базе TCP/IP, UDP, UDS и т.д.
- многоадресное вещание
- отправку текстовых и двоичных данных
- неблокирующий ввод/вывод

### [selectors](https://docs.python.org/3/library/selectors.html)

Предоставляет высокоуровневый интерфейс для одновременного наблюдения за несколькими сокетами и обеспечивает взаимодействие сетевых серверов с несколькими клиенатми. Реализован с помощью модуля [select](https://docs.python.org/3/library/select.html)- это низкоуровневый интерфейс.

Объект селектора имеет методы, позволяющие указывать какие события, связанные с сокетом, необходимо отслеживать и позволяет вызывающему оъъекту ожидать события платформенным способом и реализовывать отслеживание готовность сокетов к вводу/выводу и вызывать колбеки.

### [socketserver](https://docs.python.org/3/library/socketserver.html)

Реализует фреймворк для создания сетевого сервера, поддерживающие протоколы UDP, TCP и UDS. Фреймворк упрощает обработку синхронных сетевых запросов, кроме того он поставляет примесные классы, позволяющие выводить запросы в отдельный поток или процесс.

Фреймворк реализует высокоуровневый объектный подход, что позволяет применять классы практически без измененеий. Достыпны классы сервера и обработчика запросов. Сервер отвечает за прослушивание сокетов, установку соединений и т.д., а обработчик за протокол обработки данных (интерпретация, парсинг, отправка).

### [ssl](https://docs.python.org/3/library/ssl.html)

Этот модуль обеспечивает доступ к средствам шифрования Transport Layer Security и одноранговой аутентификации для сетевых сокетов, как на стороне клиента, так и на стороне сервера. Этот модуль использует библиотеку OpenSSL.

## Работа с интернет

### [cgi](https://docs.python.org/3/library/cgi.html) и [wsgiref](https://docs.python.org/3/library/wsgiref.html)

cgi определяет ряд утилит для использования скриптами CGI, написанными на Python.

wsgiref - это стандартный интерфейс WSGI между программным обеспечением веб-сервера и веб-приложениями, написанными на Python. Наличие стандартного интерфейса упрощает использование приложения, поддерживающего WSGI, с рядом различных веб-серверов.

Вникать в модули нужно в основном для разработки/поддержания http-фреймворков.

\* Модуль [cgitb](https://docs.python.org/3/library/cgitb.html) предоставляет специальный обработчик исключений для скриптов Python

### [urlib](https://docs.python.org/3/library/urllib.html)

- [urlib.parse](https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse) позволяет работать со строками url-ов
- [urlib.requests](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) открытие удаленных ресурсов, получение удаленного содержимого
- [urlib.robotparser](https://docs.python.org/3/library/urllib.robotparser.html#module-urllib.robotparser) работа с `robots.txt`
- [urlib.errors](https://docs.python.org/3/library/urllib.error.html#module-urllib.error) эксепшены для urlib.requests

Смотри еще:

- [urlib3](https://urllib3.readthedocs.io/en/stable/)
- [Requests: HTTP for Human](https://docs.python-requests.org/en/latest/)s

## [http](https://docs.python.org/3/library/http.html)

Реализует базовые инструменты для написания http-фреймворка (в т.ч. предоставляет обработчик коды статусов)

- http.client низкоуровневый http-клиент
- http.server HTTP сервер на базе socketserver
- http.cookies управление куками
- http.cookiejar автоматическая обработка кук

## Протоколы

[ftp](https://docs.python.org/3/library/ftplib.html), [nntp](https://docs.python.org/3/library/nntplib.html), [telnet](https://docs.python.org/3/library/telnetlib.html) а так же почтовые протоколы [[email-tools-python]]

## [uuid](https://docs.python.org/3/library/uuid.html)

Генерация уникальных значений идентификаторов ресурсов (uuid).

### [xmlrpc](https://docs.python.org/3/library/xmlrpc.html)

XML-RPC сервер, в настоящий момент стандарт можно считать устаревшим.

Смотри еще:

- [[asyncio]]
- [[http]]
- [[http-cors]]
- [[http-methods]]
- [[http-requests-errors]]
- [[http-заголовки]]
- [[python-standart-library]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[http]: ../lists/http "Http"
[email-tools-python]: email-tools-python "Email tools in python"
[asyncio]: asyncio "Asyncio"
[http-cors]: http-cors "Http cors"
[http-methods]: http-methods "Http methods"
[http-requests-errors]: http-requests-errors "Http requests"
[http-заголовки]: http-%D0%B7%D0%B0%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BA%D0%B8 "Http заголовки"
[python-standart-library]: ../lists/python-standart-library "Стандартная библиотека python и полезные ресурсы"
[//end]: # "Autogenerated link references"