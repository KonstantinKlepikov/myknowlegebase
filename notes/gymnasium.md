---
description: Gymnasium библиотека для построения стред обучения с подкреплением на python
title: Gymnasium
tags: machine-learning r-learning
---
```python
import gymnasium as gym
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset(seed=42)
for _ in range(1000):
   action = env.action_space.sample()  # this is where you would insert your policy
   observation, reward, terminated, truncated, info = env.step(action)

   if terminated or truncated:
      observation, info = env.reset()
env.close()
```

## [Создание собственной среды](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)

Пример создания собственной среды можно зарать так:

```sh
git clone https://github.com/Farama-Foundation/gym-examples
cd gym-examples
python -m venv .env
source .env/bin/activate
pip install -e .
```

Структура проекта:

```sh
gym-examples/
  README.md
  setup.py
  gym_examples/
    __init__.py
    envs/
      __init__.py
      grid_world.py
    wrappers/
      __init__.py
      relative_position.py
      reacher_weighted_reward.py
      discrete_action.py
      clip_reward.py
```

Чтобы проиллюстрировать процесс создания подклассов [gymnasium.Env](https://gymnasium.farama.org/api/env/), мы реализуем очень простую игру под названием GridWorldEnv. Мы напишем код для нашей пользовательской среды в grid_world.py. Среда состоит из 2-мерной квадратной сетки фиксированного размера (задается параметром sizeпри построении). Агент может перемещаться вертикально или горизонтально между ячейками сетки на каждом временном шаге. Цель агента — перейти к цели на сетке, которая была случайно размещена в начале эпизода.

- Наблюдения обеспечивают местоположение цели и агента.
- В нашей среде есть 4 действия, соответствующие движениям «вправо», «вверх», «влево» и «вниз».
- Сигнал готовности выдается, как только агент перейдет к ячейке сетки, где находится цель.
- Вознаграждения являются бинарными и разреженными, что означает, что немедленное вознаграждение всегда равно нулю, если только агент не достиг цели, тогда оно равно 1.

Эпизод в этой среде (с size=5) может выглядеть так: где синяя точка — агент, а красный квадрат — цель.

### Инициализация

Наша пользовательская среда будет наследоваться от абстрактного класса `gymnasium.Env`. Не забудьте добавить `metadata` атрибут в свой класс. Там вы должны указать режимы рендеринга, поддерживаемые вашей средой (например  "human", "rgb_array", , "ansi") и частоту кадров, с которой должна отображаться ваша среда. Каждая среда должна поддерживать None в качестве режима рендеринга; вам не нужно добавлять его в метаданные. В GridWorldEnv, мы будем поддерживать режимы «rgb_array» и «human» и рендерить со скоростью 4 FPS.

Метод `__init__` нашей среды будет принимать целое число `size`, определяющее размер квадратной сетки. Мы настроим некоторые переменные для рендеринга и определим `self.observation_space` и `self.action_space`. В нашем случае наблюдения должны предоставлять информацию о местоположении агента и цели на двумерной сетке. Мы выберем представление наблюдений в виде словарей с ключами `agent` и `target.` Наблюдение может выглядеть так `{"agent": array([1, 0]), "target": array([0, 3])}`. Так как у нас есть 4 действия в нашей среде («вправо», «вверх», «влево», «вниз»), мы будем использовать в качестве действия пространство.

```python
import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces


class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=5):
        self.size = size  # The size of the square grid
        self.window_size = 512  # The size of the PyGame window

        # Observations are dictionaries with the agent's
        # and the target's location.
        # Each location is encoded as an element of
        # {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
```

### Наблюдения из состояния среды

Поскольку нам нужно будет вычислять наблюдения как в `reset` так и в `step`, часто удобно иметь метод `_get_obs`, который переносит состояние среды в наблюдения. Однако это не является обязательным, и вы также можете вычислять наблюдения в `reset` и `step` отдельно:

```python
def _get_obs(self):
    return {"agent": self._agent_location, "target": self._target_location}
```

Мы также можем реализовать аналогичный метод для вспомогательной информации, возвращаемой функциями `step` and `reset`. В нашем случае мы хотели бы указать манхэттенское расстояние между агентом и целью:

```python
def _get_info(self):
    return {
        "distance": np.linalg.norm(
            self._agent_location - self._target_location, ord=1
        )
    }
```

Часто информация также будет содержать некоторые данные, которые доступны только внутри `step` метода (например, отдельные условия вознаграждения). В этом случае нам пришлось бы обновлять словарь, возвращаемый `_get_info` in `step`.

### Сброс

Метод `reset` будет вызван для запуска нового эпизода. Вы можете полагаться на то, что `step` метод не будет вызываться до `reset`. Кроме того, `reset` должен вызываться всякий раз, когда был выдан сигнал готовности. Пользователи могут передать `seed` для `reset` инициализируя генератор случайных чисел, используемый средой, в детерминированное состояние. Рекомендуется использовать генератор случайных чисел `self.np_random`, предоставляемый базовым классом среды `gymnasium.Env`. Если вы используете только этот ГСЧ, вам не нужно сильно беспокоиться о сидах, но вам нужно не забыть вызвать `super().reset(seed=seed)`, чтобы убедиться, что `gymnasium.Env` правильно сидит генератор. Как только это будет сделано, мы можем случайным образом установить состояние нашей среды. В нашем случае мы случайным образом выбираем местоположение агента и случайную выборку целевых позиций до тех пор, пока она не совпадет с позицией агента.

Метод `reset` должен возвращать кортеж исходного наблюдения и некоторую вспомогательную информацию. Для этого мы можем использовать методы `_get_obs` и `_get_info`, которые мы реализовали ранее

```python
def reset(self, seed=None, options=None):
    # We need the following line to seed self.np_random
    super().reset(seed=seed)

    # Choose the agent's location uniformly at random
    self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

    # We will sample the target's location randomly until it
    # does not coincide with the agent's location
    self._target_location = self._agent_location
    while np.array_equal(self._target_location, self._agent_location):
        self._target_location = self.np_random.integers(
            0, self.size, size=2, dtype=int
        )

    observation = self._get_obs()
    info = self._get_info()

    if self.render_mode == "human":
        self._render_frame()

    return observation, info
```

### Шаг

Метод `step` обычно содержит большую часть логики вашей среды. Он принимает action, вычисляет состояние среды после применения этого действия и возвращает 4-tuple (observation, reward, done, info). Как только новое состояние среды будет вычислено, мы можем проверить, является ли оно конечным состоянием, и установить его соответствующим образом. Поскольку мы используем разреженные бинарные вознаграждения в GridWorldEnv, вычисления становятся тривиальными, как только мы получаем сигнал `done` (готовности). Чтобы собрать observation и info, мы снова можем использовать `get_obs` и `_get_info`.

```python
def step(self, action):
    # Map the action (element of {0,1,2,3}) to the direction we walk in
    direction = self._action_to_direction[action]
    # We use `np.clip` to make sure we don't leave the grid
    self._agent_location = np.clip(
        self._agent_location + direction, 0, self.size - 1
    )
    # An episode is done iff the agent has reached the target
    terminated = np.array_equal(self._agent_location, self._target_location)
    reward = 1 if terminated else 0  # Binary sparse rewards
    observation = self._get_obs()
    info = self._get_info()

    if self.render_mode == "human":
        self._render_frame()

    return observation, reward, terminated, False, info
```

### Рендеринг

Здесь мы используем PyGame для рендеринга. Подобный подход к рендерингу используется во многих средах, входящих в состав Gymnasium, и вы можете использовать его в качестве основы для своих собственных сред

```python
def render(self):
    if self.render_mode == "rgb_array":
        return self._render_frame()

def _render_frame(self):
    if self.window is None and self.render_mode == "human":
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode(
            (self.window_size, self.window_size)
        )
    if self.clock is None and self.render_mode == "human":
        self.clock = pygame.time.Clock()

    canvas = pygame.Surface((self.window_size, self.window_size))
    canvas.fill((255, 255, 255))
    pix_square_size = (
        self.window_size / self.size
    )  # The size of a single grid square in pixels

    # First we draw the target
    pygame.draw.rect(
        canvas,
        (255, 0, 0),
        pygame.Rect(
            pix_square_size * self._target_location,
            (pix_square_size, pix_square_size),
        ),
    )
    # Now we draw the agent
    pygame.draw.circle(
        canvas,
        (0, 0, 255),
        (self._agent_location + 0.5) * pix_square_size,
        pix_square_size / 3,
    )

    # Finally, add some gridlines
    for x in range(self.size + 1):
        pygame.draw.line(
            canvas,
            0,
            (0, pix_square_size * x),
            (self.window_size, pix_square_size * x),
            width=3,
        )
        pygame.draw.line(
            canvas,
            0,
            (pix_square_size * x, 0),
            (pix_square_size * x, self.window_size),
            width=3,
        )

    if self.render_mode == "human":
        # The following line copies our drawings from `canvas` to the visible window
        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        # We need to ensure that human-rendering occurs at the predefined framerate.
        # The following line will automatically add a delay to keep the framerate stable.
        self.clock.tick(self.metadata["render_fps"])
    else:  # rgb_array
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
        )
```

### Close

Метод `close` должен закрывать все открытые ресурсы, которые использовались средой. Во многих случаях вам не нужно беспокоиться о реализации этого метода. Однако в нашем примере `render_mode` может быть "human" и нам может понадобиться закрыть открытое окно:

```python
def close(self):
    if self.window is not None:
        pygame.display.quit()
        pygame.quit()
```

В других средах `close` также могут быть закрыты открытые файлы или освобождены другие ресурсы. Вы не должны взаимодействовать с окружением после вызова `close`.

### Регистрация кастомного окружения

Чтобы Gymnasium обнаружил пользовательские среды, они должны быть зарегистрированы. Мы решим поместить регистрирующий код в `gym_examples/__init__.py`.

```python
from gymnasium.envs.registration import register

register(
     id="gym_examples/GridWorld-v0",
     entry_point="gym_examples.envs:GridWorldEnv",
     max_episode_steps=300,
)
```

Идентификатор среды состоит из трех компонентов, два из которых являются необязательными: необязательное пространство имен (здесь: `gym_examples`), обязательное имя (здесь: `GridWorld)` и необязательная, но рекомендуемая версия (здесь: `v0`). Он также может быть зарегистрирован как `GridWorld-v0` (рекомендуемый подход) `GridWorld` или `gym_examples/GridWorld`, и затем при создании среды следует использовать соответствующий идентификатор.

Аргумент ключевого слова `max_episode_steps=300` гарантирует, что среды `GridWorld`, созданные с помощью, `gymnasium.make` будут заключены в `TimeLimit` оболочку. Затем будет выдан сигнал `done`, если агент достиг цели или в текущем эпизоде ​​было выполнено 300 шагов. Чтобы отличать усечение от остановки, вы можете проверять `info["TimeLimit.truncated"]`.

Помимо `id` и `entrypoint`, вы можете передать следующие дополнительные аргументы ключевого слова в `register`:

- `reward_threshold` (float) default `None` - Порог вознаграждения до того, как задача будет считаться решенной
- `nondeterministic` (bool) default `False` - Является ли эта среда недетерминированной даже после заполнения
- `max_episode_steps` (int) default `None` - Максимальное количество шагов, из которых может состоять эпизод. Если не `None`,добавляется обертка TimeLimit
- `order_enforce` (bool) default `True` - Обернуть ли среду в `OrderEnforcing` обертку
- `autoreset` (bool) default `False` - Обернуть ли среду в `AutoResetWrapper`
- kwargs (dict) default `{}` - Kwargs по умолчанию для передачи классу среды

Большинство этих ключевых слов (за исключением `max_episode_steps`, `order_enforce` и `kwargs`) не изменяют поведение экземпляров среды, а просто предоставляют некоторую дополнительную информацию о вашей среде. После регистрации наша пользовательская GridWorld Env среда может быть создана с `.env = gymnasium.make('gym_examples/GridWorld-v0')`

gym_examples/envs/__init__.py должен иметь:

```python
from gym_examples.envs.grid_world import GridWorldEnv
```

Если ваша среда не зарегистрирована, вы можете опционально передать модуль для импорта, который зарегистрирует вашу среду перед ее созданием следующим образом - `env = gymnasium.make('module:Env-v0')`. Для среды GridWorld код регистрации запускается путем импорта, поэтому, если было невозможно явно импортировать gym_examples, вы могли зарегистрироваться при создании с помощью `env = gymnasium.make('gym_examples:gym_examples/GridWorld-v0)`. Это особенно полезно, когда вам разрешено передавать только идентификатор среды в стороннюю кодовую базу (например, в обучающую библиотеку). Это позволяет вам зарегистрировать вашу среду без необходимости редактирования исходного кода сторонней библиотеки.

### Создани е пакета

```python
from setuptools import setup

setup(
    name="gym_examples",
    version="0.0.1",
    install_requires=["gymnasium==0.26.0", "pygame==2.1.0"],
)
```

`pip install -e gym-examples`

```python
import gym_examples
env = gymnasium.make('gym_examples/GridWorld-v0')
```

Вы также можете передать аргументы в конструктор вашей среды, чтобы настроить экземпляр среды. В нашем случае мы могли бы сделать:

```python
env = gymnasium.make('gym_examples/GridWorld-v0', size=10)
```

### [Обертки](https://gymnasium.farama.org/api/wrappers/)

Часто мы хотим использовать разные варианты пользовательской среды или хотим изменить поведение среды, предоставляемой Gymnasium или какой-либо другой стороной. Обертки позволяют нам делать это без изменения реализации среды или добавления какого-либо бойлерплейта. В нашем примере наблюдения нельзя использовать непосредственно в обучающем коде, потому что они являются словарями. Однако на самом деле нам не нужно трогать нашу реализацию среды, чтобы исправить это! Мы можем просто добавить оболочку поверх экземпляров среды, чтобы объединить наблюдения в один массив.

```python
import gym_examples
from gymnasium.wrappers import FlattenObservation

env = gymnasium.make('gym_examples/GridWorld-v0')
wrapped_env = FlattenObservation(env)
print(wrapped_env.reset())     # E.g.  [3 0 3 3], {}
```

У оберток есть большое преимущество, заключающееся в том, что они делают среду очень модульной. Например, вместо того, чтобы выравнивать наблюдения из GridWorld, вы можете захотеть посмотреть только относительное положение цели и агента.

```python
import gym_examples
from gym_examples.wrappers import RelativePosition

env = gymnasium.make('gym_examples/GridWorld-v0')
wrapped_env = RelativePosition(env)
print(wrapped_env.reset())     # E.g.  [-3  3], {}
```

[Подробнее об обертках](https://gymnasium.farama.org/api/wrappers/)

Смотри еще:

- [Gymnasium](https://gymnasium.farama.org/)
- [[stable-baseline-3]]
- [[reinforcement-learning]]


[//begin]: # "Autogenerated link references for markdown compatibility"
[stable-baseline-3]: stable-baseline-3 "Stable baseline 3"
[reinforcement-learning]: ..%2Flists%2Freinforcement-learning "Reinforcement learning"
[//end]: # "Autogenerated link references"