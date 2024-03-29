---
description: Разработка на основе тестирования (BDD)
tags: tests programming
title: Разработка на оснвое поведения (BDD)
---
Это подход к тестированию приложения путем тестирования поведения, которое приложение будет демонстрировать пользователю.

В настоящее время в практике BDD устоялась следующая структура:

- Заголовок. В сослагательной форме должно быть дано описание бизнес-цели.
- Описание. В краткой и свободной форме должны быть раскрыты следующие вопросы:
  - Кто является заинтересованным лицом данной истории;
  - Что входит в состав данной истории;
  - Какую ценность данная история предоставляет для бизнеса.
- Сценарии. В одной спецификации может быть один и более сценариев, каждый из которых раскрывает одну из ситуаций поведения пользователя, тем самым конкретизируя описание спецификации. Каждый сценарий обычно строится по одной и той же схеме:
  - Начальные условия (одно или несколько);
  - Событие, которое инициирует начало этого сценария;
  - Ожидаемый результат или результаты.

Преимущества: поощряет структурированный, многоразовый тестовый код (разделение на  человекочетаемый файл [[gherkin]] и программную реализацию)

Недостаток: синтаксис объектного языка накладывает некоторые ограничения на лексику, что может помещать реализовать нюансы тестируемого поведения пользователя.

[Статья вики](https://ru.wikipedia.org/wiki/BDD_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5))

Один из инструментов для #BDD - это [[gherkin]] (корнишон). Обертка над языком в python: [[behave]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[gherkin]: gherkin "Gherkin"
[behave]: behave "Behave"
[//end]: # "Autogenerated link references"