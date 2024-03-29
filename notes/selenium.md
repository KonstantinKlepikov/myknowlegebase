---
description: Тестирвоание пользовательского пути в браузере с помощью python библиотеки selenium
tags: crawlers tests
title: Selenium
---
Используется для [[тестирование]] пользовательского пути в браузере

Лучшие приемы:

- применять явные ожидания вместо неявных
- избегать дублирования тестирующего кода - писать вспомогательные методы в базовом классе либо
- избегать функциональности двойного тестирования - если есть тест, котоырй охватывает, к примеру вход в систему, необходимо постараться пропустить его в последующих тестах
- использовать [[разработка-на-основе-поведения(BDD)]]

Смотри еще:

- [[crawlers]]
- [[scrapy]]
- [[splash]]
- [[playwright]]
- [[2021-12-26-daily-note]] парсинг csv, html, работа с pandas
- [[2022-01-04-daily-note]] использование proxy
- [[2022-02-04-daily-note]] про вебдрайверы
- [[тестирование]]
- [pytest-selenium](https://pytest-selenium.readthedocs.io/en/latest/index.html)
- [selenium-ide](https://www.selenium.dev/selenium-ide/)

[//begin]: # "Autogenerated link references for markdown compatibility"
[тестирование]: ../lists/%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5 "Основные принципы тестровния"
[разработка-на-основе-поведения(BDD)]: %D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%BD%D0%B0-%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%B5-%D0%BF%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F(BDD) "Разработка на оснвое поведения (BDD)"
[crawlers]: ../lists/crawlers "Crawlers"
[scrapy]: scrapy "Scrapy"
[splash]: splash "Splash"
[playwright]: playwright "Playwright"
[2021-12-26-daily-note]: ../posts/2021-12-26-daily-note "Немного трюков с python - работа с csv, парсинг html и другое"
[2022-01-04-daily-note]: ../posts/2022-01-04-daily-note "Proxy в selenium, запуск локального smtp и несколько вопросов про pandas"
[2022-02-04-daily-note]: ../posts/2022-02-04-daily-note "Работа в selenium с firefox"
[//end]: # "Autogenerated link references"