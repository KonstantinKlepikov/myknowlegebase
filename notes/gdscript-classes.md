---
description: Классы в godot
tags: gamedev
title: GDScript classes
---
[Смотри документацию тут](https://docs.godotengine.org/en/stable/classes/index.html)

- Globals
  - [@GDScript](https://docs.godotengine.org/en/stable/classes/class_%40gdscript.html) - встроенные функции GDScript. Доступны из любого скрипта.
  - [@GlobalScope](https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html) - константы и функции глобальной области видимости. Это все, что находится в глобальных переменных, константах, касающихся кодов ошибок, кодов клавиш, подсказок свойств и т. д. Здесь также задокументированы синглтоны, поскольку к ним можно получить доступ из любого места
- [Nodes](https://docs.godotengine.org/en/stable/classes/index.html#nodes)
  - [Node](https://docs.godotengine.org/en/stable/classes/class_node.html) базовый класс для объектов сцен

Ноды — это строительные блоки Godot. Их можно назначить дочерними элементами другой ноды, что приведет к древовидному расположению. Данная нода может содержать любое количество нод в качестве дочерних с требованием, чтобы все братья и сестры (прямые дочерние ноды ноды) имели уникальные имена.

Дерево нод называется сценой. Сцены можно сохранять на диск, а затем использовать в других сценах. Это обеспечивает очень высокую гибкость архитектуры и модели данных проектов Godot.

Дерево сцен: `SceneTree` содержит активное дерево нод. Когда нода добавляется в дерево сцены, она получает уведомление `NOTIFICATION_ENTER_TREE` и запускается его обратный вызов `_enter_tree`. Дочерние ноды всегда добавляются после их родительской ноды, т. е. обратный вызов _enter_tree родительского узла будет инициирован до его дочернего узла.

Как только все узлы добавлены в дерево сцены, они получают уведомление `NOTIFICATION_READY` и запускаются их соответствующие обратные вызовы `_ready`. Для групп узлов обратный вызов `_ready` вызывается в обратном порядке, начиная с дочерних узлов и двигаясь вверх к родительским узлам.

Это означает, что при добавлении узла в дерево сцены для обратных вызовов будет использоваться следующий порядок: `_enter_tree` родителя, `_enter_tree` дочерних элементов, `_ready` дочерних элементов и, наконец, `_ready` родительского элемента (рекурсивно для всего дерева сцены).

Processing: узлы могут переопределить состояние `processing`, чтобы получать обратный вызов для каждого кадра с запросом на обработку (что-то сделать). Обычная обработка (обратный вызов `_process`, переключаемая с помощью `set_process`) происходит максимально быстро и зависит от частоты кадров, поэтому дельта времени обработки (в секундах) передается в качестве аргумента. Обработка физики (обратный вызов `_physics_process`, переключаемая с помощью `set_physics_process`) происходит фиксированное количество раз в секунду (по умолчанию 60) и полезна для кода, связанного с физическим движком.

Узлы также могут обрабатывать входящие события. При наличии функция `_input` будет вызываться для каждого ввода, который получает программа. Во многих случаях это может быть излишним (если только не используется для простых проектов), и функция `_unhandled_input` может быть предпочтительнее; она вызывается, когда событие ввода не было обработано никем другим (как правило, узлами управления графическим интерфейсом), гарантируя, что узел получает только предназначенные для него события.

Чтобы отслеживать иерархию сцен (особенно при добавлении сцен в другие сцены), для узла можно установить «владельца» с помощью свойства `owner`. Это отслеживает, кто что создал. Однако это в основном полезно при написании редакторов и инструментов.

Наконец, когда узел освобождается с помощью `Object.free` или `queue_free`, он также освобождает всех своих потомков.

Groups: узлы могут быть добавлены в столько групп, сколько вам нужно, чтобы ими было легко управлять, например, вы можете создавать группы, такие как «враги» или «предметы коллекционирования», в зависимости от вашей игры. Затем вы можете получить все узлы в этих группах, перебрать их и даже вызвать методы в группах с помощью методов в `SceneTree`.

Networking with nodes: после подключения к серверу (или его создания) можно использовать встроенную систему RPC (удаленный вызов процедур) для связи по сети. При вызове rpc с именем метода он будет вызываться локально и во всех подключенных пирах (пиры = клиенты и сервер, который принимает соединения). Чтобы определить, какой узел получает вызов RPC, Godot будет использовать его NodePath (убедитесь, что имена узлов одинаковы на всех одноранговых узлах).

- ноды (продолжение)
  - [AcceptDialog](https://docs.godotengine.org/en/stable/classes/class_acceptdialog.html) базовый диалог для нотификации юзеров
  - [AnimatableBody2D](https://docs.godotengine.org/en/stable/classes/class_animatablebody2d.html) физическое тело для 2D-физики, которое движется только по сценарию или анимации. Полезно для перемещения платформ и дверей.
  - [AnimatableBody3D](https://docs.godotengine.org/en/stable/classes/class_animatablebody3d.html)
  - [AnimatedSprite2D](https://docs.godotengine.org/en/stable/classes/class_animatedsprite2d.html) Узел содержащий несколько текстур в виде кадров для воспроизведения анимации.
  - AnimatedSprite3D узел для анимации 2D-спрайтов в 3D
  - [AnimationPlayer](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html) ресурсы проигрывателя анимации. Проигрыватель анимации используется для общего воспроизведения ресурсов анимации. Он содержит словарь ресурсов AnimationLibrary и настраиваемое время наложения между переходами анимации.
  - [AnimationTree](https://docs.godotengine.org/en/stable/classes/class_animationtree.html) дополнительные возможности плеера
  - [Area2D](https://docs.godotengine.org/en/stable/classes/class_area2d.html) - двхумераня область для обнаружения, а так-же для применеения физики и звукового сопровождения
  - Area3D
  - [AspectRatioContainer](https://docs.godotengine.org/en/stable/classes/class_aspectratiocontainer.html) Контейнер, который сохраняет соотношение сторон своих дочерних элементов управления
  - AudioListener2D переопределяет местопложение слышимых звуков
  - AudioListener3D
  - AudioStreamPlayer непозиционный плеер
  - AudioStreamPlayer2D Воспроизведение спозиционированного звука в 2D-пространстве.
  - AudioStreamPlayer3D
  - BackBufferCopy Копирует область экрана (или весь экран) в буфер, чтобы к ней можно было получить доступ в сценариях шейдера с использованием текстуры экрана
  - [BaseButton](https://docs.godotengine.org/en/stable/classes/class_basebutton.html) базовый класс для кнопок
  - [Bone2D](https://docs.godotengine.org/en/stable/classes/class_bone2d.html) используется со Skeleton2D для управления и анимации других узлов. Используйте иерархию Bone2D, привязанную к Skeleton2D, для управления и анимации других узлов Node2D.
  - [BoneAttachment3D](https://docs.godotengine.org/en/stable/classes/class_boneattachment3d.html)
  - [BoxContainer](https://docs.godotengine.org/en/stable/classes/class_boxcontainer.html) базовый класс для бокс-контейнеров
  - [Button](https://docs.godotengine.org/en/stable/classes/class_button.html) стандартная кнопка. Кнопки (как и все узлы управления) также можно создавать в редакторе, но в некоторых ситуациях может потребоваться их создание из кода.
  - [Camera2D](https://docs.godotengine.org/en/stable/classes/class_camera2d.html) заставляет экран (текущий слой) прокручиваться вслед за этим узлом. Это упрощает (и ускоряет) программирование прокручиваемых сцен, чем ручное изменение положения узлов на основе CanvasItem.
  - [Camera3D](https://docs.godotengine.org/en/stable/classes/class_camera3d.html)
  - [CanvasGroup](https://docs.godotengine.org/en/stable/classes/class_canvasgroup.html) Объединяет несколько 2D-узлов в одну операцию рисования. Дочерние узлы CanvasItem CanvasGroup рисуются как один объект. Это позволяет, например. рисовать перекрывающиеся полупрозрачные 2D-узлы без смешивания
  - [CanvasItem](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html). Базовый класс для всего 2D. CanvasItem расширяется Control для всего, что связано с графическим интерфейсом, и Node2D для всего, что связано с движком 2D.
  - [CanvasLayer](https://docs.godotengine.org/en/stable/classes/class_canvaslayer.html) слой холста для рисования
  - [CanvasModulate](https://docs.godotengine.org/en/stable/classes/class_canvasmodulate.html) подкрашивает элементы всего холста, используя назначенный им цвет.
  - [CenterContainer](https://docs.godotengine.org/en/stable/classes/class_centercontainer.html) CenterContainer удерживает дочерние элементы управления по центру. Этот контейнер удерживает все дочерние элементы в их минимальном размере в центре.
  - [CharacterBody2D](https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html) Специализированный узел 2D-физического тела для персонажей, перемещаемых по сценарию. Тела персонажей — это особые типы тел, предназначенные для управления пользователем. На них никак не влияет физика; для других типов тел, таких как твердое тело, они аналогичны AnimatableBody2D.
  - CharacterBody3D
  - [CheckBox](https://docs.godotengine.org/en/stable/classes/class_checkbox.html)
  - [CheckButton](https://docs.godotengine.org/en/stable/classes/class_checkbutton.html)
  - CodeEdit Многострочный текстовый элемент управления, предназначенный для редактирования кода. Используется в самом редакторе.
  - [CollisionObject2D](https://docs.godotengine.org/en/stable/classes/class_collisionobject2d.html) базовый класс для 2D коллизий
  - CollisionObject3D
  - [CollisionPolygon2D](https://docs.godotengine.org/en/stable/classes/class_collisionpolygon2d.html) коллизии полигонов
  - CollisionPolygon3D
  - [CollisionShape2D](https://docs.godotengine.org/en/stable/classes/class_collisionshape2d.html) Узел, который представляет данные о форме столкновения в 2D-пространстве.Узел, который представляет данные о форме столкновения в 2D-пространстве. ВАЖНО: это помощник только для редактора для создания фигур, используйте `CollisionObject2D.shape_owner_get_shape`, чтобы получить реальную форму.
  - CollisionShape3D
  - [ColorPicker](https://docs.godotengine.org/en/stable/classes/class_colorpicker.html) управление палитрой
  - [ColorPickerButton](https://docs.godotengine.org/en/stable/classes/class_colorpickerbutton.html) кнопка вызова палитры
  - [ColorRect](https://docs.godotengine.org/en/stable/classes/class_colorrect.html) окрашенный прямоугольник
  - ConeTwistJoint3D Поворотное соединение между двумя 3D PhysicsBodies.
  - [ConfirmationDialog](https://docs.godotengine.org/en/stable/classes/class_confirmationdialog.html) Диалог подтверждения действий. Это диалоговое окно наследуется от AcceptDialog, но по умолчанию имеет кнопки «ОК» и «Отмена» (в порядке хост-операционки).
- Resources
- Other objects
- Variant types

Смотри еще:

- [Документация GDScript](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#doc-gdscript)
- [все классы в документации](https://docs.godotengine.org/en/stable/classes/index.html) [[gdscript-classes]] - кратко
- [gdscript.com](https://gdscript.com/) туториалы и решения
- [godot demo projects](https://github.com/godotengine/godot-demo-projects)
- [best practicies](https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html)
- [[godot]]
- [[gamedev]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[gdscript-classes]: gdscript-classes "GDScript classes"
[godot]: godot "godot engine"
[gamedev]: ../lists/gamedev "Gamedev"
[//end]: # "Autogenerated link references"