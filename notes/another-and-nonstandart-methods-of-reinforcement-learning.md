---
description: Другие и нестандартные методы обучения с подкреплением
tags: machine-learning r-learning
title: Another and nonstandart methods of reinforcemebt learning
---
## Алгоритмы вне политик (с раздельной стратегией)

Такие алгоритмы разделяют исследование и использование с помощью двух раздельных стратегий - целевой стратегии и стратегии поведения. В таких алгоритмах целевая стратегия не имеет возможность проверить свою оценку, однако это не мешает получить оценку для обеих политик. Целевая стратегия оптимизируется с использованием данных стратегии повдения, которая в свою очередь сосредоточена на поиске новых состояний.

Варианты реализации

- q-learning
- GTD градиентное обучение на основе [[temporal-difference]]
- жадные GQ-алгоритмы
- актор-критик вне политики (off-PAC)

## Детерменированные градиенты стратегий

Такие алгоритмы предполагают наличие одного конкретного действия для каждого состяония, что исключает необходимость использования выборки как в пространстве действий так и в пространстве состояний.

Вариации DPG:

- deep DPG (DDPG)
- дважды отложенные DPG (twin delayed deep deterministic policy gradients, TD3) реализует отложенное обновление стратегии, ограниченное двойное q-обучение и сглаживание целевой стратегии

## Методы доверительной области

Направлены на снижение зависимости градиентных методов от размера шага.

- trust region policy optimization (TRPO) испольует расхождение Кульбака-Лейбнера для оптимизации стратегии, позволяя ограничить размер шага в соответствии с изменениями в стратегии
- natural policy gradients (NPG) позволят количественно определить размер шага с точки зрения метрики, основаной на расстоянии между текущей стратегией и стратегией после обновления с помощью шага градиента
- методы штрафующие большие шаги (proximal policy optimization, PPO)

## Другие алгоритмы

- Retrace($$\lambda$$) алгоритм вне политики с трассировкой , котоырй использует взвешенную отсеченную выборку по значимости для контроля части стратегии, которая отвечает за обновление.
- ACER (actor-critic with expirience relay) дополняет Retrace($$\lambda$$) комбинацией вопсроизведения опыта, оптимизацией стратегии доверительной области и дуэльной архитектурой.
- ACKTR оптимизирует TRPO за счет аппроксимаций.

Смотри еще:

- [[reinforcement-learning]]
- [[temporal-difference]]
- [[policy-gradient-methods]]
- [[deep-q-learning]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[temporal-difference]: temporal-difference "Temporal difference methods and n-steps methods"
[reinforcement-learning]: ../lists/reinforcement-learning "Reinforcement learning"
[policy-gradient-methods]: policy-gradient-methods "Policy Gradient Methods"
[deep-q-learning]: deep-q-learning "Deep Q-learning"
[//end]: # "Autogenerated link references"