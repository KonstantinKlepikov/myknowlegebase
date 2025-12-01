---
title: Game on Rust — обзор фреймворков и библиотек для разработки игр на Rust
description: Краткий обзор популярных движков, библиотек и утилит для разработки игр на Rust на основе репозитория dasifefe/rust-game-development-frameworks
tags: rust gamedev engines wgpu
---

Этот обзор основан на подборке `rust-game-development-frameworks` и обобщает основные направления, зрелые проекты и утилиты, полезные при создании игр на [[rust]]. Статья написана с помощью gpt-5 mini.

Rust выдвигается как конкурентная платформа для разработки игр: безопасность памяти, высокая производительность и сильная экосистема для работы с графикой (wgpu), параллелизмом и сетями. Сообщество поддерживает множество движков и специализированных библиотек — от «легковесных» 2D‑фреймворков до полноценной 3D‑стека и инструментов для physics, аудио и UI.

## Основные категории и заметные проекты

### Полноценные игровые движки (2D + 3D)

- [Bevy](https://bevy.org/) — современный data‑driven игровой движок на Rust, основанный на ECS; быстро развивается и имеет активное сообщество.
- [Ambient](https://docs.rs/ambient_api/latest/ambient_api/) — runtime для высокопроизводительных мультплеерных игр и 3D‑приложений, ориентирован на WebAssembly и WebGPU.
- [Fyrox](https://docs.rs/fyrox/latest/fyrox/) (бывший rg3d) — feature‑rich движок с редактором сцен, подходящий для 3D‑проектов.
- [Hotham](https://docs.rs/hotham/latest/hotham/) — легковесный движок с прицелом на VR/стенд‑алоне.

### 2D‑фреймворки (простые и быстрые стартовые наборы)

- [Macroquad](https://docs.rs/macroquad/latest/macroquad/) — лёгкий мультиплатформенный фреймворк, прост в использовании, похож на или вдохновлённый raylib/miniquad.
- [ggez](https://docs.rs/ggez/latest/ggez/) — удобный для прототипов 2D игр (интерфейс, похожий на Love2D из мира Lua).
- [Tetra](https://docs.rs/tetra/latest/tetra/) — небольшой, прост в освоении 2D‑фреймворк.
- [Emerald](https://docs.rs/emerald/latest/emerald/), [Nova](https://github.com/17cupsofcoffee/nova), [Oxygengine](https://docs.rs/oxygengine/latest/oxygengine/) — другие варианты 2D‑ориентированных фреймворков.

### Графические библиотеки и рендер‑бэкенды

- [wgpu](https://docs.rs/wgpu/latest/wgpu/) — современный кроссплатформенный рендер‑бэкенд (Vulkan/Metal/D3D/GL/WebGPU). Базовая инфраструктура для многих проектов.
- [rend3](https://docs.rs/rend3/latest/rend3/), [rafx](https://docs.rs/rafx/latest/rafx/) — более высокоуровневые рендер‑решения поверх wgpu.
- [ash](https://docs.rs/ash/latest/ash/) — низкоуровневая обёртка Vulkan
- [glow](https://docs.rs/glow/latest/glow/) - низкоуровневая обёртка над OpenGL/WebGL
- [vulkano](https://docs.rs/vulkano/latest/vulkano/), [erupt](https://github.com/dasifefe/rust-game-development-frameworks) — низкоуровневая обёртка Vulkan
- [lyon](https://docs.rs/lyon/latest/lyon/), [miniquad](https://docs.rs/miniquad/latest/miniquad/) — 2D‑рендеринг/векторная графика и переносимость.
- [luminance](https://docs.rs/luminance/latest/luminance/) - высокоуровневая реализация поверх OpenGL
- [golem](https://docs.rs/golem/latest/golem/) - высокоуровневая обертка на основе подсветки
- [gl46](https://docs.rs/gl46) — низкоуровневая обёртка для OpenGL 4.6 (сгенерирована Phosphorus).
- [gl33](https://docs.rs/gl33) — низкоуровневая обёртка для OpenGL 3.3 (сгенерирована Phosphorus).
- [screen-13](https://docs.rs/screen-13) — простой Vulkan‑рендерер в духе QBasic.
- [sierra](https://docs.rs/sierra) — низкоуровневый контроль и высокоуровневые возможности; построен поверх `erupt`.

## Window creation and OS integration

- [winit](https://docs.rs/winit) — фреймворк для создания окон и обработки событий; де‑факто стандарт в сообществе Rust.
- [glfw](https://docs.rs/glfw) — обёртка на Rust для C‑библиотеки GLFW3.
- [fermium](https://docs.rs/fermium) — обёртка на Rust для SDL2; предоставляет больше, чем просто создание окон.
- [sdl2](https://docs.rs/sdl2) — обёртка на Rust для SDL2 с расширенным функционалом.

## Frameworks for generational-arena (containers for entities and other objects)

- [thunderdome](https://docs.rs/thunderdome) — генерационная арена, вдохновлённая generational‑arena, slotmap и slab; обеспечивает вставку, поиск и удаление за константное время с помощью небольших ключей `Arena`.
- [slotmap](https://docs.rs/slotmap) Container with persistent unique keys to access stored values.
- [generational-arena](https://docs.rs/generational-arena) A safe arena allocator that allows deletion without suffering from the [ABA problem](https://en.wikipedia.org/wiki/ABA_problem) by using generational indices.

## Frameworks for ECS (containers for entities and other objects)

- [hecs](https://docs.rs/hecs) — реализация ECS на основе архетипов (archetype).
- [yaks](https://docs.rs/yaks) — добавляет многопоточность к `hecs`.
- [legion](https://docs.rs/legion) — ECS на основе архетипов.
- [shipyard](https://docs.rs/shipyard) — реализация ECS на основе sparse‑структур.
- [specs](https://docs.rs/specs) — ECS, использующая битовые множества (bitset).

See [this repository](https://github.com/SanderMertens/ecs-faq#what-are-the-different-ways-to-implement-an-ecs) for information on the different types of ECS (archetype, sparse, bitset).

## Frameworks for physics and linear math (for 2D and 3D programming)

- [glam](https://docs.rs/glam)
- [rapier2d](https://docs.rs/rapier2d) / [rapier3d](https://docs.rs/rapier3d) — современный физический движок для 2D/3D от автора `nphysics`; есть демонстрации для 2D и 3D ([2D demo](https://rapier.rs/demos2d/index.html), [3D demo](https://rapier.rs/demos3d/index.html)).
- [cgmath](https://docs.rs/cgmath)
- [nalgebra](https://docs.rs/nalgebra)
- [ultraviolet](https://docs.rs/ultraviolet)
- [vek](https://docs.rs/vek)

## Graphical user interface (GUI)

- [yakui](https://github.com/LPGhatguy/yakui) — сочетает модель компоновки, вдохновлённую Flutter, с простотой immediate‑mode UI (Dear ImGui / egui).
- [egui](https://docs.rs/egui/) — кроссплатформенная GUI‑библиотека на Rust; многие рендереры имеют интеграцию с `egui`.
- [iced](https://docs.rs/iced/) — декларативная кроссплатформенная GUI‑библиотека на Rust.
- [imgui](https://docs.rs/imgui/) — биндинги Dear ImGui (C++) для Rust.


## Font (parser and/or rasterizer)

- [fontdue](https://docs.rs/fontdue)
- [swash](https://github.com/dfrg/swash)
- [rustybuzz](https://docs.rs/rustybuzz) — полная реализация алгоритма шейпинга HarfBuzz, портированная на Rust.
- [ttf-parser](https://docs.rs/ttf-parser) — высокоуровневый, безопасный парсер TrueType шрифтов без выделения памяти (zero-allocation).

## Space partitioning

- [rstar](https://docs.rs/crate/rstar/) — N‑мерная реализация [r*-tree](https://en.wikipedia.org/wiki/R*_tree) для пространственного индексирования.
- [bvh](https://docs.rs/crate/bvh/) — иерархия ограничивающих объёмов (Bounding Volume Hierarchy), реализована поверх [nalgebra](https://www.nalgebra.org/).
- [kdtree](https://docs.rs/crate/kdtree/) — k‑мерное дерево для быстрого геопространственного индексирования и поиска ближайших соседей.
- [ncollide 2D](https://docs.rs/crate/ncollide2d/) — реализация Bounding Volume Tree для 2D. [(2d documentation)](https://www.ncollide.org/rustdoc/ncollide2d/partitioning/struct.BVT.html).
- [ncollide 3D](https://docs.rs/crate/ncollide3d/) — реализация Bounding Volume Tree для 3D. [(3d documentation)](https://www.ncollide.org/rustdoc/ncollide3d/partitioning/struct.BVT.html).
- [spade](https://docs.rs/crate/spade/) — реализует [r*-tree](https://en.wikipedia.org/wiki/R*_tree) и триангуляцию Делоне. [delaunay triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation).
- [flat_spatial](https://docs.rs/crate/flat_spatial/) — простые плоские структуры (например, сетка или хеш‑таблица ячеек) для быстрых запросов.
- [acacia](https://docs.rs/crate/acacia/) — обобщённая по размерности структура разделения пространства; поддерживает бинарные деревья, квадродерева, октодрева и т.д.

## Network

- [tokio](https://docs.rs/tokio) — асинхронный рантайм и набор утилит для работы с I/O; поддержка асинхронных TCP и UDP сокетов.
- [quinn](https://docs.rs/quinn) — реализация транспортного протокола QUIC на Rust; построен с учётом интеграции с `tokio`.

## Audio

- [oddio](https://docs.rs/oddio) — библиотека аудио, построенная на `cpal`.
- [kira](https://docs.rs/kira) — аудиобиблиотека поверх `cpal`.
- [rodio](https://docs.rs/rodio) — высокоуровневая аудиобиблиотека поверх `cpal`.
- [cpal](https://docs.rs/cpal) — низкоуровневая кроссплатформенная библиотека для ввода/вывода аудио.
- [alto](https://docs.rs/alto) — обёртка над OpenAL.
- [openal](https://docs.rs/openal) — биндинги/обёртка для OpenAL.

## Serialization-Deserialization

- [fjall](https://github.com/fjall-rs/fjall) — встроенная key‑value база данных, написанная на чистом Rust.
- [redb](https://docs.rs/redb) — встраиваемая key‑value база данных на Rust.
- [speedy](https://docs.rs/speedy) — быстрая и простая бинарная сериализация/десериализация.
- [serde](https://docs.rs/serde) — универсальная библиотека для сериализации и десериализации структур данных.
- [serde-json](https://crates.io/crates/serde_json) — реализация формата JSON для `serde`.
- [bincode](https://crates.io/crates/bincode) — компактный бинарный формат сериализации на основе `serde`.
- [borsh](https://docs.rs/borsh) — реализация бинарного формата Borsh, ориентированного на детерминированность, консистентность и безопасность.

## Other utilities

- [hexasphere](https://docs.rs/hexasphere) — делит 3D‑формы (икосаэдр, тетраэдр, квадрат, треугольник, куб) на треугольные сетки.
- [navmesh](https://docs.rs/navmesh/) — навигационная сетка (navmesh) для поиска пути.
- [density-mesh-core](https://docs.rs/density-mesh-core) / [density-mesh-image](https://docs.rs/density-mesh-image) — генерация 2D‑сетки из изображений, представляющих плотность/высотную карту.
- [image](https://docs.rs/image) — кодирование и декодирование изображений во множестве форматов.
- [rayon](https://docs.rs/rayon) — добавляет параллелизм в код и упрощает безопасное многопоточное выполнение без data‑race.
- [palette](https://docs.rs/palette) — операции и преобразования в цветовом пространстве, линейные цветовые вычисления.
- [pathfinding](https://docs.rs/pathfinding) — набор реализаций алгоритмов поиска пути.
- [salva2d](https://docs.rs/salva2d) / [salva3d](https://docs.rs/salva3d) — моделирование динамики жидкости на основе частиц.
- [collider](https://docs.rs/collider) — непрерывное обнаружение столкновений в 2D.

### Примеры открытых игр в [репозитории](https://github.com/dasifefe/rust-game-development-frameworks)

В подборке перечислены множество проектов‑примеров (RecWars, Veloren, RustCycles и др.), которые можно изучить как источник архитектурных идей и практических реализаций.

## Смотри еще

- [репозиторий со ссылками на фреймворки](https://github.com/dasifefe/rust-game-development-frameworks)
- [Learn WGPU](https://sotrh.github.io/learn-wgpu/)
- [Are We Game Yet?](https://arewegameyet.rs/)
- [[rust]]

[rust]: ../lists/rust "Ресурсы по языку программирования Rust"
