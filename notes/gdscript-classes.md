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
  - [Container](https://docs.godotengine.org/en/stable/classes/class_container.html) базовая нода для контейнеров
  - CPUParticles2D - 2D частицы с обработкой процессором
  - CPUParticles3D
  - CSGBox3D бокс для использования CSG системы
  - CSGCombiner3D, CSGCylinder3D, CSGMesh3D, CSGPolygon3D, CSGPrimitive3D, CSGShape3D, CSGTorus3D
  - [DampedSpringJoint2D](https://docs.godotengine.org/en/stable/classes/class_dampedspringjoint2d.html) Демпфированная пружинная зависимость для 2D-физики. Это напоминает пружинное соединение, которое всегда хочет вернуться к заданной длине.
  - [Decal](https://docs.godotengine.org/en/stable/classes/class_decal.html) Декали используются для проецирования текстуры на меш в сцене. Используйте декали, чтобы добавить детали к сцене, не затрагивая базовую сетку. Они часто используются, чтобы добавить атмосферных воздействий зданию, добавить грязь или следы или разнообразить реквизит. Декали можно перемещать в любое время, что делает их подходящими для таких вещей, как тени от капель или точки лазерного прицела.
  - [DirectionalLight2D](https://docs.godotengine.org/en/stable/classes/class_directionallight2d.html) Направленный свет — это тип узла Light2D, который моделирует бесконечное количество параллельных лучей, покрывающих всю сцену. Он используется для источников света с высокой интенсивностью, расположенных далеко от сцены (например, для моделирования солнечного или лунного света).
  - DirectionalLight3D
  - EditorCommandPalette, EditorFileDialog, EditorFileSystem, EditorInspector, EditorInterface, EditorPlugin, EditorProperty, EditorResourcePicker, EditorResourcePreview, EditorSpinSliderEditorScriptPicker
  - FileDialog — это предустановленный диалог, используемый для выбора файлов и каталогов в файловой системе.
  - FileSystemDock
  - FlowContainer базовый класс для потоковых контейнеров
  - [FogVolume](https://docs.godotengine.org/en/stable/classes/class_fogvolume.html) используются для добавления локализованного тумана в глобальный объемный эффект тумана. FogVolumes также может удалять объемный туман из определенных областей при использовании FogMaterial с отрицательным значением FogMaterial.density.
  - Generic6DOFJoint3D, GeometryInstance3D
  - [GPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html) 2D частицы с процессингом на гпу
  - GPUParticles3D, GPUParticlesAttractor3D, GPUParticlesAttractorBox3D, GPUParticlesAttractorSphere3D, GPUParticlesAttractorVectorField3D, GPUParticlesCollision3D, GPUParticlesCollisionHeightField3D, GPUParticlesCollisionSDF3D, GPUParticlesCollisionSphere3D
  - [GraphEdit¶](https://docs.godotengine.org/en/stable/classes/class_graphedit.html) — это элемент управления, отвечающий за отображение графоподобных данных и управление ими с помощью GraphNodes. Предоставляет доступ к созданию, удалению, подключению и отключению узлов.
  - [GraphNode](https://docs.godotengine.org/en/stable/classes/class_graphnode.html) — это элемент управления Container, представляющий один блок данных в графе GraphEdit. Вы можете настроить количество, тип и цвет портов подключения слева и справа. GraphNode позволяет создавать узлы для графа GraphEdit с настраиваемым содержимым на основе его дочерних элементов управления. GraphNode является контейнером и отвечает за размещение своих дочерних элементов на экране. Это работает аналогично VBoxContainer. Дети, в свою очередь, предоставляют GraphNode так называемые слоты, каждый из которых может иметь порт подключения с любой стороны. Это похоже на то, как TabContainer использует дочерние элементы для создания вкладок.
  - [GridContainer](https://docs.godotengine.org/en/stable/classes/class_gridcontainer.html) используется для размещения дочерних элементов, производных от Control, настеке
  - GridMap Узел для 3D-карт на основе тайлов
  - [GrooveJoint2D](https://docs.godotengine.org/en/stable/classes/class_groovejoint2d.html) Ограничение канавы для 2D-физики. Это полезно для того, чтобы заставить тело «двигаться» через сегмент, помещенный в другой сегмент.
  - HBoxContainer, HFlowContainer, HingeJoint3D, HScrollBar, HSeparator, HSlider, HSplitContainer горизонтальные контейнеры
  - [HTTPRequest](https://docs.godotengine.org/en/stable/classes/class_httprequest.html) нода из которой можно делать http-запросы
  - ImporterMeshInstance3D
  - InstancePlaceholder Это полезно, чтобы избежать одновременной загрузки больших сцен путем выборочной загрузки их частей.
  - [ItemList](https://docs.godotengine.org/en/stable/classes/class_itemlist.html) Элемент управления, предоставляющий список доступных для выбора элементов (и/или значков) в одном столбце или, при необходимости, в нескольких столбцах.
  - [Joint2D](https://docs.godotengine.org/en/stable/classes/class_joint2d.html) Базовый узел для всех совместных ограничений в 2D-физике.
  - Joint3D
  - [Label](https://docs.godotengine.org/en/stable/classes/class_label.html) отображает обычный текст в строке или в прямоугольнике. Для форматированного текста используйте RichTextLabel.
  - Label3D
  - [Light2D](https://docs.godotengine.org/en/stable/classes/class_light2d.html) Излучает свет в 2D-среде. Свет определяется как цвет, значение энергии, режим (см. константы) и различные другие параметры (связанные с диапазоном и тенями).
  - Light3D
  - LightmapGI Вычисляет и сохраняет карты освещения для быстрого глобального освещения.
  - LightmapProbe Представляет один размещенный вручную источник для динамического освещения объекта с помощью LightmapGI.
  - [LightOccluder2D](https://docs.godotengine.org/en/stable/classes/class_lightoccluder2d.html) Перекрывает свет, отбрасываемый Light2D, отбрасывая тени
  - [Line2D](https://docs.godotengine.org/en/stable/classes/class_line2d.html)
  - [LineEdit](https://docs.godotengine.org/en/stable/classes/class_lineedit.html) Элемент управления, обеспечивающий редактирование строки.
  - [LinkButton](https://docs.godotengine.org/en/stable/classes/class_linkbutton.html) Простая кнопка, используемая для представления ссылки на какой-либо ресурс.
  - [MarginContainer](https://docs.godotengine.org/en/stable/classes/class_margincontainer.html) Добавляет верхнее, левое, нижнее и правое поле ко всем узлам управления, которые являются прямыми дочерними элементами контейнера.
  - Marker2D подсказка положения для редактирования. Это как обычный Node2D, но он всегда отображается в виде креста в 2D-редакторе. Вы можете установить визуальный размер креста, используя гизмо в 2D-редакторе, пока узел выбран.
  - Marker3D
  - MenuBar, MenuButton
  - [MeshInstance2D](https://docs.godotengine.org/en/stable/classes/class_meshinstance2d.html) Узел, используемый для отображения Mesh в 2D. Mesh — это тип ресурса, который содержит геометрию на основе массива вершин, разделенную на поверхности. Каждая поверхность содержит полностью отдельный массив и материал, используемый для его рисования. С точки зрения дизайна сетка с несколькими поверхностями предпочтительнее одной поверхности, потому что объекты, созданные в программном обеспечении для 3D-редактирования, обычно содержат несколько материалов.
  - MeshInstance3D
  - MissingNode Это класс внутреннего редактора, предназначенный для хранения данных узлов неизвестного типа.
  - MultiMeshInstance2D, MultiMeshInstance3D
  - MultiplayerSpawner, MultiplayerSynchronizer
  - [NavigationAgent2D](https://docs.godotengine.org/en/stable/classes/class_navigationagent2d.html) 2D-агент, который используется в навигации для достижения позиции, избегая статических и динамических препятствий. Динамические препятствия обходятся с помощью предотвращения столкновений RVO. Агенту нужны навигационные данные для правильной работы. NavigationAgent2D безопасен для физики
  - NavigationAgent3D
  - [NavigationLink2D](https://docs.godotengine.org/en/stable/classes/class_navigationlink2d.html) Создает связь между двумя позициями, через которые NavigationServer2D может направлять агентов. Ссылки можно использовать для выражения методов навигации, которые небанально перемещаются по поверхности навигационной сетки, например, зиплайны, телепорты или прыжки через промежутки.
  - NavigationLink3D
  - [NavigationObstacle2D](https://docs.godotengine.org/en/stable/classes/class_navigationobstacle2d.html) 2D-препятствие, используемое в навигации для предотвращения столкновений. Препятствию нужны навигационные данные для правильной работы. NavigationObstacle2D безопасен с точки зрения физики.
  - NavigationObstacle3D
  - [NavigationRegion2D](https://docs.godotengine.org/en/stable/classes/class_navigationregion2d.html) Регион навигационной карты. Он сообщает NavigationServer2D, что можно перемещать, а что нельзя, на основе его ресурса NavigationPolygon.
  - NavigationRegion3D
  - [NinePatchRect](https://docs.godotengine.org/en/stable/classes/class_ninepatchrect.html) Масштабируемая рамка на основе текстуры, которая заполняет центр и стороны текстуры, но сохраняет исходный размер углов. Идеально подходит для панелей и диалоговых окон.
  - [Node2D](https://docs.godotengine.org/en/stable/classes/class_node2d.html) Объект 2D-игры, наследуемый всеми узлами, связанными с 2D. Имеет позицию, вращение, масштаб и Z-индекс. Двухмерный игровой объект с трансформацией (положением, вращением и масштабом). Все 2D-узлы, включая физические объекты и спрайты, наследуются от Node2D. Используйте Node2D в качестве родительского узла для перемещения, масштабирования и поворота дочерних узлов в 2D-проекте. Также дает контроль над порядком рендеринга узла.
  - Node3D
  - OccluderInstance3D
  - OmniLight3D
  - OpenXRHand Узел, поддерживающий отслеживание пальцев в OpenXR
  - [OptionButton](https://docs.godotengine.org/en/stable/classes/class_optionbutton.html) Кнопочное управление, которое обеспечивает выбор параметров при нажатии
  - [Panel](https://docs.godotengine.org/en/stable/classes/class_panel.html) Обеспечивает непрозрачный фон для дочерних элементов управления.
  - PanelContainer
  - ParallaxBackground Узел, используемый для создания фона прокрутки параллакса.
  - ParallaxLayer
  - [Path2D](https://docs.godotengine.org/en/stable/classes/class_path2d.html) Содержит путь Curve2D для узлов PathFollow2D.
  - Path3D
  - [PathFollow2D](https://docs.godotengine.org/en/stable/classes/class_pathfollow2d.html) Этот узел берет свой родительский Path2D и возвращает координаты точки внутри него, учитывая расстояние от первой вершины. Это полезно для того, чтобы заставить другие узлы следовать по пути без кодирования шаблона движения. Для этого узлы должны быть потомками этого узла. Затем узлы-потомки будут перемещаться соответствующим образом при настройке хода выполнения в этом узле.
  - PathFollow3D
  - [PhysicalBone2D](https://docs.godotengine.org/en/stable/classes/class_physicalbone2d.html) Узел PhysicalBone2D — это узел на основе RigidBody2D, который можно использовать для того, чтобы узлы Bone2D в Skeleton2D реагировали на физику. Этот узел очень похож на узел PhysicalBone3D, только для 2D вместо 3D.
  - PhysicalBone3D
  - [PhysicsBody2D](https://docs.godotengine.org/en/stable/classes/class_physicsbody2d.html) Базовый класс для всех объектов, затронутых физикой в ​​2D-пространстве.
  - PhysicsBody3D
  - [PinJoint2D](https://docs.godotengine.org/en/stable/classes/class_pinjoint2d.html) Шарнирное соединение для 2D твердых тел. Он соединяет два тела (динамические или статические) вместе.
  - PinJoint3D
  - [PointLight2D](https://docs.godotengine.org/en/stable/classes/class_pointlight2d.html) позиционный 2D свет
  - [Polygon2D](https://docs.godotengine.org/en/stable/classes/class_polygon2d.html) двухмерный полигон. Polygon2D определяется набором точек. Каждая точка соединяется со следующей, а последняя точка соединяется с первой, в результате чего получается замкнутый многоугольник. Polygon2D могут быть заполнены цветом (сплошным или градиентным) или заполнены заданной текстурой.
  - [Popup](https://docs.godotengine.org/en/stable/classes/class_popup.html), [PopupMenu](https://docs.godotengine.org/en/stable/classes/class_popupmenu.html), [PopupPanel](https://docs.godotengine.org/en/stable/classes/class_popuppanel.html)
  - [ProgressBar](https://docs.godotengine.org/en/stable/classes/class_progressbar.html)
  - Range Абстрактный базовый класс для элементов управления на основе диапазона.
  - [RayCast2D](https://docs.godotengine.org/en/stable/classes/class_raycast2d.html) представляет собой линию от начала до места назначения, target_position. Он используется для запроса 2D-пространства, чтобы найти ближайший объект на пути луча.
  - RayCast3D
  - [ReferenceRect](https://docs.godotengine.org/en/stable/classes/class_referencerect.html) Рамка отсчета для графического интерфейса.
  - [ReflectionProbe](https://docs.godotengine.org/en/stable/classes/class_reflectionprobe.html) Захватывает свое окружение, чтобы создать быстрые и точные отражения от заданной точки.
  - [RemoteTransform2D](https://docs.godotengine.org/en/stable/classes/class_remotetransform2d.html) отправляет свой собственный Transform2D на другой производный узел Node2D в сцене.
  - RemoteTransform3D
  - [ResourcePreloader](https://docs.godotengine.org/en/stable/classes/class_resourcepreloader.html) Предварительно загружает список ресурсов внутри сцены. Этот узел используется для предварительной загрузки подресурсов внутри сцены, поэтому, когда сцена загружается, все ресурсы готовы к использованию и могут быть получены из загрузчика. Вы можете добавить ресурсы, используя вкладку ResourcePreloader, когда узел выбран.
  - [RichTextLabel](https://docs.godotengine.org/en/stable/classes/class_richtextlabel.html) Форматированный текст может содержать пользовательский текст, шрифты, изображения и некоторое базовое форматирование. Label управляет ими как внутренним стеком тегов. Он также адаптируется к заданной ширине/высоте.
  - [RigidBody2D](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html) Физическое тело, которое перемещается с помощью 2D-моделирования физики. Полезно для объектов, которые имеют гравитацию и могут толкаться другими объектами.
  - RigidBody3D
  - RootMotionView хелпер для редактора
  - ScriptCreateDialog попап для создания нового скрипта в редакторе
  - ScriptEditor, ScriptEditorBase
  - ScrollBar
  - ScrollContainer
  - Separator
  - [ShapeCast2D](https://docs.godotengine.org/en/stable/classes/class_shapecast2d.html) Приведение формы позволяет обнаруживать объекты столкновения, перемещая форму вдоль направления до цели, определяемого target_position (полезно для таких вещей, как лучевое оружие).
  - ShapeCast3D
  - [Skeleton2D](https://docs.godotengine.org/en/stable/classes/class_skeleton2d.html) для 2D-персонажей и анимированных объектов, является родителем иерархии объектов Bone2D. Это требование Bone2D. Skeleton2D содержит ссылку на позу покоя своих дочерних элементов и действует как единая точка доступа к своим bons.
  - Skeleton3D
  - SkeletonIK3D
  - Slider базовый класс для GUI слайдера
  - SliderJoint3D
  - SoftBody3D
  - [SpinBox](https://docs.godotengine.org/en/stable/classes/class_spinbox.html) Текстовое поле числового ввода.
  - [SplitContainer](https://docs.godotengine.org/en/stable/classes/class_splitcontainer.html) Контейнер для разделения двух элементов управления по вертикали или горизонтали с захватом, который позволяет регулировать смещение или соотношение разделения.
  - SpotLight3D
  - SpringArm3D
  - [Sprite2D](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html) Узел, отображающий 2D-текстуру. Отображаемая текстура может быть областью из более крупной текстуры атласа или кадром из анимации листа спрайтов.
  - Sprite3D, SpriteBase3D
  - [StaticBody2D](https://docs.godotengine.org/en/stable/classes/class_staticbody2d.html) — это простое тело, которое не движется при моделировании физики, т. е. оно не может быть перемещено внешними силами или контактами, но его преобразование все еще может быть обновлено пользователем вручную. Он идеально подходит для реализации объектов в окружающей среде, таких как стены или платформы. В отличие от RigidBody2D, он не потребляет никаких ресурсов процессора, пока они не перемещаются.
  - StaticBody3D
  - SubViewport Создает подвид на экране
  - SubViewportContainer
  - TabBar Панель управления вкладками
  - TabContainer
  - TextEdit Управление редактированием многострочного текста.
  - TextureButton кнопка на основе текстуры. Поддерживает состояния Pressed, Hover, Disabled и Focused.
  - TextureProgressBar
  - TextureRect
  - [TileMap](https://docs.godotengine.org/en/stable/classes/class_tilemap.html) Узел для двухмерных тайловых карт. Tilemaps используют TileSet, который содержит список плиток, которые используются для создания карт на основе сетки. TileMap может иметь несколько слоев, размещающих плитки друг над другом.
  - [Timer](https://docs.godotengine.org/en/stable/classes/class_timer.html) Таймер обратного отсчета
  - [TouchScreenButton](https://docs.godotengine.org/en/stable/classes/class_touchscreenbutton.html) Кнопка для устройств с сенсорным экраном для использования в игре.
  - [Tree](https://docs.godotengine.org/en/stable/classes/class_tree.html) Это показывает дерево элементов, которые можно выбрать, развернуть и свернуть. Дерево может иметь несколько столбцов с пользовательскими элементами управления, такими как редактирование текста, кнопки и всплывающие окна. Это может быть полезно для структурированных дисплеев и взаимодействий.
  - VBoxContainer горизонтальный бокс-контейнер
  - VehicleBody3D Физическое тело, имитирующее поведение автомобиля
  - VehicleWheel3D
  - VFlowContainer вертикальный контейнер потока
  - VideoStreamPlayer Управление воспроизведением видеопотоков.
  - Viewport базовый класс для отображения экранов
  - [VisibleOnScreenEnabler2D](https://docs.godotengine.org/en/stable/classes/class_visibleonscreenenabler2d.html) Автоматически отключает другой узел, если он не отображается на экране.
  - VisibleOnScreenEnabler3D
  - [VisibleOnScreenNotifier2D](https://docs.godotengine.org/en/stable/classes/class_visibleonscreennotifier2d.html) Определяет, когда экстенты узла видны на экране.
  - VisibleOnScreenNotifier3D
  - VisualInstance3D
  - [VoxelGI](https://docs.godotengine.org/en/stable/classes/class_voxelgi.html) используются для предоставления высококачественного непрямого света и отражений в сценах в реальном времени. Он предварительно вычисляет эффект объектов, излучающих свет, и эффект статической геометрии для имитации поведения сложного света в реальном времени. VoxelGI необходимо сериализовать, прежде чем появится видимый эффект. Однако после сериализации динамические объекты будут получать от них свет. Кроме того, источники света могут быть полностью динамическими или сериализованными.
  - VScrollBar вертикальный скролбар
  - VSeparator, VSlider, VSplitContainer
  - Window Узел, создающий окно. Окно может быть либо собственным системным окном, либо встроенным в другое окно.
  - [WorldEnvironment](https://docs.godotengine.org/en/stable/classes/class_worldenvironment.html) Свойства среды по умолчанию для всей сцены (эффекты постобработки, настройки освещения и фона).
  - XRAnchor3D, XRCamera3D, XRController3D, XRNode3D, XROrigin3D
- [Resources](https://docs.godotengine.org/en/stable/classes/index.html#resources)
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


[gdscript-classes]: gdscript-classes "GDScript classes"
[godot]: godot "godot engine"
[gamedev]: ../lists/gamedev "Gamedev"
